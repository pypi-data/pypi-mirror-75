import sys
import signal
import logging
import pkg_resources
from time import sleep
from snowctl.utils import *
from snowctl.config import Config
from snowctl.logger import logger_options
from snowctl.connect import snowflake_connect
from snowctl.arguments import arg_parser, cmd_parser

VERSION = pkg_resources.require('snowctl')[0].version
LOG = logging.getLogger(__name__)
BANNER = """\
 __        __        __  ___      
/__` |\ | /  \ |  | /  `  |  |    
.__/ | \| \__/ |/\| \__,  |  |___ 
                                 
"""

def print_usage():
    print('\nsnowctl usage:')
    print('\tuse <database|schema|warehouse> <name>')
    print('\tcopy views [-f] [-r] - copy view(s) in currect context to other schemas as is')
    print('\t\t[-f] - filter target view columns')
    print('\t\t[-r] - rename target view')
    print('\tlist views <filter> - list views in current context with an optional filter')
    print('\tpeek <view> - show first row of data from the view')
    print('\tsql <query> - execute sql query')
    print('\texit / ctrl+C\n')


class Controller:
    def __init__(self, conn, engine, safe):
        self.connection = conn
        self.engine = engine
        self.safe_mode = safe
        self.run = True
        self.prompt = 'snowctl> '
        self.curr_db = None
        self.curr_schema = None

    def run_console(self):
        self.listen_signals()
        print_usage()
        try:
            while self.run:
                self.get_prompt()
                print(self.prompt, end='', flush=True)
                user_input = sys.stdin.readline()
                cmd = parser(user_input)
                if self.operation(cmd) == -1:
                    print('command not found')
        except Exception as e:
            LOG.error(e)
        finally:
            self.exit_console()

    def operation(self, cmd: list):
        try:
            if cmd[0] == 'help':
                print_usage()
            elif cmd[0] == 'copy':
                try:
                    args = cmd_parser(cmd[2:])
                except Exception as e:
                    print(e)
                    pass
                self.copy_views(filter_cols=args.filter, rename=args.rename)
            elif cmd[0] == 'list':
                self.list_views(cmd)
            elif cmd[0] == 'peek':
                self.peek(cmd[1])
            elif cmd[0] == 'use':
                self.use(cmd)
            elif cmd[0] == 'sql':
                self.user_query(cmd)
            elif cmd[0] == 'exit':
                self.exit_console()
            else:
                return -1
        except Exception as e:
            print(f'Error. {e}')
            return -2

    def use(self, cmd: list):
        results = self.connection.execute(f"use {cmd[1]} {cmd[2]}")
        response = results.fetchone()
        print(response[0])        

    def user_query(self, cmd: list):
        cmd.pop(0)
        query = ' '.join(cmd)
        response = self.execute_query(query)
        for row in response:
            print(row)

    def peek(self, view):
        row = self.execute_query(f'select * from {self.curr_db}.{self.curr_schema}.{view} limit 1')
        print(row)

    def list_views(self, cmd):
        filter = False
        if len(cmd) == 3:
            filter = cmd[2]
        rows = self.execute_query('show views')
        for i, row in enumerate(rows):
            if filter:
                if filter.lower() in row[1].lower():
                    print(f'{i} - {row[1]}')
            else:
                print(f'{i} - {row[1]}')

    def copy_views(self, filter_cols=False, rename=False):
        from snowctl.copy import Copycat
        cp = Copycat(self.connection, self.engine, self.safe_mode)
        cp.copy_views(self.curr_db, filter_cols=filter_cols, rename=rename)

    def execute_query(self, query):
        LOG.debug(f'executing:\n{query}')
        ret = []
        results = self.connection.execute(query)
        while True:
            row = results.fetchone()
            if not row:
                break
            ret.append(row)
        return ret

    def get_prompt(self):
        prompt = ''
        response = self.execute_query('select current_warehouse(), current_database(), current_schema()')
        wh = response[0][0]
        db = response[0][1]
        schema = response[0][2]
        if wh is not None:
            prompt += f'{wh}:'
        if db is not None:
            prompt += f'{db}:'
            self.curr_db = db
        if schema is not None:
            prompt += f'{schema}:'
            self.curr_schema = schema
        if not len(prompt):
            self.prompt = 'snowctl> '
        else:
            prompt = prompt[:-1]
            self.prompt = f'{prompt}> '.lower()

    def exit_console(self):
        print('closing connections...')
        try:
            self.connection.close()
            self.engine.dispose()
        finally:
            sys.exit('exit')

    def listen_signals(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        if signum == signal.SIGINT or signum == signal.SIGTERM:
            self.exit_console()


def main():
    args = arg_parser()
    conf = Config()
    if args.echo:
        conf.echo_config()
    elif args.version:
        print(VERSION)
    else:
        print(BANNER)
        conf.write_config(args.configuration)
        logger_options(args.debug)
        conn, engine = snowflake_connect(conf.read_config())
        try:
            c = Controller(conn, engine, args.safe)
            c.run_console()
        finally:
            conn.close()
            engine.dispose()


if __name__ == '__main__':
    main()

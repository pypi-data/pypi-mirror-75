import sys
import getpass
import os.path
from configparser import ConfigParser
from os.path import dirname, realpath

class Config:

    def __init__(self):
        self.work_dir = dirname(realpath(__file__))
        self.config_path = f'{self.work_dir}/config.ini'
        self.config_parser = ConfigParser()

    def write_config(self, rewrite: bool):

        if os.path.isfile(self.config_path):
            config_exists = True
        else:
            config_exists = False

        if rewrite is True or config_exists is False:
            try:
                self.config_parser.read('config.ini')
                self.config_parser.add_section('snowflake')

                account = 'snowflake_account'
                user = 'snowflake_user'
                password = 'snowflake_password'
                wh = 'default_warehouse'
                db = 'default_database'

                if config_exists is False:
                    print('First time configuration, please provide following values')

                print('snowflake_account (e.g. "xy12345.east-us-2.azure"): ' , end='', flush=True)
                val = sys.stdin.readline().replace('\n', '').replace('snowflakecomputing.com', '')
                self.config_parser.set('snowflake', account, val)
                print('snowflake_user: ' , end='', flush=True)
                val = sys.stdin.readline().replace('\n', '')
                self.config_parser.set('snowflake', user, val)
                print('default_warehouse: ' , end='', flush=True)
                val = sys.stdin.readline().replace('\n', '')
                self.config_parser.set('snowflake', wh, val)
                print('default_database: ' , end='', flush=True)
                val = sys.stdin.readline().replace('\n', '')
                self.config_parser.set('snowflake', db, val)
                val = getpass.getpass('snowflake_password: ')
                self.config_parser.set('snowflake', password, val)

                with open(self.config_path, 'w') as f:
                    self.config_parser.write(f)
            except KeyboardInterrupt:
                sys.exit('\nconfig file was not updated')
            except Exception as e:
                sys.exit(f'error while writing configuration: {e}')
        return

    def read_config(self):
        try:
            r = {}
            self.config_parser.read(self.config_path)
            r['account'] = self.config_parser['snowflake']['snowflake_account']
            r['user'] = self.config_parser['snowflake']['snowflake_user']
            r['warehouse'] = self.config_parser['snowflake']['default_warehouse']
            r['database'] = self.config_parser['snowflake']['default_database']
            r['password'] = self.config_parser['snowflake']['snowflake_password']
            return r
        except KeyError as e:
            sys.exit(f'missing values in configuration: {e}')

    def echo_config(self):
        c = self.read_config()
        print('\ncurrent configuration')
        for k, v in c.items():
            if k == 'password':
                v = '*****'
            print(f'  {k}: {v}')

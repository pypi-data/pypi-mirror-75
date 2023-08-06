import sys
from snowctl.utils import *
from snowctl.snowctl import Controller

class Copycat(Controller):
    """
    Subclass of Controller to handle view copying
    """
    def __init__(self, conn, engine, safe):
        super().__init__(conn, engine, safe)

    def prompt_input(self, msg):
        print(msg, end='', flush=True)
        return sys.stdin.readline().replace('\n', '').strip().split(',')

    def get_views(self):
        views = []
        rows = self.execute_query('show views')
        for i, row in enumerate(rows):
            views.append(row[1])
            print(f'{i} - {row[1]}')
        return views

    def select_views(self):
        views = self.get_views()
        user_input = self.prompt_input('choose view(s) to copy ([int, int, ...]|all): ')
        copy_these = []
        if user_input == ['']:
            return None
        elif user_input[0] == 'all':
            copy_these = views
        else:
            for index in user_input:
                copy_these.append(views[int(index)])
        print(f'chose view(s) {", ".join(copy_these)}')
        return copy_these

    def get_ddls(self, views):
        ddls = []
        for view in views:
            ddl = self.execute_query(f"select GET_DDL('view', '{view}')")[0][0]
            newddl = make_overwrite(ddl)
            print(newddl)
            ddls.append(newddl)
        return ddls

    def get_schemas(self):
        schemas = []
        rows = self.execute_query('show schemas')
        rows.pop(0)  # Ignore information schema
        for i, row in enumerate(rows):
            schemas.append(row[1])
            print(f'{i} - {row[1]}')
        return schemas

    def select_schemas(self):
        schemas = self.get_schemas()
        user_input = self.prompt_input('copy into ([int, int, ...]|all): ')
        copy_into = []
        if user_input == ['']:
            return None
        elif user_input[0] == 'all':
            copy_into = schemas
        else:
            for index in user_input:
                copy_into.append(schemas[int(index)])
        print(f'chose schema(s) {", ".join(copy_into)}')
        return copy_into

    def copy_views(self, db, filter_cols=False, rename=False):
        errors = 0
        clear_screen()
        copy_these = self.select_views()
        if copy_these is None:
            return
        ddls = self.get_ddls(copy_these)
        copy_into = self.select_schemas()
        if copy_into is None:
            return
        if filter_cols:
            clear_screen()    
        for i, view in enumerate(copy_these):
            for schema in copy_into:
                query = format_ddl(ddls[i], view, schema, db)
                if filter_cols is True:
                    query = filter_ddl(query, view, db, schema)
                if rename is True:
                    query = rename_target(query, view, db, schema)
                if self.safe_mode:
                    if not self.ask_confirmation(query):
                        continue
                try:
                    results = self.connection.execute(query)
                    response = results.fetchone()
                except Exception as e:
                    print(e)
                    errors += 1
                    continue
                print(f'{response[0]} (target: {db}.{schema})')
        print(f'\ncopy views finished: {errors} errors\n')

    def ask_confirmation(self, query):
        print(f'\n{query}')
        print(f'Confirm? (y/n): ', end='', flush=True)
        user_input = sys.stdin.readline().replace('\n', '').strip()
        if user_input == 'y':
            return True
        else:
            return False

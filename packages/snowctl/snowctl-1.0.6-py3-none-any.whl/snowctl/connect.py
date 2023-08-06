import sys
import snowflake.connector
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

def snowflake_connect(conf):
    print('Connecting to snowflake... ', end='', flush=True)
    try:
        engine = create_engine(URL(
            user=conf['user'],
            password=conf['password'],
            account=conf['account'],
            warehouse=conf['warehouse'],
            database=conf['database'],
            schema='PUBLIC'
        ))
        conn = engine.connect()
        print('connected')
        return (conn, engine)
    except Exception as e:
        sys.exit(e)

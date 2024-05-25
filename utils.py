from packaging import version
import sqlalchemy
import urllib.parse
import pandas as pd
try: # sqlalchemy <=1.4.15 backwards compatibility
    from sqlalchemy import URL
except Exception:
    pass
from sqlalchemy import create_engine


def dbconnect(
    SQLdatabasename: str,
    database: dict,
    dialect_driver: str = 'mysql+pymysql',
    query = {}):
    """Establish connection to database

    Args:
        SQLdatabasename (str): Database name.
        database (dict, optional): {host:'', 'port': '', 'username': '', 'password': ''}
        dialect_driver (str, optional): SQLAlchemy dialect and driver. See https://docs.sqlalchemy.org/en/20/dialects/mysql.html#dialect-mysql

    Returns:
        [type]: [description]

    Examples:
    #### Example 1 (pandas):
        from credentials_engtk import database_credentials
        import sqlalchemy

        engine = dbconnect(SQLdatabasename = 'neomexicana_dash',
            database = database_credentials['Bane'],
            dialect_driver = 'mysql+pymysql')
        connection = engine.connect()

        pd.read_sql_table('lista_sucursales', con = connection)

        sql_dql = "SELECT * FROM neomexicana_dash.lista_sucursales"
        query = sqlalchemy.text(sql_dql)
        pd.read_sql_query(query, con = connection)
        
        connection.close()
        engine.dispose()

    #### Example 2 ( execute):
        from credentials_engtk import database_credentials
        import sqlalchemy

        engine = dbconnect(
            'neomexicana_dash',
            database_credentials['Bane'],
            'mysql+pymysql')
        sql_dql = "SELECT * FROM neomexicana_dash.lista_sucursales"
        query = sqlalchemy.text(sql_dql)
        with engine.begin() as conn:
            results = conn.execute(query).fetchall()
        print(results)
        engine.dispose()
    """
    # http://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#engine-connection-examples
    # https://docs.sqlalchemy.org/en/20/core/engines.html#creating-urls-programmatically
    # https://docs.sqlalchemy.org/en/20/core/engines.html#escaping-special-characters-such-as-signs-in-passwords
    # https://community.snowflake.com/s/article/Password-with-special-character-may-cause-authentication-failure-at-SQLAlchemy
    # https://stackoverflow.com/questions/75309237/read-sql-query-throws-optionengine-object-has-no-attribute-execute-with

    try: #
        url_object = URL.create( # https://docs.sqlalchemy.org/en/20/core/engines.html#creating-urls-programmatically
            dialect_driver,
            username=database['username'],
            password=database['password'],  # plain (unescaped) text
            host=database['host'],
            database=SQLdatabasename,
            query = query, # https://stackoverflow.com/questions/53704187/connecting-to-an-azure-database-using-sqlalchemy-in-python
        )
        engine = create_engine(url_object)
    except Exception:
        sqlalchemy_version = version.parse(sqlalchemy.__version__) < version.parse("2.0.0")
        pandas_version = version.parse(pd.__version__) <= version.parse('1.2.3')
        if (sqlalchemy_version & pandas_version): # numpy==1.23.5
            print("inside sqlalchemy")
            db_username = database['username']
            db_pasword = database['password']
        else: # https://docs.sqlalchemy.org/en/20/core/engines.html#escaping-special-characters-such-as-signs-in-passwords
            print("parsing")
            db_username = urllib.parse.quote_plus(database['username'])
            db_pasword = urllib.parse.quote_plus(database['password'])
        engine = sqlalchemy.create_engine(
            (f"{dialect_driver}://{db_username}"
            f":{db_pasword}"
            f"@{database['host']}"
            f":{database['port']}"
            f"/{SQLdatabasename}")
            )
    
    return engine


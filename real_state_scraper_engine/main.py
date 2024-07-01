from datetime import datetime, timezone
from pydantic_settings import BaseSettings
from pydantic import SecretStr
from utils import dbconnect
from mercadolibrerealstatescraper import fetch_mercadolibre_data

class Settings(BaseSettings):
    rdbms_server_name: SecretStr
    rdbms_server_port: SecretStr
    rdbms_username: SecretStr
    rdbms_password: SecretStr
    rdbms_database_name: SecretStr

settings = Settings()

database_credentials={
    'mercadolibre_scraper':
        {'host': settings.rdbms_server_name,
        'username': settings.rdbms_username,
        'password': settings.rdbms_password,
        'port': settings.rdbms_server_port}
    }

# https://stackoverflow.com/questions/10997577/python-timezone-conversion
# from datetime import tzinfo
timestamp = datetime.now(tz = timezone.utc)
# timestamp = datetime.now(tz = pytz.timezone("US/Pacific")) # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List

df = fetch_mercadolibre_data(search_offset = 0)
df['publication_check_timestamp_utc'] = timestamp


engine = dbconnect(
   SQLdatabasename = settings.rdbms_database_name,
   database = database_credentials['mercadolibre_scraper'],
   dialect_driver = 'mssql+pyodbc',
   query = {
        "driver": "ODBC Driver 18 for SQL Server",
        "TrustServerCertificate": "no",
        "Connection Timeout": "30",
        "Encrypt": "yes",
        'autocommit':"true"
    })
engine = engine.execution_options(autocommit=True)

connection = engine.connect()

cols_to_omit = ['shipping', 'seller', 'attributes',
         'location', 'seller_contact']
# HACK: Temporary fix -@paco at 5/23/2024, 5:33:54 AM
# SQL Sever complains of dictionaries inside the pandas.DataFrames. Converting to strings in the meantime
# TODO: Tasks pending completion -@paco at 5/23/2024, 5:42:10 AM
# Try to send the dict cell as json to SQL Server
df = df.astype(dict(zip(cols_to_omit, len(cols_to_omit) * [str])))
dict_cols = ['shipping', 'seller', 'attributes',
         'location', 'seller_contact']
cols_to_insert = ['id', 'title', 'price',
                  'latitude', 'longitude',
                  'city', 'state', 'property_area']
df[[*cols_to_insert, *dict_cols]].to_sql("RealStatePublications",con=engine, if_exists='replace', index=False)

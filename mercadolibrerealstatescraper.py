import requests
import pandas as pd
from datetime import datetime, timezone, tzinfo
import pytz
import sqlalchemy
from utils import dbconnect

# https://stackoverflow.com/questions/10997577/python-timezone-conversion
timestamp = datetime.now(tz = timezone.utc)
# timestamp = datetime.now(tz = pytz.timezone("US/Pacific")) # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List

def lat_long_zip_available(x, y = 'latitude'):
  if y in x:
    return x[y]

def get_property_area(ml):
    property_area = [a for a in ml if a['id'] == 'TOTAL_AREA'][0]['value_struct']['number']
    return property_area

def fetch_mercadolibre_data(id: list = ['id'],
               search_limit: int = 50, # max limit allowed for public users. If over 50, then a 400 http response error will be returned
               search_offset: int = 0,
               site_id: str =  'MLM', # Mexi
               category_id: int = 'MLM170363'
               ):

  url_query_params = f"category={category_id}&limit={search_limit}&offset={search_offset}"
  url = f"https://api.mercadolibre.com/sites/{site_id}/search?{url_query_params}"
  response = requests.request("GET", url, headers={}, data={})

  # ToDo: Save http response.content as is to a bronze layer

  df_inmuebles = pd.DataFrame(response.json()['results'])
  df_inmuebles.shape

  df_inmuebles['latitude'] = df_inmuebles['location'].apply(lat_long_zip_available, y = 'latitude')
  df_inmuebles['longitude'] = df_inmuebles['location'].apply(lat_long_zip_available, y = 'longitude')
  df_inmuebles['zip_code'] = df_inmuebles['location'].apply(lat_long_zip_available, y = 'zip_code')

  df_inmuebles['city'] = df_inmuebles['location'].apply(lambda x : x['city']['name'])
  df_inmuebles['state'] = df_inmuebles['location'].apply(lambda x : x['state']['name'])
  df_inmuebles['country'] = df_inmuebles['location'].apply(lambda x : x['country']['name'])

  df_inmuebles['property_area'] = df_inmuebles['attributes'].apply(get_property_area)

  return df_inmuebles

df = fetch_mercadolibre_data(search_offset = 0)
df['publication_check_timestamp_utc'] = timestamp


engine = dbconnect(
   SQLdatabasename = 'mercadolibre-scraper-database',
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

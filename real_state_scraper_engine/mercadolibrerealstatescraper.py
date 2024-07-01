import requests
import pandas as pd

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
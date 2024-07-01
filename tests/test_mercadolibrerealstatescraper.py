from real_state_scraper_engine.mercadolibrerealstatescraper import lat_long_zip_available

def test_lat_long_zip_available():
    target_value = 40.7
    coord = lat_long_zip_available(
        x = {'latitude': target_value,
            'longitude': -74.0})
    assert coord == target_value


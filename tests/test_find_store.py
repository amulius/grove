from find_store import geocode, format_stores, run
from tests.constants import TEST_STORES, ACCEPTABLE_ERROR, GoogleValues, GOOD_ADDRESS, BAD_ADDRESS


def percent_difference(a, b):
    return abs(b - a) / b


def test_format_stores_count():
    formatted_stores = format_stores(TEST_STORES)
    assert len(formatted_stores) == 10


def test_format_stores_content():
    formatted_stores = format_stores(TEST_STORES)
    for store in formatted_stores:
        assert 'Latitude' in store and store['Latitude'] is not None
        assert 'Longitude' in store and store['Longitude'] is not None
        assert 'Address' in store and store['Address'] is not None


def test_geocode_fail():
    assert geocode(BAD_ADDRESS) is None


def test_geocode_pass():
    assert geocode(GOOD_ADDRESS) is not None


def test_geocode():
    geocode_zip_latitude, geocode_zip_longitude = geocode('94530')
    geocode_address_latitude, geocode_address_longitude = geocode(GOOD_ADDRESS)

    assert percent_difference(geocode_zip_latitude, GoogleValues.zip_latitude) <= ACCEPTABLE_ERROR
    assert percent_difference(geocode_zip_longitude,  GoogleValues.zip_longitude) <= ACCEPTABLE_ERROR
    assert percent_difference(geocode_address_latitude, GoogleValues.address_latitude) <= ACCEPTABLE_ERROR
    assert percent_difference(geocode_address_longitude, GoogleValues.address_longitude) <= ACCEPTABLE_ERROR


def test_run_fail():
    try:
        run(BAD_ADDRESS, None, False, TEST_STORES)
    except SystemExit:
        assert True
    else:
        assert False


def test_run_pass():
    try:
        run(GOOD_ADDRESS, None, False, TEST_STORES)
    except SystemExit:
        assert False
    else:
        assert True

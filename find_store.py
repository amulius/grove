"""Find Store
  find_store will locate the nearest store (as the vrow flies) from
  store-locations.csv, print the matching store address, as well as
  the distance to that store.

Usage:
  find_store --address=<address>
  find_store --address=<address>  [--units=(mi|km)] [--output=(text|json)]
  find_store --zip=<zip>
  find_store --zip=<zip> [--units=(mi|km)] [--output=(text|json)]

Options:
  --zip=<zip>           Find nearest store to this zip code. If there are multiple best-matches, return the first.
  --address=<address>   Find nearest store to this address. If there are multiple best-matches, return the first.
  --units=(mi|km)       Display units in miles or kilometers [default: mi].
  --output=(text|json)  Output in human-readable text, or in JSON (e.g. machine-readable) [default: text].

Example
  find_store --address="1770 Union St, San Francisco, CA 94123"
  find_store --zip=94115 --units=km
"""
from collections import defaultdict
from docopt import docopt
import csv
from math import sin, cos, sqrt, atan2, radians
from geopy.geocoders import Nominatim

EARTH_RADIUS = 6372.795


def format_stores(file_name):
    with open(file_name, 'rb') as store_locations:
        store_reader = csv.reader(store_locations, delimiter=',', quotechar='"')
        keys = next(store_reader)  # skip the headers
        return [{key: val for key, val in zip(keys, prop)} for prop in store_reader]


def geocode(somewhere):
    geolocator = Nominatim()
    location = geolocator.geocode(somewhere)
    if location:
        return location.latitude, location.longitude
    else:
        return None


def distance(point_a, point_b):
    # from https://en.wikipedia.org/wiki/Great-circle_distance#Computational_formulas
    # this assumes the earth is a uniform sphere, faster and easier calculation,
    # but not as accurate as Vincenty's formulae
    latitude_a, longitude_a = radians(point_a[0]), radians(point_a[1])  # convert to radians
    latitude_b, longitude_b = radians(point_b[0]), radians(point_b[1])  # convert to radians

    sin_lat_a, cos_lat_a = sin(latitude_a), cos(latitude_a)
    sin_lat_b, cos_lat_b = sin(latitude_b), cos(latitude_b)

    delta_longitude = longitude_b - longitude_a
    cos_delta_lng, sin_delta_lng = cos(delta_longitude), sin(delta_longitude)

    radians_a_to_b = atan2(sqrt(pow((cos_lat_b * sin_delta_lng), 2) +
                                pow((cos_lat_a * sin_lat_b - sin_lat_a * cos_lat_b * cos_delta_lng), 2)),
                           sin_lat_a * sin_lat_b + cos_lat_a * cos_lat_b * cos_delta_lng)

    # assume uniform sphere/circle, distance is the radius * the angle in radians
    return EARTH_RADIUS * radians_a_to_b


def map_stores(stores_formatted, geocoded_address):
    distance_map = defaultdict(lambda: [])
    for store in stores_formatted:
        store_loc = (float(store['Latitude']), float(store['Longitude']))
        dist = distance(geocoded_address, store_loc)
        distance_map[dist].append(store)
    return distance_map


def print_formatted_output(store, distance_km, is_miles, is_json):
    distance_to_store = distance_km
    closest_store = store[0]
    if is_miles:
        distance_to_store *= 0.621371
        units = 'miles'
    else:
        units = 'km'

    distance_to_store_formatted = '%s %s' % (distance_to_store, units)

    if is_json:
        response = closest_store
        response['distance'] = distance_to_store
        response['units'] = units
    else:
        lead = 'Closest store found.'
        found = 'Store:%s located at %s %s %s, %s away' % \
                (closest_store['Store Name'],
                 closest_store['Address'],
                 closest_store['City'],
                 closest_store['State'],
                 distance_to_store_formatted)

        response = '%s\n%s' % (lead, found)

    print response


def run(address, zip_code, is_miles, is_json, store_file):
    formatted_stores = format_stores(store_file)

    where = address if address else zip_code

    where_geocoded = geocode(where)

    if where_geocoded:
        store_distance_map = map_stores(formatted_stores, where_geocoded)
        # list of keys/distances ordered by distance
        distances = sorted(store_distance_map.iterkeys())
        print_formatted_output(store_distance_map[distances[0]], distances[0], is_miles, is_json)
    else:
        print 'Unable to geocode your location'
        raise SystemExit(1)  # for tests


if __name__ == '__main__':
    arguments = docopt(__doc__)

    address = arguments['--address']
    zip_code = arguments['--zip']
    is_miles = arguments['--units'] == 'mi'
    is_json = arguments['--output'] == 'json'

    run(address, zip_code, is_miles, is_json, 'store-locations-2.csv')

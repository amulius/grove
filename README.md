# grove

My version of the store locator first unpacks the arguments

then takes the csv and formats it to a list of dicts, attempts to geocode the given address or zipcode

if it is not able to geocode the address then it exits letting the user know it was not successful

if it does geocode, then it creates a hash map of the stores and their distances from the address,
and finally it returns the closest store to the user in either text or json format


The big assumption this makes is it assumes the earth is a uniform sphere and uses the great-circle distance, 
I did it this way because it was faster and easier to calculate, the trade-off is that it's not as accurate as the 
Vincenty's formulae which does not assume the earth is uniform sphere.


#Instructions
create a virtual env, then `pip install -t requirements.txt`
```
Usage:
  python find_store.py --address=<address>
  python find_store.py --address=<address>  [--units=(mi|km)] [--output=(text|json)]
  python find_store.py --zip=<zip>
  python find_store.py --zip=<zip> [--units=(mi|km)] [--output=(text|json)]

Options:
  --zip=<zip>           Find nearest store to this zip code. If there are multiple best-matches, return the first.
  --address=<address>   Find nearest store to this address. If there are multiple best-matches, return the first.
  --units=(mi|km)       Display units in miles or kilometers [default: mi].
  --output=(text|json)  Output in human-readable text, or in JSON (e.g. machine-readable) [default: text].

Example
  python find_store.py --address="1770 Union St, San Francisco, CA 94123"
  python find_store.py --zip=94115 --units=km
```

to test just run `pytest`
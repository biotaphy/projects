"""Module containing functions for interacting with GBIF APIs."""
import urllib
import requests

MAX_POINTS = 10000
LOCAL_LIMIT = 500

# .............................................................................
def get_gbif_accepted_name(name_str):
    """Get the accepted name for a name string."""
    other_filters = {'name': name_str.strip(), 'verbose': 'true'}
    url = 'http://api.gbif.org/v1/species/match?{}'.format(
        urllib.parse.urlencode(other_filters))
    response = requests.get(url).json()
    if response['status'].lower() in ('accepted', 'synonym'):
        return (response['canonicalName'], response['speciesKey'])
    return None, None


# .............................................................................
def get_points_from_gbif(taxon_key, max_points=MAX_POINTS):
    """Get points from GBIF using the provided taxon key."""
    offset = 0
    other_filters = {
        'taxonKey': taxon_key,
        'limit': LOCAL_LIMIT,
        'hasCoordinate': 'true',
        'hasGeospatialIssue': 'false',
        'offset': offset
    }
    url = 'http://api.gbif.org/v1/occurrence/search?{}'
    ret_points = []
    response = requests.get(
        url.format(urllib.parse.urlencode(other_filters))).json()
    ret_points.extend(response['results'])
    while not response['endOfRecords'] and offset < max_points:
        offset += LOCAL_LIMIT
        other_filters['offset'] = offset
        response = requests.get(
            url.format(urllib.parse.urlencode(other_filters))).json()
        ret_points.extend(response['results'])
    return ret_points

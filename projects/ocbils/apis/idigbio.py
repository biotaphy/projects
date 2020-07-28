"""Module containing functions for accessing iDigBio APIs."""
import urllib
import requests

# .............................................................................
def get_points_from_idigbio(species_key=None, genus_key=None,
                            max_points=MAX_POINTS):
    """Get points from iDigBio using the provided species or genus key."""
    offset = 0
    base_url = 'https://search.idigbio.org/v2/search/records'
    ret_points = []
    url_params = {
        'limit': LOCAL_LIMIT,
        'offset': offset,
        'no_attribution': 'false'
    }
    other_filters = {
        'rq': {
            'basisofrecord': 'preservedspecimen'
            }
        }
    if species_key:
        other_filters['rq']['taxonid'] = species_key
    elif genus_key:
        other_filters['rq']['genus'] = genus_key
    else:
        raise ValueError('Either species_key or genus_key must be specified')
    url = '{}?{}'.format(base_url, urllib.parse.urlencode(url_params))
    response = requests.post(url, json=other_filters).json()
    ret_points.extend(response['items'])
    while offset + LOCAL_LIMIT <= response['itemCount'] and \
            offset < max_points:
        offset += LOCAL_LIMIT
        url_params['offset'] = offset
        url = '{}?{}'.format(base_url, urllib.parse.urlencode(url_params))
        response = requests.post(url, json=other_filters).json()
        ret_points.extend(response['items'])
    return ret_points

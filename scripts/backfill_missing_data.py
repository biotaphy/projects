"""Attempt to retrieve missing data"""
import argparse
import json
from operator import itemgetter
import os
from time import sleep
import urllib
import requests

from lmpy.data_preparation.occurrence_transformation import convert_json_to_point

from tools.apis.gbif import get_points_from_gbif
from tools.apis.idigbio import get_points_from_idigbio
from tools.apis.powo import get_species_kew, get_kew_id_for_species
from tools.common.utilities import get_species_filename


def species_chain_getter(*args):
    atts = list(args)
    def getter(obj):
        for att in atts:
            obj = itemgetter(att)(obj)
        return obj.capitalize()
    return getter
    
def chain_getter(*args):
    atts = list(args)
    def getter(obj):
        for att in atts:
            obj = itemgetter(att)(obj)
        return obj
    return getter

# .............................................................................
def get_genus_path(genus_name):
    """Get the base path for a genus"""
    return os.path.join(BASE_DIR, 'genera', genus_name)


# .............................................................................
def read_failures(fail_filename):
    """Get a list of failed species with keys"""
    failed_species = []
    with open(fail_filename, mode='r', encoding='utf8') as in_fails:
        for line in in_fails:
            sp_key, sp_name = line.strip().split(', ')
            failed_species.append((sp_key, sp_name))
    return failed_species


# .............................................................................
def write_points(filename, point_objs):
    """Write points to file."""
    with open(filename, mode='w', encoding='utf8') as point_file:
        for pt in point_objs:
            point_file.write('{}, {}, {}, "{}"\n'.format(
                pt.species_name, pt.x, pt.y, ','.join(pt.flags)))


# # .............................................................................
# def get_points_from_gbif(taxon_key, max_points=MAX_POINTS):
#     """Get points from GBIF using the provided taxon key."""
#     offset = 0
#     other_filters = {
#         'taxonKey': taxon_key,
#         'limit': LOCAL_LIMIT,
#         'hasCoordinate': 'true',
#         'hasGeospatialIssue': 'false',
#         'offset': offset
#     }
#     url = 'http://api.gbif.org/v1/occurrence/search?{}'
#     ret_points = []
#     response = requests.get(
#         url.format(urllib.parse.urlencode(other_filters))).json()
#     ret_points.extend(response['results'])
#     while not response['endOfRecords'] and offset < max_points:
#         offset += LOCAL_LIMIT
#         other_filters['offset'] = offset
#         response = requests.get(
#             url.format(urllib.parse.urlencode(other_filters))).json()
#         ret_points.extend(response['results'])
#     return ret_points


# .............................................................................
def get_gbif(species_key, species_name, base_dir):
    """Attempt to get gbif record for species."""
    # Get points
    json_points = get_points_from_gbif(species_key)
    converted_points = []
    if len(json_points) > 0:
        # Convert points
        converted_points = convert_json_to_point(
            json_points, itemgetter('species'), itemgetter('decimalLongitude'),
            itemgetter('decimalLatitude'), flags_getter=itemgetter('issues'))
    # Get file name
    sp_filename = get_species_filename(species_name, base_dir, '_gbif', '.csv')
    # Write points
    write_points(sp_filename, converted_points)


# .............................................................................
def get_idigbio(species_key, species_name, base_dir):
    """Attempt to get idigbio record for species."""
    # Get points
    json_points = get_points_from_idigbio(species_key=species_key)
    converted_points = []
    if len(json_points) > 0:
        # Convert points
        converted_points = convert_json_to_point(
            json_points, species_chain_getter('indexTerms', 'canonicalname'),
            chain_getter('indexTerms', 'geopoint', 'lon'),
            chain_getter('indexTerms', 'geopoint', 'lat'),
            flags_getter=chain_getter('indexTerms', 'flags'))
    # Get file name
    sp_filename = get_species_filename(species_name, base_dir, '_idigbio', '.csv')
    # Write points
    write_points(sp_filename, converted_points)

# .............................................................................
def get_powo(species_key, species_name, base_dir):
    """Attempt to get powo record for species."""
    # Get data
    #try:
    result = {}
    fq_id = get_kew_id_for_species(species_name)
    #except Exception:
    #    fq_id = None
    if fq_id:
        result = get_species_kew(fq_id)

    # Get file name
    sp_filename = get_species_filename(species_name, base_dir, '_powo', '.json')
    # Write
    with open(sp_filename, 'w', encoding='utf8') as powo_out:
        json.dump(result, powo_out)


# .............................................................................
def main():
    """Main method."""
    parser = argparse.ArgumentParser()
    parser.add_argument('base_dir', type=str, help='Base data directory')
    parser.add_argument(
        'powo_fails_filename', type=str,
        help='File location to store missing powo taxa')
    parser.add_argument(
        'gbif_fails_filename', type=str,
        help='File location to store missing gbif taxa')
    parser.add_argument(
        'idigbio_fails_filename', type=str,
        help='File location to store missing idigbio taxa')
    args = parser.parse_args()
    max_fails = 10
    
    
    # Get failed taxa for each service
    powo_species = read_failures(args.powo_fails_filename)
    gbif_species = read_failures(args.gbif_fails_filename)
    idigbio_species = read_failures(args.idigbio_fails_filename)
    len_powo = len(powo_species)
    len_gbif = len(gbif_species)
    len_idigbio = len(idigbio_species)
    # While i from 0 to max length of failures
    num_fails = 0
    for i in range(max([len_powo, len_gbif, len_idigbio])):
        try:
            if i < len_powo:
                get_powo(*powo_species[i], args.base_dir)
            if i < len_gbif:
                get_gbif(*gbif_species[i], args.base_dir)
            if i < len_idigbio:
                get_idigbio(*idigbio_species[i], args.base_dir)
        except Exception as err:
            num_fails += 1
            print('Failed ({} of {}): {}'.format(num_fails, max_fails, err))
            print('Sleep 60 seconds...')
            sleep(60)
            if num_fails >= max_fails:
                raise Exception('Failed maximum number of times')


# .............................................................................
if __name__ == '__main__':
    main()

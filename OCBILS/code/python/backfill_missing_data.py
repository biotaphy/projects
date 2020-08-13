"""Attempt to retrieve missing data"""
import argparse
import json
from operator import itemgetter
import os
from time import sleep

from lmpy.data_preparation.occurrence_transformation import (
    convert_json_to_point)

from apis.gbif import get_points_from_gbif
from apis.idigbio import get_points_from_idigbio
from apis.powo import get_species_kew, get_kew_id_for_species


# .............................................................................
def get_species_filename(species_name, base_dir, service_suffix, file_ext):
    """Get the file name for the species data / service combination.

    Args:
        species_name (str): The name of the species.
        base_dir (str): The base directory to write points.
        service_suffix (str): The service suffix for the data files.
        file_ext (str): The extension for the filename.
    """
    temp = species_name.replace(
        '_', ' ').replace('.', '_').replace('/', '_').split(' ')
    genus = temp[0]
    if len(temp) == 1:
        escaped_species = genus
    else:
        escaped_species = '{} {}'.format(genus, temp[1])
    genus_dir = os.path.join(base_dir, genus)
    species_filename = os.path.join(
        genus_dir, '{}{}{}'.format(escaped_species, service_suffix, file_ext))
    if not os.path.exists(genus_dir):
        os.mkdir(genus_dir)
    return species_filename


# .............................................................................
def species_chain_getter(*args):
    """Get a species name through nested attributes."""
    atts = list(args)

    def getter(obj):
        for att in atts:
            obj = itemgetter(att)(obj)
        return obj.capitalize()
    return getter


# .............................................................................
def chain_getter(*args):
    """Chain getter that retrieves nested attributes."""
    atts = list(args)

    def getter(obj):
        for att in atts:
            obj = itemgetter(att)(obj)
        return obj
    return getter


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
        for point in point_objs:
            point_file.write('{}, {}, {}, "{}"\n'.format(
                point.species_name, point.x, point.y, ','.join(point.flags)))


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
    sp_filename = get_species_filename(
        species_name, base_dir, '_idigbio', '.csv')
    # Write points
    write_points(sp_filename, converted_points)


# .............................................................................
def get_powo(species_key, species_name, base_dir):
    """Attempt to get powo record for species."""
    # Get data
    result = {}
    fq_id = get_kew_id_for_species(species_name)
    if fq_id:
        result = get_species_kew(fq_id)

    # Get file name
    sp_filename = get_species_filename(
        species_name, base_dir, '_powo', '.json')
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

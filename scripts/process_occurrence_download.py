"""Process a GBIF download and write out species data as separate files."""
import argparse
import json
from operator import attrgetter, itemgetter
import os
import sys

#sys.path.append('/home/cjgrady/git/projects/')

from lmpy.data_preparation.occurrence_transformation import (
    convert_delimited_to_point, convert_json_to_point)
from tools.common.utilities import get_species_filename

def json_getter(fld_idx):
    def getter(obj):
        if len(obj[fld_idx]) > 1:
            return json.loads(obj[fld_idx])
        else:
            return []
    return getter

def key_getter(fld_idx, get_key):
    def getter(obj):
        return json.loads(obj[fld_idx])[get_key]
    return getter

def species_name_getter(genus_index, species_index):
    def getter(obj):
        return '{} {}'.format(obj[genus_index].capitalize(), obj[species_index])
    return getter

def gbif_flag_getter(fld_idx):
    def getter(obj):
        return obj[fld_idx].replace(';', ',')
    return getter

# .............................................................................
def convert_gbif_download(filename):
    """Convert a GBIF download to points.

    Args:
        filename (str): The file location of the GBIF download.
    """
    return convert_delimited_to_point(
        filename, itemgetter(9), itemgetter(22), itemgetter(21),
        flags_getter=gbif_flag_getter(49), delimiter='\t', headers=True)


# .............................................................................
def convert_idigbio_download(filename):
    """Convert a iDigBio download to points.

    Args:
        filename (str): The file location of the iDigBio download.
    """
    return convert_delimited_to_point(
        filename, species_name_getter(33, 69), key_getter(35, 'lon'),
        key_getter(35, 'lat'),
        flags_getter=json_getter(31), delimiter=',', headers=True)

# .............................................................................
def write_points(points, base_dir, service_suffix):
    """Write the sorted points into separate directories and files.

    Args:
        points (list of Point): A list of points sorted by species name.
        base_dir (str): The base directory to write points.
        service_suffix (str): The service suffix for the data files.
    """
    current_species = None
    out_file = None
    for point in points:
        if point.species_name != current_species:
            if out_file:
                out_file.close()
            current_species = point.species_name
            #print(point)
            #print(current_species)
            out_file = open(
                get_species_filename(
                    current_species, base_dir, service_suffix, '.csv'), 'w')
        if isinstance(point.flags, list):
            flags = ','.join(point.flags)
        elif isinstance(point.flags, str):
            flags = point.flags
        else:
            flags = ''
        out_file.write(
            '{}, {}, {}, "{}"\n'.format(
                point.species_name, point.x, point.y, flags))
    if out_file:
        out_file.close()

# .............................................................................
def main():
    """Main method for script."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'provider', type=str, choices=('idigbio', 'gbif'),
        help='The data provider service that created the download.')
    parser.add_argument(
        'filename', type=str, help='The downloaded occurrence data file.')
    parser.add_argument(
        'base_dir', type=str, help='The base directory to write data')
    args = parser.parse_args()
    print('Getting points...')
    if args.provider == 'idigbio':
        points = convert_idigbio_download(args.filename)
        service_suffix = '_idigbio'
    else:
        points = convert_gbif_download(args.filename)
        service_suffix = '_gbif'
    print('Sorting points...')
    points.sort(key=attrgetter('species_name'))
    print('Writing points...')
    write_points(points, args.base_dir, service_suffix)


# .............................................................................
if __name__ == '__main__':
    main()

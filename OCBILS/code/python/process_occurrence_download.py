"""Process an occurrence download and write out species data."""
import argparse
import os

from lmpy.data_preparation.occurrence_transformation import (
    convert_gbif_download, convert_idigbio_download)


# .............................................................................
def get_species_filename(species_name, base_dir, service_suffix):
    """Get the file name for the species data / service combination.

    Args:
        species_name (str): The name of the species.
        base_dir (str): The base directory to write points.
        service_suffix (str): The service suffix for the data files.
    """
    temp = species_name.replace('_', ' ').split(' ')
    genus = temp[0]
    escaped_species = '{} {}'.format(genus, temp[1])
    genus_dir = os.path.join(base_dir, genus)
    species_filename = os.path.join(
        genus_dir, '{}{}.csv'.format(escaped_species, service_suffix))
    if not os.path.exists(genus_dir):
        os.mkdir(genus_dir)
    return species_filename


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
            out_file = open(
                get_species_filename(
                    current_species, base_dir, service_suffix), 'w')
        if point.flags:
            flags = ','.join(point.flags)
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
    points.sort()
    print('Writing points...')
    write_points(points, args.base_dir, service_suffix)


# .............................................................................
if __name__ == '__main__':
    main()

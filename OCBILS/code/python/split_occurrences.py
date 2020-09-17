"""Split occurrence records based on a field"""
import argparse
import json

from lmpy.point import PointCsvReader, PointCsvWriter
from lmpy.data_preparation.occurrence_transformation import split_points
from lmpy.data_wrangling.occurrence.factory import wrangler_factory


CHARACTER_SET = list('abcdefghijklmnopqrstuvwxyz')


# .............................................................................
def get_all_combos(character_set, num_left):
    """Recurse to get all combinations of characters."""
    if num_left <= 1:
        return character_set
    all_combinations = []
    for char in character_set:
        for combo in get_all_combos(character_set, num_left - 1):
            all_combinations.append('{}{}'.format(char, combo))
    return all_combinations


# .............................................................................
def main():
    """Main method for script."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--filter_config', type=argparse.FileType('r'), action='append',
        help='Data wrangler configuration filename.')
    parser.add_argument('base_out_filename', type=str, help='Output file location')
    parser.add_argument('species_field', type=str, help='Field in CSV for species name')
    parser.add_argument('x_field', type=str, help='Field in CSV for X coordinate')
    parser.add_argument('y_field', type=str, help='Field in CSV for Y coordinate')
    parser.add_argument('group_size', type=int)
    parser.add_argument('group_position', type=int)
    parser.add_argument('group_attribute', type=str)
    parser.add_argument(
        'in_filename', type=str, nargs='+',
        help='Input CSV file location')
    args = parser.parse_args()

    # Initialize point readers
    readers = []
    for filename in args.in_filename:
        point_reader = PointCsvReader(
            filename, args.species_field, args.x_field, args.y_field)
        point_reader.open()
        readers.append(point_reader)

    # Load data wranglers
    wranglers = []
    if args.filter_config:
        wranglers = [wrangler_factory(json.load(config)) for config in args.filter_config]

    writers = {}
    for combo in get_all_combos(CHARACTER_SET, args.group_size):
        out_filename = '{}{}.csv'.format(args.base_out_filename, combo)
        writers[combo] = PointCsvWriter(
            out_filename, ['species_name', 'x', 'y'])
        writers[combo].open()
    # Split the occurrence data files
    split_points(
        readers, writers, args.group_attribute, args.group_size,
        args.group_position, wranglers=wranglers)
    for writer in writers.values():
        writer.close()

    # Close readers
    for point_reader in readers:
        point_reader.close()






# .............................................................................
if __name__ == '__main__':
    main()

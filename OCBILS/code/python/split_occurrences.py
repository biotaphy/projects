"""Split occurrence records based on a field"""
import argparse

from point_io import PointCsvReader, PointCsvWriter

CHARACTER_SET = list('abcdefghijklmnopqrstuvwxyz')


# .............................................................................
def get_chunk_key(value, group_position, group_size, filler_char='a'):
    """Get the chunk key from the value."""
    value += 10 * filler_char
    chunk = value[
        group_size * group_position:group_size * (group_position + 1)].lower()
    return chunk


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
def split_occurrences(point_reader, point_writers, group_size, group_position,
                      group_attribute):
    """Split occurrences into multiple files."""
    # Open writers
    for point in point_reader:
        location_key = get_chunk_key(
            point.get_attribute(group_attribute), group_position, group_size)
        point_writers[location_key].write_points(point)


# .............................................................................
def main():
    """Main method for script."""
    parser = argparse.ArgumentParser()
    # Todo: Need to take a list of input files
    # Todo: Fix this so can be specified before positional args
    parser.add_argument(
        '-f', '--filter_configs', type=argparse.FileType('r'), nargs='*',
        help='File location of filter configuration')
    parser.add_argument('in_filename', type=str, help='Input file location')
    parser.add_argument(
        'base_out_filename', type=str, help='Base output file location')
    parser.add_argument('species_field', type=str)
    parser.add_argument('x_field', type=str)
    parser.add_argument('y_field', type=str)
    parser.add_argument('group_size', type=int)
    parser.add_argument('group_position', type=int)
    parser.add_argument('group_attribute', type=str)
    args = parser.parse_args()
    # Get input reader
    point_reader = PointCsvReader(
        args.in_filename, args.species_field, args.x_field, args.y_field)
    point_reader.open()

    writers = {}
    for combo in get_all_combos(CHARACTER_SET, args.group_size):
        out_filename = '{}{}.csv'.format(args.base_out_filename, combo)
        writers[combo] = PointCsvWriter(
            out_filename, ['species_name', 'x', 'y'])
        writers[combo].open()
    split_occurrences(
        point_reader, writers, args.group_size, args.group_position,
        args.group_attribute)
    for writer in writers.values():
        writer.close()
    point_reader.close()


# .............................................................................
if __name__ == '__main__':
    main()

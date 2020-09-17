"""Sort occurrence records.

Sort a single file based on a group field
"""
import argparse
import json

from lmpy import PointCsvReader, PointCsvWriter
from lmpy.data_preparation.occurrence_transformation import sort_points
from lmpy.data_wranglers.occurrence.factory import wrangler_factory


# .............................................................................
def main():
    """Main method for script."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--filter_config', type=argparse.FileType('r'), action='append',
        help='Data wrangler configuration filename.')
    parser.add_argument('in_filename', type=str,
        help='Input CSV file location')
    parser.add_argument('out_filename', type=str, help='Output file location')
    parser.add_argument('species_field', type=str,
        help='Field in CSV for species name')
    parser.add_argument('x_field', type=str,
        help='Field in CSV for X coordinate')
    parser.add_argument('y_field', type=str,
        help='Field in CSV for Y coordinate')
    args = parser.parse_args()

    # Load data wranglers
    wranglers = [wrangler_factory(json.load(args.filter_config))]

    # Initialize point reader
    with PointCsvReader(
            filename, args.species_field, args.x_field, args.y_field
            ) as reader:
        # Open point writer
        with PointCsvWriter(args.out_filename, ['species_name', 'x', 'y']
                ) as writer:
            # Sort points
            sort_points(readers, writer, wranglers=wranglers)


# .............................................................................
if __name__ == '__main__':
    main()

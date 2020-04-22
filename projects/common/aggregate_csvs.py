"""Aggregate csv and report files."""
import argparse
import glob
import os


# .............................................................................
def create_report(in_dir, report_filename, omitted_species):
    """Create the report file."""
    with open(report_filename, 'w') as out_file:
        out_file.write('Omitted species due to not enough points (>0 but less than minimum)\n')
        for sp, cnt in omitted_species:
            out_file.write('    {}: {}\n'.format(sp, cnt))
        out_file.write('\n\nFilter counts:\n')
        out_file.write('Species name, idigbio, gbif, bbox, duplicates, locality\n')
        for fn in glob.glob(os.path.join(in_dir, '*report.txt')):
            species = os.path.basename(fn).split('_report.txt')[0]
            with open(fn) as in_file:
                for line in in_file:
                    out_file.write('{}, {}'.format(species, line))

# .............................................................................
def create_csv_file(in_dir, csv_filename, min_points):
    """Create the main csv file."""
    omitted_species = []
    with open(csv_filename, 'w') as out_file:
        for fn in glob.glob(os.path.join(in_dir, '*.csv')):
            with open(fn) as in_file:
                sp_points = in_file.readlines()
                if len(sp_points) >= min_points:
                    for line in sp_points:
                        out_file.write(line)
                elif len(sp_points) > 0:
                    omitted_species.append(
                        (os.path.basename(fn).split('_points.csv')[0],
                         len(sp_points)))
    return omitted_species

# .............................................................................
def main():
    """Main method for script."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=int, default=12, help='Minimum number of points')
    parser.add_argument('csv_filename')
    parser.add_argument('report_filename')
    parser.add_argument('in_dir')
    args = parser.parse_args()
    omitted_species = create_csv_file(args.in_dir, args.csv_filename, args.m)
    create_report(args.in_dir, args.report_filename, omitted_species)


# .............................................................................
if __name__ == '__main__':
    main()

"""Single species script."""
import argparse
from collections import namedtuple
import json
import os
from data_preparation.filters import (
    get_bounding_box_filter, get_data_flag_filter,get_tdwg_locality_filter,
    get_unique_localities_filter)

# .............................................................................
Point = namedtuple('Point', 'species_name, x, y, flags')
GBIF_FILTER_FLAGS = [
    'TAXON_MATCH_FUZZY', 'TAXON_MATCH_HIGHERRANK', 'TAXON_MATCH_NONE']
IDIGBIO_FILTER_FLAGS = [
    'geopoint_datum_missing', 'geopoint_bounds', 'geopoint_datum_error',
    'geopoint_similar_coord', 'rev_geocode_mismatch', 'rev_geocode_failure',
    'geopoint_0_coord', 'taxon_match_failed', 'dwc_kingdom_suspect',
    'dwc_taxonrank_invalid', 'dwc_taxonrank_removed']


# .............................................................................
def get_points_from_csv(csv_filename):
    """Load points from a csv"""
    with open(csv_filename, 'r') as in_file:
        reader = csv.reader(in_file)
        points = [Point(row[0], row[1], row[2], json.loads(row[3])) for row in reader]
        reader.close()
    return points

# .............................................................................
def get_species_list_from_file(filename):
    species_names = []
    with open(filename) as in_file:
        for line in in_file:
            try:
                parts = line.split(',')
                species_names.append(parts[1].strip().strip('"'))
            except Exception as err:
                print(err)
    return species_names

# .............................................................................
def filter_points(points_in, flt):
    out_points = []
    num_removed = 0
    for point in points_in:
        if flt(point):
            out_points.append(point)
        else:
            num_removed += 1
    return (out_points, num_removed)

# .............................................................................
def _get_filename(base_dir, species, service_suffix):
    genus = species.split(' ')[0]
    return os.path.join(base_dir, genus, '{}{}'.format(species, service_suffix))

# .............................................................................
def get_gbif_points(base_dir, species):
    fn = _get_filename(base_dir, species, '_gbif.csv')
    if os.path.exists(fn):
        points = []
        with open(fn, 'r') as in_file:
            for line in in_file:
                try:
                    row = line.strip().split(', ')
                    points.append(Point(row[0], float(row[1]), float(row[2]), json.loads(row[3].replace(',', '').replace(';', ','))))
                except Exception as err:
                    print(err)
        return points
    return []

# .............................................................................
def get_process_species_function(base_dir, idigbio_flags, gbif_flags, bbox):
    idigbio_flag_filter = get_data_flag_filter(idigbio_flags)
    gbif_flag_filter = get_data_flag_filter(gbif_flags)
    bbox_filter = get_bounding_box_filter(*bbox)
    unique_filter = get_unique_localities_filter()

    def process_species(species):
        # Initialize
        species_points = []
        base_dir = '/DATA/biotaphy/data2/genera/'
    
        # Idigbio
        idigbio_points = get_idigbio_points(base_dir, species)
        filtered_points, idigbio_filtered = filter_points(
            idigbio_points, idigbio_flag_filter)
        species_points.extend(filtered_points)
    
        # GBIF
        gbif_points = get_gbif_points(base_dir, species)
        filtered_points, gbif_filtered = filter_points(
            gbif_points, gbif_flag_filter)
    
        # Bounding box
        species_points, bbox_filtered = filter_points(
            species_points, bbox_filter)
    
        # Duplicates
        species_points, dup_filtered = filter_points(
            species_points, unique_filter)
    
        # Locality
        loc_filtered = 0
        locality_filter = get_kew_filter(base_dir, species)
        if locality_filter is not None:
            species_points, loc_filtered = filter_points(
                species_points, locality_filter)
        return (species, species_points, idigbio_filtered, gbif_filtered, bbox_filtered, dup_filtered, loc_filtered)
    return process_species

# .............................................................................
def get_idigbio_points(base_dir, species):
    fn = _get_filename(base_dir, species, '_idigbio.csv')
    if os.path.exists(fn):
        points = []
        with open(fn, 'r') as in_file:
            for line in in_file:
                try:
                    row = line.strip().split(', ')
                    points.append(Point(row[0], float(row[1]), float(row[2]), json.loads(row[3])))
                except Exception as err:
                    print(err)
        return points
    return []

# .............................................................................
def get_kew_filter(base_dir, species):
    fn = _get_filename(base_dir, species, '_powo.json')
    if os.path.exists(fn):
        with open(fn) as json_in:
            species_info = json.load(json_in)
            try:
                return get_tdwg_locality_filter(species_info['distribution']['natives'])
            except Exception as err:
                pass
    return None

# .............................................................................
def main():
    """main method for script."""
    # Get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('species_name')
    args = parser.parse_args()
    # Montane
    #bbox = (-180.0, -56.0, -34.0, 90.0)
    #out_dir = '/DATA/biotaphy/montane_v5/'
    # Africa
    #bbox = (0.0, -40.0, 60.0, 0.0)
    #out_dir = '/DATA/biotaphy/angiosperms_v3/'
    # China
    bbox = (73.67, 18.19, 135.03, 53.46)
    out_dir = '/DATA/biotaphy/china_v1/'
    base_dir = '/DATA/biotaphy/data2/genera/'
    point_csv_filename = os.path.join(out_dir, '{}_points.csv'.format(args.species_name))
    sp_report_filename = os.path.join(out_dir, '{}_report.txt'.format(args.species_name))
    sp_processor = get_process_species_function(base_dir, IDIGBIO_FILTER_FLAGS, GBIF_FILTER_FLAGS, bbox)
    (species, points, idigbio_filtered, gbif_filtered, bbox_filtered, dup_filtered, loc_filtered) = sp_processor(args.species_name)
    with open(point_csv_filename, 'w') as out_file:
        for pt in points:
            out_file.write('{}, {}, {}\n'.format(species, pt.x, pt.y))

    with open(sp_report_filename, 'w') as out_file:
        out_file.write('{}, {}, {}, {}, {}\n'.format(idigbio_filtered, gbif_filtered, bbox_filtered, dup_filtered, loc_filtered))


# .............................................................................
if __name__ == '__main__':
    main()

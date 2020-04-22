"""Create a csv file"""
from collections import namedtuple
import csv
import json
import os
import time

from data_preparation.filters import (
    get_bounding_box_filter, get_data_flag_filter,get_tdwg_locality_filter,
    get_unique_localities_filter)
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

MAX_WORKERS = 7
#   1 - 0.148563078
#   2 - 0.352552332
#   5 - 0.461907618
#   7 - 0.473991998
#   8 - 0.441400304
#  10 - 0.372372372
#  30 - 0.118292683 percent per second
#  60 - 0.008074534 percent per second
# 100 - 0.003186275 percent per second

# .............................................................................
"""
Get species list
Create "global" filters
Start occurrence file
For each species
    Get filters
    For each filter
        Filter points
        Log filtered points
    If enough points
        Write points to csv
"""
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
def main(base_dir, out_filename, species_filename, min_points, bbox=None, use_powo=True,
         remove_duplicates=True, idigbio_flags=None, gbif_flags=None):
    """Main method for script"""
    # Get species names
    print('Get species names')
    start_time = time.time()
    species_names = get_species_list_from_file(species_filename)
    report_filename = '{}.report'.format(out_filename)
    process_species = get_process_species_function(base_dir, idigbio_flags, gbif_flags, bbox)
    with open(out_filename, 'w') as out_file:
        with open(report_filename, 'w') as report_file:
            i = 0
            percent = 0
            ten_percent = int(len(species_names) / 10)
            one_percent = int(len(species_names) / 100)
            one_tenth_percent = int(len(species_names) / 1000)
            
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                for result in executor.map(process_species, species_names):
                    (sp_name, sp_points, idigbio_filtered, gbif_filtered,
                     bbox_filtered, dup_filtered, locality_filtered) = result
                    # print('Species: {}'.format(sp_name))
                    report_file.write('{}, {}, {}, {}, {}, {}\n'.format(
                        sp_name, idigbio_filtered, gbif_filtered,
                        bbox_filtered, dup_filtered, locality_filtered))
            
                    # If enough points leftover...
                    if len(sp_points) >= min_points:
                        for point in sp_points:
                            out_file.write(
                                '{}, {}, {}\n'.format(
                                    point.species_name, point.x, point.y))
                    i += 1
                    #if i % one_percent == 0:
                    #    percent += 1
                    #    print('{}%, {} seconds'.format(percent, time.time() - start_time))
                    if i % one_tenth_percent == 0:
                        percent += .1
                        print('{}%, {} seconds'.format(percent, time.time() - start_time))

# .............................................................................
if __name__ == '__main__':
    main(
        '/DATA/biotaphy/data2/genera/',
        '/DATA/biotaphy/montane_v5_2.csv',
        '/DATA/biotaphy/seed_plants/accepted_species.csv', 12,
        bbox=(-180.0, -56.0, -34.0, 90.0), use_powo=True,
        remove_duplicates=True, idigbio_flags=IDIGBIO_FILTER_FLAGS,
        gbif_flags=GBIF_FILTER_FLAGS)

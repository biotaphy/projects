"""Create a csv file"""
from collections import namedtuple
import csv
import json
import os
import time

from tools.data_preparation.filters import (
    get_bounding_box_filter, get_data_flag_filter, get_tdwg_locality_filter,
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
    def process_species_2(species):
        # Initialize
        species_points = []
        base_dir = '/DATA/biotaphy/out3/'
    
        # Initial number of points
        # Num filtered out
        #  Num filtered from gbif
        #  Num filtered from idigbio
        # Num filtered by bbox
        # Num filtered by duplicates
        # Num filtered by localities
    
        # Initial number of points
        initial_num_points = 0
    
        # Idigbio
        idigbio_points = get_idigbio_points(base_dir, species)
        initial_num_points += len(idigbio_points)
        filtered_points, idigbio_filtered = filter_points(
            idigbio_points, idigbio_flag_filter)
        species_points.extend(filtered_points)
    
        # GBIF
        gbif_points = get_gbif_points(base_dir, species)
        initial_num_points += len(gbif_points)
        filtered_points, gbif_filtered = filter_points(
            gbif_points, gbif_flag_filter)
        species_points.extend(filtered_points)
    
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
        return (
            species, species_points, initial_num_points, gbif_filtered,
            idigbio_filtered, bbox_filtered, dup_filtered, loc_filtered)
    return process_species_2

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
    
    total_points = 0
    total_gbif_filtered = 0
    total_idigbio_filtered = 0
    total_bbox_filtered = 0
    total_duplicate_filtered = 0
    total_locality_filtered = 0

    removed_initial = 0
    removed_flags = 0
    removed_bbox = 0
    removed_duplicates = 0
    removed_locality = 0
    
    
    
    with open(out_filename, 'w') as out_file:
        i = 0
        valid_sp = 0
        percent = 0
        ten_percent = int(len(species_names) / 10)
        one_percent = int(len(species_names) / 100)
        one_tenth_percent = int(len(species_names) / 1000)
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for result in executor.map(process_species, species_names):

                (sp_name, sp_points, initial_points, gbif_filtered,
                 idigbio_filtered, bbox_filtered, dup_filtered,
                 locality_filtered) = result
                
                # Add counts to totals
                total_points += initial_points
                total_gbif_filtered += gbif_filtered
                total_idigbio_filtered += idigbio_filtered
                total_bbox_filtered += bbox_filtered
                total_duplicate_filtered += dup_filtered
                total_locality_filtered += locality_filtered
                
        
                # If enough points leftover...
                if len(sp_points) >= min_points:
                    valid_sp += 1
                    for point in sp_points:
                        out_file.write(
                            '{}, {}, {}\n'.format(
                                point.species_name, point.x, point.y))
                else:
                    # What removed this species?
                    t = initial_points
                    if t < min_points:
                        removed_initial += 1
                    else:
                        t -= gbif_filtered
                        t -= idigbio_filtered
                        if t < min_points:
                            removed_flags += 1
                        else:
                            t -= bbox_filtered
                            if t < min_points:
                                removed_bbox += 1
                            else:
                                t -= dup_filtered
                                if t < min_points:
                                    removed_duplicates += 1
                                else:
                                    removed_locality += 1
                i += 1
                #if i % one_percent == 0:
                #    percent += 1
                #    print('{}%, {} seconds'.format(percent, time.time() - start_time))
                if i % one_tenth_percent == 0:
                    percent += .1
                    print('{}%, {} seconds'.format(percent, time.time() - start_time))
    # Print results of filters
    print('')
    print('Total number of points: {}'.format(total_points))
    print('Total number of points filtered by GBIF flags: {}'.format(total_gbif_filtered))
    print('Total number of points filtered by iDigBio flags: {}'.format(total_idigbio_filtered))
    print('Total number of points filtered by bounding box: {}'.format(total_bbox_filtered))
    print('Total number of points filtered by duplicates: {}'.format(total_duplicate_filtered))
    print('Total number of points filtered by locality: {}'.format(total_locality_filtered))
    print('')
    print('Total number of species: {}'.format(i))
    print('Number of species removed by not having enough point to start: {}'.format(removed_initial))
    print('Number of species removed by flags: {}'.format(removed_flags))
    print('Number of species removed by bounding box: {}'.format(removed_bbox))
    print('Number of species removed by duplicates: {}'.format(removed_duplicates))
    print('Number of species removed by locality: {}'.format(removed_locality))
    print('')
    print('Number of species remaining: {}'.format(valid_sp))
    

# .............................................................................
if __name__ == '__main__':
    # Montane
    main(
        '/DATA/biotaphy/out3/',
        '/DATA/biotaphy/montane_v7.csv',
        '/DATA/biotaphy/seed_plants/accepted_species.csv', 12,
        bbox=(-180.0, -56.0, -34.0, 90.0), use_powo=True,
        remove_duplicates=True, idigbio_flags=IDIGBIO_FILTER_FLAGS,
        gbif_flags=GBIF_FILTER_FLAGS)

    # Australia
    #main(
    #    '/DATA/biotaphy/out3/',
    #    '/DATA/biotaphy/australia_v1.csv',
    #    '/DATA/biotaphy/seed_plants/accepted_species.csv', 12,
    #    bbox=(112.0, -44.0, 154.0, -10.0), use_powo=True,
    #    remove_duplicates=True, idigbio_flags=IDIGBIO_FILTER_FLAGS,
    #    gbif_flags=GBIF_FILTER_FLAGS)

    # China
    #main(
    #    '/DATA/biotaphy/out3/',
    #    '/DATA/biotaphy/china_v2.csv',
    #    '/DATA/biotaphy/seed_plants/accepted_species.csv', 12,
    #    bbox=(73.66, 18.21, 135.05, 53.47), use_powo=True,
    #    remove_duplicates=True, idigbio_flags=IDIGBIO_FILTER_FLAGS,
    #    gbif_flags=GBIF_FILTER_FLAGS)

    # South America
    #main(
    #    '/DATA/biotaphy/out3/',
    #    '/DATA/biotaphy/south_america_v1.csv',
    #    '/DATA/biotaphy/seed_plants/accepted_species.csv', 12,
    #    bbox=(-82.0, -32.0, 0.0, 33.0), use_powo=True,
    #    remove_duplicates=True, idigbio_flags=IDIGBIO_FILTER_FLAGS,
    #    gbif_flags=GBIF_FILTER_FLAGS)

    # Africa
    #main(
    #    '/DATA/biotaphy/out3/',
    #    '/DATA/biotaphy/africa_v4.csv',
    #    '/DATA/biotaphy/seed_plants/accepted_species.csv', 12,
    #    bbox=(0.0, -40.0, 60.0, 0.0), use_powo=True,
    #    remove_duplicates=True, idigbio_flags=IDIGBIO_FILTER_FLAGS,
    #    gbif_flags=GBIF_FILTER_FLAGS)


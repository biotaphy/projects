"""Create a csv file"""
import argparse
import csv
import json
import os
import time

from concurrent.futures import ThreadPoolExecutor
from osgeo import ogr

from lmpy import Point
from lmpy.data_preparation.occurrence_filters import (
    get_bounding_box_filter, get_data_flag_filter,
    get_unique_localities_filter)
from lmpy.spatial import SpatialIndex


MAX_WORKERS = 7

# .............................................................................
GBIF_FILTER_FLAGS = [
    'TAXON_MATCH_FUZZY', 'TAXON_MATCH_HIGHERRANK', 'TAXON_MATCH_NONE']
IDIGBIO_FILTER_FLAGS = [
    'geopoint_datum_missing', 'geopoint_bounds', 'geopoint_datum_error',
    'geopoint_similar_coord', 'rev_geocode_mismatch', 'rev_geocode_failure',
    'geopoint_0_coord', 'taxon_match_failed', 'dwc_kingdom_suspect',
    'dwc_taxonrank_invalid', 'dwc_taxonrank_removed']


# .............................................................................
def _get_tdwg_level_shapefile(level, wgsrpd_dir):
    return os.path.join(
        wgsrpd_dir, 'level{}'.format(level), 'level{}.shp'.format(level))


# .............................................................................
def get_geometry_for_tdwg_feature(level, code, feat_id, wgsrpd_dir):
    """Get a geometry for a TDWG feature."""
    # Get the shapefile
    geometries = []
    level_shapefile = _get_tdwg_level_shapefile(level, wgsrpd_dir)
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataset = driver.Open(level_shapefile, 0)
    layer = dataset.GetLayer()
    layer.SetAttributeFilter("LEVEL{}_COD = '{}'".format(level, code))
    for feature in layer:
        geometries.append(feature.GetGeometryRef().ExportToWkt())
    return geometries


# .............................................................................
def get_spatial_index_filter(geometries):
    """Get a spatial index filter."""
    spatial_index = SpatialIndex()
    for i, geom in enumerate(geometries):
        spatial_index.add_feature(i, geom, i)

    def spatial_index_filter(point):
        return bool(spatial_index.search(point.x, point.y))
    return spatial_index_filter


# .............................................................................
def get_tdwg_locality_filter(locality_dicts_list, wgsrpd_dir='./'):
    """Get a filter function that only allows points within the localities.

    Args:
        locality_dicts_list (list of dict): A list of dictionaries representing
            TDWG localities.

    Returns:
        function - A function that takes a point as input and returns a boolean
            output indicating if the point is valid according to this filter.

    Example dictionary:
        {
            "establishment": "Native",
            "featureId": "127",
            "tdwgCode": "GUY",
            "tdwgLevel": 3,
            "name": "Guyana"
        }

    """
    # Get geometries
    geometries = []
    for locality_dict in locality_dicts_list:
        tdwg_code = locality_dict['tdwgCode']
        tdwg_level = locality_dict['tdwgLevel']
        feat_id = locality_dict['featureId']
        geometries.extend(
            get_geometry_for_tdwg_feature(
                tdwg_level, tdwg_code, feat_id, wgsrpd_dir))
    return get_spatial_index_filter(geometries)


# .............................................................................
def get_points_from_csv(csv_filename):
    """Load points from a csv"""
    with open(csv_filename, 'r') as in_file:
        reader = csv.reader(in_file)
        points = [
            Point(row[0], row[1], row[2], json.loads(row[3])
                  ) for row in reader]
        reader.close()
    return points


# .............................................................................
def get_species_list_from_file(filename):
    """Get a list of species names from a file."""
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
    """Filter points using the provided function."""
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
    return os.path.join(
        base_dir, genus, '{}{}'.format(species, service_suffix))


# .............................................................................
def get_gbif_points(base_dir, species):
    """Get GBIF points."""
    fn = _get_filename(base_dir, species, '_gbif.csv')
    if os.path.exists(fn):
        points = []
        with open(fn, 'r') as in_file:
            for line in in_file:
                try:
                    row = line.strip().split(', ')
                    points.append(
                        Point(
                            row[0], float(row[1]), float(row[2]),
                            json.loads(row[3].replace(',', ''
                                                      ).replace(';', ','))))
                except Exception as err:
                    print(err)
                    raise err
        return points
    return []


# .............................................................................
def get_process_species_function(base_dir, idigbio_flags, gbif_flags, bbox,
                                 wgsrpd_dir):
    """Get a function to process a species."""
    idigbio_flag_filter = get_data_flag_filter(idigbio_flags)
    gbif_flag_filter = get_data_flag_filter(gbif_flags)
    bbox_filter = get_bounding_box_filter(*bbox)
    unique_filter = get_unique_localities_filter()

    def process_species(species):
        # Initialize
        species_points = []

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
        locality_filter = get_kew_filter(base_dir, species, wgsrpd_dir)
        if locality_filter is not None:
            species_points, loc_filtered = filter_points(
                species_points, locality_filter)
        return (
            species, species_points, initial_num_points, gbif_filtered,
            idigbio_filtered, bbox_filtered, dup_filtered, loc_filtered)
    return process_species


# .............................................................................
def get_idigbio_points(base_dir, species):
    """Get iDigBio points."""
    fn = _get_filename(base_dir, species, '_idigbio.csv')
    if os.path.exists(fn):
        points = []
        with open(fn, 'r') as in_file:
            for line in in_file:
                try:
                    row = line.strip().split(', ')
                    points.append(
                        Point(
                            row[0], float(row[1]), float(row[2]),
                            json.loads(row[3])))
                except Exception as err:
                    print(err)
        return points
    return []


# .............................................................................
def get_kew_filter(base_dir, species, wgsrpd_dir):
    """Get a filter for KEW POWO expert opinion"""
    fn = _get_filename(base_dir, species, '_powo.json')
    if os.path.exists(fn):
        with open(fn) as json_in:
            species_info = json.load(json_in)
            try:
                return get_tdwg_locality_filter(
                    species_info['distribution']['natives'],
                    wgsrpd_dir=wgsrpd_dir)
            except Exception as err:
                print(err)
                
    return None


# .............................................................................
def main(base_dir, out_filename, species_filename, min_points, bbox=None,
         use_powo=True, remove_duplicates=True, idigbio_flags=None,
         gbif_flags=None, wgsrpd_dir=None):
    """Main method for script"""
    # Get species names
    print('Get species names')
    start_time = time.time()
    species_names = get_species_list_from_file(species_filename)
    process_species = get_process_species_function(
        base_dir, idigbio_flags, gbif_flags, bbox, wgsrpd_dir)

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
                if i % one_tenth_percent == 0:
                    percent += .1
                    print('{}%, {} seconds'.format(
                        percent, time.time() - start_time))
    # Print results of filters
    print('')
    print('Total number of points: {}'.format(total_points))
    print('Total number of points filtered by GBIF flags: {}'.format(
        total_gbif_filtered))
    print('Total number of points filtered by iDigBio flags: {}'.format(
        total_idigbio_filtered))
    print('Total number of points filtered by bounding box: {}'.format(
        total_bbox_filtered))
    print('Total number of points filtered by duplicates: {}'.format(
        total_duplicate_filtered))
    print('Total number of points filtered by locality: {}'.format(
        total_locality_filtered))
    print('')
    print('Total number of species: {}'.format(i))
    print('Species without enough points to begin with: {}'.format(
            removed_initial))
    print('Number of species removed by flags: {}'.format(removed_flags))
    print('Number of species removed by bounding box: {}'.format(removed_bbox))
    print('Number of species removed by duplicates: {}'.format(
        removed_duplicates))
    print('Number of species removed by locality: {}'.format(removed_locality))
    print('')
    print('Number of species remaining: {}'.format(valid_sp))


# .............................................................................
def init():
    """Initialize."""
    parser = argparse.ArgumentParser()
    parser.add_argument('base_dir', type=str, help='Base data directory')
    parser.add_argument(
        'out_csv_filename', type=str,
        help='File location to write CSV points.')
    parser.add_argument(
        'accepted_taxa_filename', type=str,
        help='File location containing accepted taxon names.')
    parser.add_argument(
        'minimum_number_of_points', type=int,
        help='Minimum number of points required to keep a species in output.')
    parser.add_argument('min_x', type=float, help='Minimum x value for bbox')
    parser.add_argument('min_y', type=float, help='Minimum y value for bbox')
    parser.add_argument('max_x', type=float, help='Maximum x value for bbox')
    parser.add_argument('max_y', type=float, help='Maximum y value for bbox')
    parser.add_argument(
        'wgsrpd_base_dir', type=str,
        help='Base directory for WGSRPD shapefiles.')
    args = parser.parse_args()

    main(
        args.base_dir, args.out_csv_filename, args.accepted_taxa_filename,
        args.minimum_number_of_points,
        bbox=(args.min_x, args.min_y, args.max_x, args.max_y),
        use_powo=True, remove_duplicates=True,
        idigbio_flags=IDIGBIO_FILTER_FLAGS, gbif_flags=GBIF_FILTER_FLAGS,
        wgsrpd_dir=args.wgsrpd_base_dir)


# .............................................................................
if __name__ == '__main__':
    init()

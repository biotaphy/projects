"""Create a GeoJSON file with encoded layer data and PAM statistics."""
import argparse
import json

import numpy as np
from osgeo import ogr

from lmpy import Matrix, TreeWrapper
from lmpy.data_preparation.layer_encoder import LayerEncoder

from biotaphy.analyses.pam_stats.site_statistics import (
    calculate_tree_site_statistics)


# .............................................................................
def encode_environment_layers(shapegrid_filename, layers):
    """Encode the layers using the shapegrid."""
    encoder = LayerEncoder(shapegrid_filename)
    for layer_filename, column_name in layers:
        encoder.encode_mean_value(layer_filename, column_name)
    return encoder.get_encoded_matrix()


# .............................................................................
def join_encoded_layers_and_pam_stats(encoded_layers, pam_stats):
    """Concatenate encoded layers and pam statistics.

    Note:
        The PAM statistics, very likely, represent a subset of cells that are
        in the shapegrid and therefore must be "inflated" to match the same
        sites.
    """
    row_headers = encoded_layers.get_row_headers()

    new_stats_mtx = Matrix(
        np.zeros((len(row_headers), len(pam_stats.get_column_headers()))),
        headers={'0': row_headers, '1': pam_stats.get_column_headers()})

    # Set values in new stats matrix
    # Note: This is somewhat fragile.  It requires that encoded_layers row site
    #    ids be a superset of pam_stats row site ids.  Consider either forcing
    #    the data to match or something more robust for a more official version
    all_site_ids = np.array(
        [int(site_id) for site_id, _, _ in encoded_layers.get_row_headers()])
    ps_site_ids = np.array(
        [int(site_id) for site_id, _, _ in pam_stats.get_row_headers()])
    data_idxs = np.take(all_site_ids, ps_site_ids)
    for i in range(len(data_idxs)):
        new_stats_mtx[data_idxs[i]] = pam_stats[i]

    # Concatenate and return
    joined_mtx = Matrix.concatenate([encoded_layers, new_stats_mtx], axis=1)
    return joined_mtx


# .............................................................................
def create_geojson(shapegrid_filename, matrix):
    """Create GeoJSON from a matrix."""
    ret = {
        'type': 'FeatureCollection'
    }
    features = []

    column_headers = matrix.get_column_headers()

    column_enum = [(j, str(k)) for j, k in enumerate(column_headers)]

    shapegrid_dataset = ogr.Open(shapegrid_filename)
    shapegrid_layer = shapegrid_dataset.GetLayer()

    i = 0
    feat = shapegrid_layer.GetNextFeature()
    while feat is not None:
        ft_json = json.loads(feat.ExportToJson())
        # right_hand_rule(ft_json['geometry']['coordinates'])
        # TODO(CJ): Remove this if updated library adds first id correctly
        ft_json['id'] = feat.GetFID()
        props = {}
        for j, k in column_enum:
            val = matrix[i, j].item()
            if val > -9998 and float(val) != 0.0:
                props[k] = val
        ft_json['properties'] = props
        features.append(ft_json)
        i += 1
        feat = shapegrid_layer.GetNextFeature()

    ret['features'] = features
    shapegrid_dataset = shapegrid_layer = None
    return ret


# .............................................................................
def main():
    """Main method for script."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--out_stats_matrix_filename', type=str,
        help='Location to write statistics matrix.')
    parser.add_argument(
        'shapegrid_filename', type=str,
        help='File location of the shapegrid shapefile')
    parser.add_argument(
        'pam_filename', type=str,
        help='File location of the PAM matrix for statistics')
    parser.add_argument(
        'tree_filename', type=str,
        help='File location of the tree to use for statistics')
    parser.add_argument(
        'tree_schema', choices=['newick', 'nexus'], help='The tree schema')
    parser.add_argument(
        'out_geojson_filename', type=str,
        help='File location to write the output GeoJSON')
    parser.add_argument(
        'out_csv_filename', type=str,
        help='File location to write the output CSV')
    parser.add_argument(
        'out_matrix_filename', type=str,
        help='File location to write the output matrix')
    parser.add_argument(
        '--layer', nargs=2, action='append',
        help='File location of a layer followed by a label')
    args = parser.parse_args()

    # Load data
    pam = Matrix.load(args.pam_filename)
    tree = TreeWrapper.get(path=args.tree_filename, schema=args.tree_schema)

    # Encode layers
    encoded_layers = encode_environment_layers(
        args.shapegrid_filename, args.layer)
    # Calculate PAM statistics
    stats_mtx = calculate_tree_site_statistics(pam, tree)
    if args.out_stats_matrix_filename:
        stats_mtx.write(args.out_stats_matrix_filename)
    # Join encoded layers and PAM statistics
    mtx = join_encoded_layers_and_pam_stats(encoded_layers, stats_mtx)
    # Generate GeoJSON
    geojson_data = create_geojson(args.shapegrid_filename, mtx)
    # Write GeoJSON
    with open(args.out_geojson_filename, 'w') as out_file:
        json.dump(geojson_data, out_file, indent=4)

    # Write matrix data
    new_rh = []
    res = 0.5
    for _, x, y in mtx.get_row_headers():
        min_x = x - res
        max_x = x + res
        min_y = y - res
        max_y = y + res
        new_rh.append(
            '"POLYGON (({} {},{} {},{} {},{} {},{} {}))"'.format(
                min_x, max_y, max_x, max_y, max_x, min_y, min_x, min_y, min_x,
                max_y))
    mtx.write(args.out_matrix_filename)
    mtx.set_row_headers(new_rh)
    with open(args.out_csv_filename, 'w') as out_file:
        mtx.write_csv(out_file)


# .............................................................................
if __name__ == '__main__':
    main()

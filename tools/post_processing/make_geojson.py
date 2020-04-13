"""Make a GeoJSON file from a matrix"""
import json
import numpy as np

from lmpy import Matrix

# .............................................................................
def get_polygon_coordinates(x, y, x_res, y_res):
    min_x = x - x_res
    min_y = y - y_res
    max_x = x + x_res
    max_y = y + y_res
    coords = '[ [{0}, {1}], [{2}, {1}], [{2}, {3}], [{0}, {3}], [{0}, {1}] ]'.format(min_x, min_y, max_x, max_y)
    return coords


# .............................................................................
def main():
    tree_mtx_fn = 'C:/Users/cj/Desktop/ryan_v3/tree_mtx.lmm'
    out_geojson_fn = 'C:/Users/cj/Desktop/ryan_v3/tree_geo.json'
    # Read matrix
    with open(tree_mtx_fn, 'rb') as in_file:
        tree_mtx = Matrix.load_flo(in_file)

    stats = tree_mtx.get_column_headers()
    row_headers = tree_mtx.get_row_headers()
    # Open out file
    with open(out_geojson_fn, 'w') as out_file:
        # Write head line
        out_file.write("""\
{
    "type": "FeatureCollection",
    "features": [
""")
        # Loop through rows
        for idx in range(tree_mtx.shape[0]):
            if not np.isclose(tree_mtx[idx].max(), 0.0):
                # Write feature
                id_, x, y = row_headers[idx]
                coords = get_polygon_coordinates(x, y, .25, .25)
                out_file.write("""\
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
""")
                out_file.write("""
                    {}
""".format(coords))
                out_file.write("""
                ]
            },
            "properties": {
""")
                tmp = []
                for i, stat_name in enumerate(stats):
                    tmp.append('                "{}": {}'.format(
                        stat_name, tree_mtx[idx, i]))
                out_file.write(',\n'.join(tmp))
                out_file.write("""\
            }
        },
""")

        # Write end of list
        out_file.write("""\
    ]
}""")
    with open(out_geojson_fn) as in_file:
        json.load(in_file)


# .............................................................................
if __name__ == '__main__':
    main()

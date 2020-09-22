"""Build a spatial index for searching"""
import argparse

from osgeo import ogr

from lmpy.spatial import SpatialIndex


# ............................................................................
def build_index(base_index_filename, shapefiles):
    """Build a spatial index and save to files.

    Args:
        base_index_filename (str): Base file location for index files.
        shapefiles (list of str): A list of shapefile filenames to use for
            index.
    """
    index = SpatialIndex(base_index_filename)
    # Loop through shapefiles and add features
    i = 0
    for shapefile_filename in shapefiles:
        driver = ogr.GetDriverByName("ESRI Shapefile")
        dataset = driver.Open(shapefile_filename, 0)
        layer = dataset.GetLayer()
        lyr_def = layer.GetLayerDefn()
        fields = [
            lyr_def.GetFieldDefn(i).GetName() for i in range(
                lyr_def.GetFieldCount())]
        for feature in layer:
            # Get attributes
            feat_atts = {fld: feature.GetField(fld) for fld in fields}
            # Index
            index.add_feature(i, feature.geometry(), feat_atts)
            i += 1
        layer = dataset = None
    index.save()


# ............................................................................
def main():
    """Main method for script."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'base_filename', type=str, help='Base filename for index data files')
    parser.add_argument(
        'shapefile', type=str, nargs='+',
        help='Shapefile to add to index')
    args = parser.parse_args()
    build_index(args.base_filename, args.shapefile)


# ............................................................................
if __name__ == '__main__':
    main()


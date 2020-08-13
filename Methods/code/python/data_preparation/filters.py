"""Module containing various filtering functions.

Todo:
    * Handle missing keys (for flags)
"""
import os
from osgeo import ogr
from .spatial_index import SpatialIndex

WGSRPD_BASE_DIR = '/home/cjgrady/git/wgsrpd'

# .............................................................................
def get_bounding_box_filter(min_x, min_y, max_x, max_y):
    """Get a filter function for the specified bounding box.

    Args:
        x_index (str or int): The index of the 'x' value for each point.
        y_index (str or int): The index of the 'y' value for each point.
        min_x (numeric): The minimum 'x' value for the bounding box.
        min_y (numeric): The minimum 'y' value for the bounding box.
        max_x (numeric): The maximum 'x' value for the bounding box.
        max_y (numeric): The maximum 'y' value for the bounding box.

    Returns:
        function - A function that takes a point as input and returns a boolean
            output indicating if the point is valid according to this filter.
    """
    # .......................
    def bounding_box_filter(point):
        """Bounding box filter function."""
        return (min_x <= point.x <= max_x and
                min_y <= point.y <= max_y)
    return bounding_box_filter


# .............................................................................
def get_data_flag_filter(filter_flags):
    """Get a filter function for the specified flags.

    Args:
        flag_field_index (str or int): The index of the flag field for each
            point.
        filter_flags (list): A list of flag values that should be considered to
            be invalid.

    Returns:
        function - A function that takes a point as input and returns a boolean
            output indicating if the point is valid according to this filter.
    """
    # .......................
    def flag_filter(point):
        """Data flag filter function."""
        test_flags = point.flags
        if not isinstance(test_flags, (list, tuple)):
            test_flags = [test_flags]
        return not any([flag in filter_flags for flag in test_flags])
    return flag_filter


# .............................................................................
def get_intersect_geometries_filter(geometry_wkts):
    """Get a filter function for intersecting the provided shapefiles.

    Args:
        geometries (list of ogr.Geometry): A list of geometries to check for
            intersection.

    Returns:
        function - A function that takes a point as input and returns a boolean
            output indicating if the point is valid according to this filter.
    """
    geometries = []
    for wkt in geometry_wkts:
        geometries.append(ogr.CreateGeometryFromWkt(wkt))
    # .......................
    def intersect_geometry_filter(point):
        """Intersect geometry filter function."""
        point_geometry = ogr.Geometry(ogr.wkbPoint)
        point_geometry.AddPoint(point.x, point.y)
        for geom in geometries:
            tmp = geom.Intersection(point_geometry).IsEmpty()
        return any([not geom.Intersection(point_geometry).IsEmpty() for geom in geometries])
    return intersect_geometry_filter



# .............................................................................
def get_unique_localities_filter():
    """Get a filter function that only allows unique (x, y) values.

    Returns:
        function - A function that takes a point as input and returns a boolean
            output indicating if the point is valid according to this filter.
    """
    unique_values = []
    # .......................
    def unique_localities_filter(point):
        """Unique localities filter function."""
        test_val = (point.x, point.y)
        if test_val in unique_values:
            return False
        unique_values.append(test_val)
        return True
    return unique_localities_filter


# .............................................................................
def get_tdwg_locality_filter_old(locality_dicts_list):
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
            get_geometry_for_tdwg_feature(tdwg_level, tdwg_code, feat_id))
    return get_intersect_geometries_filter(geometries)


# .............................................................................
def get_tdwg_locality_filter(locality_dicts_list):
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
            get_geometry_for_tdwg_feature(tdwg_level, tdwg_code, feat_id))
    return get_spatial_index_filter(geometries)


# .............................................................................
def get_spatial_index_filter(geometries):
    spatial_index = SpatialIndex()
    for i, geom in enumerate(geometries):
        spatial_index.add_feature(i, geom, i)
    def spatial_index_filter(point):
        return bool(spatial_index.search(point.x, point.y))
    return spatial_index_filter


# .............................................................................
def _get_tdwg_level_shapefile(level):
    return os.path.join(
        WGSRPD_BASE_DIR, 'level{}'.format(level), 'level{}.shp'.format(level))

# .............................................................................
def get_geometry_for_tdwg_feature(level, code, feat_id):
    # Get the shapefile
    geometries = []
    level_shapefile = _get_tdwg_level_shapefile(level)
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataset = driver.Open(level_shapefile, 0)
    layer = dataset.GetLayer()
    layer.SetAttributeFilter("LEVEL{}_COD = '{}'".format(level, code))
    for feature in layer:
        geometries.append(feature.GetGeometryRef().ExportToWkt())
    return geometries

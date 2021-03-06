"""Module containing a class for working with a spatial index.

Version 1: Store geometries in memory in table.  Save as wkt.
"""
from osgeo import ogr
import rtree

# .............................................................................
def create_geometry_from_bbox(min_x, min_y, max_x, max_y):
    """Create a geometry from a bounding box."""
    wkt = 'POLYGON (({0} {1}, {0} {3}, {2} {3}, {2} {1}, {0} {1}))'.format(
        min_x, min_y, max_x, max_y)
    return ogr.CreateGeometryFromWkt(wkt)


# .............................................................................
def quadtree_index(geom, bbox, min_size, depth_left):
    """Use a quadtree approach to gather spatial index data."""
    # min_x, min_y, max_x, max_y = bbox
    test_geom = create_geometry_from_bbox(*bbox)
    intersection = geom.Intersection(test_geom)
    min_x, max_x, min_y, max_y = intersection.GetEnvelope()
    if min_x == max_x or min_y == max_y:
        return []
    # print('{}, {}, {}'.format(depth_left, intersection.Area(), bbox))
    # if intersection.Equals(test_geom):
    if intersection.Area() < min_size:
        return [(bbox, intersection)]
    if intersection.Area() == test_geom.Area():
        return [(bbox, True)]
    ret = []
    if depth_left > 0:
        half_x = min_x + (max_x - min_x) / 2.0
        half_y = min_y + (max_y - min_y) / 2.0
        # print('Half x: {}, half y: {}'.format(half_x, half_y))
        ret.extend(
            quadtree_index(
                intersection, (min_x, min_y, half_x, half_y), min_size,
                depth_left - 1))
        ret.extend(
            quadtree_index(
                intersection, (half_x, min_y, max_x, half_y), min_size,
                depth_left - 1))
        ret.extend(
            quadtree_index(
                intersection, (half_x, half_y, max_x, max_y), min_size,
                depth_left - 1))
        ret.extend(
            quadtree_index(
                intersection, (min_x, half_y, half_x, max_y), min_size,
                depth_left - 1))
    return ret


# .............................................................................
class SpatialIndex:
    """This class provides an index for quickly performing intersects."""
    # ..........................
    def __init__(self):
        self.index = rtree.index.Index()
        self.att_lookup = {}
        self.geom_lookup = {}
        self.min_size = 0.01
        self.depth_left = 10
        self.next_geom = 0

    # ..........................
    @classmethod
    def load_from_file(cls, filename):
        """Load a stored index."""
        pass

    # ..........................
    def add_feature(self, identifier, geom, att_dict):
        """Add a feature to the index.

        Args:
            identifier: An identifier for this feature in the lookup table
            geom: A geometry to spatially index
            att_dict: A dictionary of attributes to store in the lookup table
        """
        self.att_lookup[identifier] = att_dict
        min_x, max_x, min_y, max_y = geom.GetEnvelope()
        idx_entries = quadtree_index(
            geom, (min_x, min_y, max_x, max_y), self.min_size, self.depth_left)
        for bbox, idx_geom in idx_entries:
            if isinstance(idx_geom, bool) and idx_geom:
                # Index as entire bbox
                self.index.insert(identifier, bbox, obj=True)
            else:
                # Add geometry to lookup, increment counter
                self.index.insert(identifier, bbox, obj=self.next_geom)
                self.geom_lookup[self.next_geom] = idx_geom
                self.next_geom += 1

    # ..........................
    def search(self, x, y):
        """Search for x, y and return attributes in lookup if found."""
        hits = {}
        for hit in self.index.intersection((x, y, x, y), objects=True):
            if hit.id not in hits.keys():
                if isinstance(hit.object, bool) or \
                        self._point_intersect(x, y, self.geom_lookup[hit.object]):
                    hits[hit.id] = self.att_lookup[hit.id]
        return hits

    # ..........................
    @staticmethod
    def _point_intersect(pt_x, pt_y, geom):
        # print('Intersecting geometry!')
        pt_geom = ogr.CreateGeometryFromWkt('POINT ({} {})'.format(pt_x, pt_y))
        return pt_geom.Within(geom)

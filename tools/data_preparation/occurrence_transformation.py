"""This module contains tools for transforming raw occurrence data."""
from collections import namedtuple
import csv
from operator import itemgetter


# .............................................................................
Point = namedtuple('Point', 'species_name, x, y, flags', defaults=[None])


# .............................................................................
def none_getter(obj):
    """Return None as a function."""
    return None


# .............................................................................
def _get_points_for_generator(rec_generator, species_name_getter, x_getter,
                              y_getter, flags_getter):
    """Get a list of Points from a specimen record generator.

    Args:
        rec_generator: A generator function that generates point records.
        species_name_getter: A function for getting species name from a record.
        x_getter: A function for getting the 'x' value from a record.
        y_getter: A function for getting the 'y' value from a record.
        flags_getter: A function for getting the 'flags' value from a record.

    Returns:
        list of Point named tuples
    """
    points = []
    for pt_rec in rec_generator:
        try:
            points.append(
                Point(
                    species_name_getter(pt_rec), x_getter(pt_rec),
                    y_getter(pt_rec), flags_getter(pt_rec)))
        except (IndexError, KeyError):
            print('Could not extract required fields from {}'.format(pt_rec))


# .............................................................................
def convert_delimited_to_point(filename, species_index, x_index, y_index,
                               flags_index=None, delimiter=', ', headers=True):
    """Convert a file of delimited data into points.

    Args:
        filename (str): A path to a file of delimited data.
        species_index (int): The position of the species filed in each record.
        x_index (int): The position of the x field in each record.
        y_index (int): The position of the y field in each record.
        flags_index (int): The position of the flags field in each record.
        delimiter (str): The delimiter of the delimited data.
        headers (bool): Does the file have a header row.

    Returns:
        list of Point named tuples
    """
    if flags_index:
        flag_getter = itemgetter(flags_index)
    else:
        flag_getter = none_getter

    with open(filename) as in_file:
        if headers:
            _ = next(in_file)
        reader = csv.reader(in_file, delimiter=delimiter)
        points = _get_points_for_generator(
            reader, itemgetter(species_index), itemgetter(x_index),
            itemgetter(y_index), flag_getter)
    return points


# .............................................................................
def convert_json_to_point(json_obj, point_iterator=iter, species_name_getter,
                          x_getter, y_getter, flags_getter=none_getter):
    """Get a list of Points from a JSON object.

    Args:
        json_obj (dict or list): A JSON object to get point records from.
        point_iterator: An iterator function to pull records from the JSON
            object.
        species_name_getter: A function for getting species name from a record.
        x_getter: A function for getting the 'x' value from a record.
        y_getter: A function for getting the 'y' value from a record.
        flags_getter: A function for getting the 'flags' value from a record.

    Returns:
        list of Point named tuples
    """
    points = _get_points_for_generator(
        point_iterator(json_obj), species_name_getter, x_getter, y_getter,
        flags_getter)
    return points


# .............................................................................
def convert_gbif_download(filename):
    """Convert a GBIF download to points.

    Args:
        filename (str): The file location of the GBIF download.
    """
    return convert_delimited_to_point(
        filename, species_index, x_index, y_index, flags_index, delimiter,
        headers)


# .............................................................................
def convert_idigbio_download(filename):
    """Convert a iDigBio download to points.

    Args:
        filename (str): The file location of the iDigBio download.
    """
    return convert_delimited_to_point(
        filename, species_index, x_index, y_index, flags_index, delimiter,
        headers)

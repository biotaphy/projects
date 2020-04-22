"""This module contains tools for transforming raw occurrence data."""
from collections import namedtuple
import csv
import json
from operator import itemgetter
import sys

csv.field_size_limit(sys.maxsize)


# .............................................................................
Point = namedtuple('Point', 'species_name, x, y, flags', defaults=[None])


# .............................................................................
def none_getter(obj):
    """Return None as a function."""
    return None

def gbif_flags_getter(flags_idx):
    def getter(obj):
        return obj[flags_idx].split(';')
    return getter

def json_getter(fld_idx):
    def getter(obj):
        if len(obj[fld_idx]) > 1:
            return json.loads(obj[fld_idx])
        else:
            return []
    return getter

def key_getter(fld_idx, get_key):
    def getter(obj):
        return json.loads(obj[fld_idx])[get_key]
    return getter

def species_name_getter(genus_index, species_index):
    def getter(obj):
        return '{} {}'.format(obj[genus_index].capitalize(), obj[species_index])
    return getter

def chain_getter(*args):
    atts = list(args)
    def getter(obj):
        for att in atts:
            obj = itemgetter(att)(obj)
        return obj
    return getter

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
    i = 0
    for pt_rec in rec_generator:
        i += 1
        try:
            sp_parts = species_name_getter(pt_rec).replace('_', ' ').split(' ')
            
            if len(sp_parts) > 1:
                sp_name = '{} {}'.format(sp_parts[0].capitalize(), sp_parts[1]).replace('/', '_')
                points.append(
                    Point(
                        sp_name, x_getter(pt_rec),
                        y_getter(pt_rec), flags_getter(pt_rec)))
                #print(points)
                #raise Exception('cj')
        except (IndexError, KeyError, csv.Error, json.decoder.JSONDecodeError) as err:
            print(err)
            print('Could not extract required fields from {}'.format(pt_rec))
            print(i)
    return points


# .............................................................................
def convert_delimited_to_point(filename, species_getter, x_getter, y_getter,
                               flag_getter=none_getter, delimiter=', ', headers=True):
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
    with open(filename, 'r') as in_file:
        if headers:
            _ = next(in_file)
        reader = csv.reader(in_file, delimiter=delimiter)
        points = _get_points_for_generator(
            reader, species_getter, x_getter, y_getter, flag_getter)
    return points


# .............................................................................
def convert_json_to_point(json_obj, species_name_getter,
                          x_getter, y_getter, point_iterator=iter,
                          flags_getter=none_getter):
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
        filename, itemgetter(9), itemgetter(22), itemgetter(21),
        itemgetter(49), delimiter='\t', headers=True)


# .............................................................................
def convert_idigbio_download(filename):
    """Convert a iDigBio download to points.

    Args:
        filename (str): The file location of the iDigBio download.
    """
    return convert_delimited_to_point(
        filename, species_name_getter(33, 69), key_getter(35, 'lon'),
        key_getter(35, 'lat'),
        flag_getter=json_getter(31), delimiter=',', headers=True)

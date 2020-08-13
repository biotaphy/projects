"""Get the accepted names for a tree"""
import argparse
from copy import deepcopy
from time import sleep
from lmpy import TreeWrapper

from tools.apis.gbif import get_gbif_accepted_name


# .............................................................................
def get_and_replace_names(tree):
    new_tree = deepcopy(tree)
    total_sp = len(new_tree.taxon_namespace)
    i = 0
    for taxon in new_tree.taxon_namespace:
        i += 1
        o_sp_name = taxon.label
        try:
            acc_name, sp_key = get_gbif_accepted_name(o_sp_name)
            if acc_name is not None and o_sp_name != acc_name:
                taxon.label = acc_name
                print('Replaced {} with {} ({} of {})'.format(
                    o_sp_name, acc_name, i, total_sp))
            sleep(.5)
        except KeyError:
            pass
    return new_tree


# .............................................................................
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'in_tree_filename', type=str,
        help='The file location of the input tree')
    parser.add_argument(
        'in_tree_schema', type=str, choices=['newick', 'nexus'],
        help='The schema of the input tree')
    parser.add_argument(
        'out_tree_filename', type=str,
        help='The file location of the output tree')
    parser.add_argument(
        'out_tree_schema', type=str, choices=['newick', 'nexus'],
        help='The schema of the output tree')

    args = parser.parse_args()
    tree = TreeWrapper.get(
        path=args.in_tree_filename, schema=args.in_tree_schema)
    out_tree = get_and_replace_names(tree)
    out_tree.write(path=args.out_tree_filename, schema=args.out_tree_schema)


# .............................................................................
if __name__ == '__main__':
    main()

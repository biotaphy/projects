"""Get GBIF accepted names where possible for the tips in a tree."""
import argparse
from copy import deepcopy
from time import sleep
import urllib

import requests

from lmpy import TreeWrapper


# .............................................................................
def get_gbif_accepted_name(name_str):
    """Get the accepted name for a name string.

    Note:
        If there is an HTTP error, I want it to fail out
    """
    try:
        other_filters = {'name': name_str.strip()}
        url = 'http://api.gbif.org/v1/species/match?{}'.format(
            urllib.parse.urlencode(other_filters))
        response = requests.get(url).json()
        if response['status'].lower() in ('accepted', 'synonym') and \
                'speciesKey' in response.keys():
            return (
                response['canonicalName'], response['speciesKey'],
                response['genus'], response['genusKey'], response['family'],
                response['familyKey'])
    except KeyError:
        pass
    return None


# .............................................................................
def get_and_replace_names(tree):
    """Get GBIF accepted taxon names and replace tip labels in the tree."""
    new_tree = deepcopy(tree)
    total_sp = len(new_tree.taxon_namespace)
    accepted_taxa = set([])
    i = 0
    for taxon in new_tree.taxon_namespace:
        i += 1
        o_sp_name = taxon.label
        try:
            acc_name, _, _, _, _, _ = get_gbif_accepted_name(o_sp_name)
            accepted_taxa.add(acc_name)
            if acc_name is not None and o_sp_name != acc_name:
                taxon.label = acc_name
                print('Replaced {} with {} ({} of {})'.format(
                    o_sp_name, acc_name, i, total_sp))
            sleep(.5)
        except KeyError:
            pass
    return new_tree, accepted_taxa


# .............................................................................
def main():
    """Main method for script."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'in_tree_filename', type=str, help='Path to initial tree')
    parser.add_argument(
        'in_tree_schema', type=str, choices=['nexus', 'newick'],
        help='The input tree schema')
    parser.add_argument('out_tree_filename', type=str, help='Ouput tree path')
    parser.add_argument(
        'out_tree_schema', type=str, choices=['nexus', 'newick'],
        help='The output tree schema')
    parser.add_argument(
        'accepted_taxa_filename', type=str,
        help='File path to write out accepted taxon names')
    args = parser.parse_args()
    tree = TreeWrapper.get(
        path=args.in_tree_filename, schema=args.in_tree_schema)
    out_tree, accepted_taxa = get_and_replace_names(tree)
    # Write tree
    out_tree.write(path=args.out_tree_filename, schema=args.out_tree_schema)
    # Write accepted taxa
    with open(args.accepted_taxa_filename, 'w') as taxa_out_file:
        for taxon_name in accepted_taxa:
            taxa_out_file.write(taxon_name)


# .............................................................................
if __name__ == '__main__':
    main()

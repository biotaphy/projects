"""Subset a tree based on the species in a CSV file"""
import argparse
import os

from lmpy import TreeWrapper


# .............................................................................
def purge_tree(tree_filename, tree_schema, occurrence_filename, species_col):
    """Get a tree and purge taxa not in occurrence data."""
    tree = TreeWrapper.get(path=tree_filename, schema=tree_schema)
    species = set([])
    with open(occurrence_filename, 'r') as in_file:
        for line in in_file:
            parts = line.split(', ')
            sp_name = parts[species_col].strip()
            species.add(sp_name)
    purge_taxa = []
    for taxon in tree.taxon_namespace:
        if not taxon.label in species:
            purge_taxa.append(taxon)
    tree.prune_taxa(purge_taxa)
    tree.purge_taxon_namespace()
    return tree


# .............................................................................
def main():
    """Main method for script."""
    parser = argparse.ArgumentParser()
    parser.add_argument('tree_filename', type=str)
    parser.add_argument('tree_schema', type=str)
    parser.add_argument('occurrence_filename', type=str)
    parser.add_argument('species_column', type=int)
    parser.add_argument('out_tree_filename', type=str)
    parser.add_argument('out_tree_schema', type=str)
    args = parser.parse_args()
    ret_tree = purge_tree(
        args.tree_filename, args.tree_schema, args.occurrence_filename,
        args.species_column)
    ret_tree.write(path=args.out_tree_filename, schema=args.out_tree_schema)


# .............................................................................
if __name__ == '__main__':
    main()

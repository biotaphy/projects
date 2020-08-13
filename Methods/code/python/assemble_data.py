"""Assemble data files together for processing."""
import os
import argparse

from lmpy import TreeWrapper
import shutil

# .............................................................................
def check_and_copy(out_filename, check_filename):
    if not os.path.exists(out_filename):
        if os.path.exists(check_filename):
            shutil.copy(check_filename, out_filename)
    
    return os.path.exists(out_filename)


# .............................................................................
def process_species(species_name, gbif_dir, idigbio_dir, powo_dir, out_dir):
    """Find data files for individual species."""
    (gbif_exists, idigbio_exists, powo_exists) = (False, False, False)

    try:
        # Get out directory, create if necessary
        escaped_species_name = species_name
        genus = species_name.split(' ')[0]
        genus_dir = os.path.join(out_dir, 'genera', genus)
        if not os.path.exists(genus_dir):
            os.mkdir(genus_dir)
        out_gbif_filename = os.path.join(
            genus_dir, '{}_gbif.csv'.format(escaped_species_name))
        out_idigbio_filename = os.path.join(
            genus_dir, '{}_idigbio.csv'.format(escaped_species_name))
        out_powo_filename = os.path.join(
            genus_dir, '{}_powo.json'.format(escaped_species_name))
    
        check_gbif_filename = os.path.join(
            gbif_dir, genus, '{}_gbif.csv'.format(escaped_species_name))
        check_idigbio_filename = os.path.join(
            idigbio_dir, genus, '{}_idigbio.csv'.format(escaped_species_name))
        check_powo_filename = os.path.join(
            powo_dir, genus, escaped_species_name, 'kew.json')
    
        gbif_exists = check_and_copy(out_gbif_filename, check_gbif_filename)
        idigbio_exists = check_and_copy(
            out_idigbio_filename, check_idigbio_filename)
        powo_exists = check_and_copy(out_powo_filename, check_powo_filename)
    except Exception as err:
        print('{}: {}'.format(species_name, err))
    return (gbif_exists, idigbio_exists, powo_exists)



# .............................................................................
def main():
    """Main method for script."""
    parser = argparse.ArgumentParser()
    parser.add_argument('accepted_species_filename')
    #parser.add_argument('tree_filename')
    parser.add_argument('gbif_dir')
    parser.add_argument('idigbio_dir')
    parser.add_argument('powo_dir')
    parser.add_argument('out_dir')
    args = parser.parse_args()

    gbif_fails = []
    idigbio_fails = []
    powo_fails = []
    # Load species
    accepted_species = []
    with open(args.accepted_species_filename) as in_file:
        for line in in_file:
            try:
                parts = line.split(',')
                accepted_species.append(parts[1].strip().strip('"'))
            except Exception as err:
                print(err)
    # Load tree
    #print('Load tree')
    #tree = TreeWrapper.get(path=args.tree_filename, schema='newick')
    print('Processing species')
    # For each species
    #for taxon in tree.taxon_namespace:
    for taxon in accepted_species:
        # Process species
        gbif_exists, idigbio_exists, powo_exists = process_species(
            taxon, args.gbif_dir, args.idigbio_dir, args.powo_dir,
            args.out_dir)
        # Note failures
        if not gbif_exists:
            gbif_fails.append(taxon)
        if not idigbio_exists:
            idigbio_fails.append(taxon)
        if not powo_exists:
            powo_fails.append(taxon)
    # Write out failures
    print('Write failures')
    with open(os.path.join(args.out_dir, 'gbif_failures.txt'),
              'w') as out_file:
        for taxon in gbif_fails:
            out_file.write('{}\n'.format(taxon))
    with open(os.path.join(args.out_dir, 'idigbio_failures.txt'),
              'w') as out_file:
        for taxon in idigbio_fails:
            out_file.write('{}\n'.format(taxon))
    with open(os.path.join(args.out_dir, 'powo_failures.txt'),
              'w') as out_file:
        for taxon in powo_fails:
            out_file.write('{}\n'.format(taxon))

# .............................................................................
if __name__ == '__main__':
    main()

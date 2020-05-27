"""Look through data directory and report missing data."""

import argparse
import os


# .............................................................................
def find_missing_data(accepted_taxa_filename, base_dir):
    """Find and report missing data."""
    num_species = 0
    powo_fails = []
    gbif_fails = []
    idigbio_fails = []
    with open(accepted_taxa_filename) as taxa_file:
        for line in taxa_file:
            num_species += 1
            parts = line.split(', ')
            species_name = parts[1].strip().strip('"')
            sp_key = int(parts[2])
            print(species_name)
            genus_name = species_name.split(' ')[0]
            genus_dir = os.path.join(base_dir, genus_name)
            kew_filename = os.path.join(
                genus_dir, '{}_powo.json'.format(species_name))
            gbif_filename = os.path.join(
                genus_dir, '{}_gbif.csv'.format(species_name))
            idigbio_filename = os.path.join(
                genus_dir, '{}_idigbio.csv'.format(species_name))
            if not os.path.exists(kew_filename):
                powo_fails.append((species_name, sp_key))
            if not os.path.exists(gbif_filename):
                gbif_fails.append((species_name, sp_key))
            if not os.path.exists(idigbio_filename):
                idigbio_fails.append((species_name, sp_key))
            if num_species % 10000 == 0:
                print('Species num: {}'.format(num_species))
    return (num_species, powo_fails, gbif_fails, idigbio_fails)


# .............................................................................
def main():
    """Main method for script"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'accepted_taxa_filename', type=str,
        help='CSV file containing accepted taxon names and taxon keys {original name}, {accepted name}, {taxon key}...')
    parser.add_argument(
        'base_dir', type=str, help='Base directory to inspect for data')
    parser.add_argument(
        'powo_fails_filename', type=str,
        help='File location to store missing powo taxa')
    parser.add_argument(
        'gbif_fails_filename', type=str,
        help='File location to store missing gbif taxa')
    parser.add_argument(
        'idigbio_fails_filename', type=str,
        help='File location to store missing idigbio taxa')
    args = parser.parse_args()
    num_species, powo_fails, gbif_fails, idigbio_fails = find_missing_data(
        args.accepted_taxa_filename, args.base_dir)

    print('POWO: {} failures, {} species'.format(len(powo_fails), num_species))
    with open(args.powo_fails_filename, 'w', encoding='utf8') as powo_out:
        for species_name, sp_key in powo_fails:
            powo_out.write('{}, {}\n'.format(sp_key, species_name))
    print('GBIF: {} failures, {} species'.format(len(gbif_fails), num_species))
    with open(args.gbif_fails_filename, 'w', encoding='utf8') as gbif_out:
        for species_name, sp_key in gbif_fails:
            gbif_out.write('{}, {}\n'.format(sp_key, species_name))
    print('IDIGBIO: {} failures, {} species'.format(len(idigbio_fails), num_species))
    with open(args.idigbio_fails_filename, 'w', encoding='utf8') as idig_out:
        for species_name, sp_key in idigbio_fails:
            idig_out.write('{}, {}\n'.format(sp_key, species_name))


# .............................................................................
if __name__ == '__main__':
    main()

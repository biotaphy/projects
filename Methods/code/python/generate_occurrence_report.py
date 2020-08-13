"""Generate a report of the content of the occurrence data in a directory"""
import argparse
import os
import numpy as np
from lmpy import Matrix

# .............................................................................
def get_report_data(accepted_taxa_filename, base_dir):
    num_accepted_species = 0
    species_report = {}
    # Generate report
    with open(accepted_taxa_filename) as taxa_file:
        for line in taxa_file:
            num_accepted_species += 1
            parts = line.split(', ')
            species_name = parts[1].strip().strip('"')
            sp_key = int(parts[2])
            genus_name = species_name.split(' ')[0]
            genus_dir = os.path.join(base_dir, genus_name)
            kew_filename = os.path.join(
                genus_dir, '{}_powo.json'.format(species_name))
            k_val = -1
            if os.path.exists(kew_filename):
                k_val += 1
                if os.stat(kew_filename).st_size > 5:
                    k_val += 1
            idigbio_filename = os.path.join(
                genus_dir, '{}_idigbio.csv'.format(species_name))
            i_val = -1
            if os.path.exists(idigbio_filename):
                i_val += 1
                if os.stat(idigbio_filename).st_size > 5:
                    i_val += 1
            gbif_filename = os.path.join(
                genus_dir, '{}_gbif.csv'.format(species_name))
            g_val = -1
            if os.path.exists(gbif_filename):
                g_val += 1
                if os.stat(gbif_filename).st_size > 5:
                    g_val += 1
            if sum([k_val, i_val, g_val]) < 3:
                species_report[species_name] = [k_val, i_val, g_val]
    
    # Create a matrix for output
    species_names = []
    report_data = []
    for k in sorted(species_report.keys()):
        species_names.append(k)
        report_data.append(species_report[k])
    species_report_matrix = Matrix(
        np.array(report_data), headers={
            '0': species_names, '1': ['POWO', 'iDigBio', 'GBIF']})
    return num_accepted_species, species_report_matrix


# .............................................................................
def main():
    """Main method for script"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'accepted_taxa_filename', type=str,
        help='CSV file containing accepted taxon names and taxon keys {original name}, {accepted name}, {taxon key}...')
    parser.add_argument(
        'base_dir', type=str, help='Base directory to inspect for data')
    args = parser.parse_args()
    num_accepted, sp_mtx = get_report_data(
        args.accepted_taxa_filename, args.base_dir)
    print('Number of accepted taxa: {}'.format(num_accepted))
    missing = np.where(sp_mtx == -1)[1]
    empty = np.where(sp_mtx == 0)[1]

    print('{} - missing: {}, empty: {}'.format(
        'KEW', len(np.where(missing == 0)[0]), len(np.where(empty == 0)[0])))
    print('{} - missing: {}, empty: {}'.format(
        'iDigBio', len(np.where(missing == 1)[0]), len(np.where(empty == 1)[0])))
    print('{} - missing: {}, empty: {}'.format(
        'GBIF', len(np.where(missing == 2)[0]), len(np.where(empty == 2)[0])))

# .............................................................................
if __name__ == '__main__':
    main()


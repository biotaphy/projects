import os

# .............................................................................
def get_species_filename(species_name, base_dir, service_suffix, file_ext):
    """Get the file name for the species data / service combination.

    Args:
        species_name (str): The name of the species.
        base_dir (str): The base directory to write points.
        service_suffix (str): The service suffix for the data files.
        file_ext (str): The extension for the filename.
    """
    temp = species_name.replace('_', ' ').replace('.', '_').replace('/', '_').split(' ')
    genus = temp[0]
    # TODO: Encode file path as necessary
    if len(temp) == 1:
        escaped_species = genus
    else:
        escaped_species = '{} {}'.format(genus, temp[1])
    genus_dir = os.path.join(base_dir, genus)
    species_filename = os.path.join(
        genus_dir, '{}{}{}'.format(escaped_species, service_suffix, file_ext))
    if not os.path.exists(genus_dir):
        os.mkdir(genus_dir)
    return species_filename


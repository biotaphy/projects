"""This module provides access to plants of the world APIs."""
import pykew.powo as powo
from pykew.powo_terms import Filters, Name


# .............................................................................
def get_species_kew(fq_id):
    """Get the species information from kew"""
    result = powo.lookup(fq_id, include=['distribution'])
    return result


# .............................................................................
def get_kew_ids_for_genus(genus_name):
    """Get ids for kew queries"""
    query = {Name.genus: genus_name}
    results = powo.search(query, filters=Filters.accepted)
    try:
        return {res['name']: res['fqId'] for res in results}
    except Exception as err:
        raise err


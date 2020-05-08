Description
===========

Study Area
==========
Bounding box - 0,-40, 60, 0

Workflow
========
1. Get the accepted taxon names for all tips in the Smith and Brown tree
1. Replace non-accepted tips in tree
1. Download occurrences from iDigBio and GBIF for accepted names
1. Download locality information from Plants of the World Online for accepted names
1. Process points from iDigBio and filter out any with the following flags:
  * geopoint_datum_missing
  * geopoint_bounds
  * geopoint_datum_error
  * geopoint_similar_coord
  * rev_geocode_mismatch
  * rev_geocode_failure
  * geopoint_0_coord
  * taxon_match_failed
  * dwc_kingdom_suspect
  * dwc_taxonrank_invalid
  * dwc_taxonrank_removed
1. Process points from GBIF and filter out any with the following flags:
  * Geospatial issues
  * TAXON_MATCH_FUZZY
  * TAXON_MATCH_HIGHERRANK
  * TAXON_MATCH_NONE
1. Aggregate the remaining points from iDigBio and GBIF filtered sets and group by species
1. Filter points by bounding box
1. Remove any points with duplicate localities
1. Filter points to only those intersecting the geometries specified by POWO for each species
1. For remaining points, remove any species with less than 12 points
1. Assemble occurrence file with the remaining species occurrences
1. Subset tree using remaining species
1. Create a climate dataset subsetted to the study area
1. POST an experiment to Lifemapper using the occurrence data, subsetted tree, climate data, and the following parameters:
   * SDM Algorithm: Open Source AT&T Maxent
   * PAM grid of half degree cells for study area
   * 10% of PAM cell coverage considered presence
1. Run experiment using Lifemapper to generate SDMs and PAM
1. Pull PAM and squidded (connection between PAM labels and tree tips) tree from Lifemapper server
1. Compute statistics using PAM and Tree
1. Create GeoJSON from statistics matrix output


Results
=======
XXXX species after pre-processing occurrence

![Alpha Diversity](https://biotaphy.github.io/projects/images/africa_angiosperms_alpha.png)
![Phylogenetic Diversity](https://biotaphy.github.io/projects/images/africa_angiosperms_pd.png)

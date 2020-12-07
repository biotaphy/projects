Summary of Ocbils project
=========================
Old, climatically buffered, infertile landscapes (Ocbils) have been hypothesized to harbor an elevated number of persistent plant 
lineages and are predicted to occur across different parts of the globe, interspersed with other types of landscapes.  We tested 
whether the mean age of a plant community is associated with occurrence on Ocbils, as predicted by climatic stability and poor 
soil environments. Using digitized occurrence data for seed plants occurring in Australia (15,029 species), sub-Saharanouthern 
Africa (16,802 species), and South America (31,313 species), regions that comprise commonly investigated Ocbils (Southwestern 
Australian Floristic Region, Greater Cape Floristic Region, and campos rupestres), and phylogenies pruned to match the species 
occurrences, we tested for associations between environmental data (current-day climate, soil composition, elevation, and climatic 
stability) and two novel metrics developed here that capture the age of a community (Mean Tip Length and Mean Node Height). Our 
results indicate that plant community ages are influenced by a combination of multiple environmental predictors that vary 
globally; we did not find statistically strong associations between the environments of Ocbil areas and community age, in contrast 
to the prediction for these landscapes. The Cape Floristic Region was the only Ocbil that showeding a significant, although not 
strong, overlap with old communities.  


----


Data Processing
===============

Python requirements:
 - gdal
 - lmpy - https://github.com/lifemapper/lmpy
 - BiotaphyPy - https://github.com/biotaphy/BiotaphyPy

1. Acquire study tree (Smith and Brown 2018)
2. Get accepted taxa names for the tips in the tree (get_accepted_names_for_tree.py)
3. Download data from iDigBio and GBIF
 - iDigBio: https://api.idigbio.org/v2/download/?rq={"scientificname": {"type": "exists"},"kingdom": "Plantae", "geopoint": {"type": "exists"}}&email={fill in email}
 - GBIF (HTTP POST): https://api.gbif.org/v1/occurrence/download/request
   - POST data
```
{
    "creator": "userName",
    "notificationAddresses": [
        "userEmail@example.org"
    ],
    "sendNotification": true,
    "format": "SIMPLE_CSV",
    "predicate": {
        "type": "and",
        "predicates": [
            {
                "type": "equals",
                "key": "BASIS_OF_RECORD",
                "value": "PRESERVED_SPECIMEN"
            },
            {
                "type": "equals",
                "key": "KINGDOM_KEY",
                "value": "6"
            },
            {
                "type": "equals",
                "key": "HAS_COORDINATE",
                "value": "true"
            },
            {
                "type":"equals",
                "key":"HAS_GEOSPATIAL_ISSUE",
                "value":"false"
            }
        ]
    }
}
```
4. Fill in missing data from iDigBio and GBIF and get data from POWO (backfill_missing_data.py)
5. Process GBIF and iDigBio data through filters to fill in accepted taxon name, remove problem data flags, and convert to a common format (process_occurrences.py)
  ```
  $ export WRANGLER_CONFIG_DIR=configuration/data_wranglers
  $ python process_occurrences.py -f $WRANGLER_CONFIG_DIR/decimal_precision_filter.json -f $WRANGLER_CONFIG_DIR/gbif_flag_filter.json -f $WRANGLER_CONFIG_DIR/accepted_taxon_filter.json -f $WRANGLER_CONFIG_DIR/gbif_to_common_map_modifier.json gbif_processed.csv species decimalLongitude decimalLatitude gbif.csv
  $ python process_occurrences.py -f $WRANGLER_CONFIG_DIR/decimal_precision_filter.json -f $WRANGLER_CONFIG_DIR/idigbio_flag_filter.json -f $WRANGLER_CONFIG_DIR/accepted_taxon_filter.json -f $WRANGLER_CONFIG_DIR/idigbio_to_common_map_modifier.json -g idigbio_processed.csv species lon lat idigbio.csv
  ```
6. Split processed files into easier to manage chunks (split_occurrences.py)
  ```
  $ python split_occurrences.py chunks/occurrences_ species x y 2 0 species gbif.csv idigbio.csv
  ```
7. Sort chunks (sort_occurrences.py)
  ```
  $ python sort_occurrences.py chunks/occurrences_aa.csv sorted/occurrences_aa.csv species x y
  $ python sort_occurrences.py chunks/occurrences_ab.csv sorted/occurrences_ab.csv species x y
  ...
  $ python sort_occurrences.py chunks/occurrences_zz.csv sorted/occurrences_zz.csv species x y  
  ```
8. Process sorted chunks into one large file and filter duplicate localities, filter with KEW expert opinion localities, and minimum number of points (process_occurrences.py)
  ```
  $ python process_occurrences.py -f $WRANGLER_CONFIG_DIR/duplicate_locality_filter.json -f $WRANGLER_CONFIG_DIR/kew_locality_filter.json -f $WRANGLER_CONFIG_DIR/minimum_points_filter.json processed_occurrences.csv species x y sorted/occurrences_aa.csv sorted/occurrences_ab.csv ... sorted/occurrences_zz.csv
  ```
9. For each region, process larger occurrence file into regional subset and filter out species without enough points (process_occurrences.py)
  ```
  $ python process_occurrences.py -f $WRANGLER_CONFIG_DIR/africa_bbox_filter.json -f $WRANGLER_CONFIG_DIR/minimum_points_filter.json africa_occurrences.csv species x y processed_occurrences.csv
  $ python process_occurrences.py -f $WRANGLER_CONFIG_DIR/australia_bbox_filter.json -f $WRANGLER_CONFIG_DIR/minimum_points_filter.json australia_occurrences.csv species x y processed_occurrences.csv
  $ python process_occurrences.py -f $WRANGLER_CONFIG_DIR/south_america_bbox_filter.json -f $WRANGLER_CONFIG_DIR/minimum_points_filter.json south_america_occurrences.csv species x y processed_occurrences.csv
  ```
10. POST using Lifemapper / Biotaphy web UI (http://client.lifemapper.org/biotpahy/)
11. Calculate PAM stats, encode environment layers and create GeoJSON (join_env_and_pam_stats.py)
  ```
  $ python join_env_and_pam_stats.py shpgrid_africa.shp africa_pam.lmm tree.nex nexus africa.geojson --layer layers/BIOCLIM_12.tif Bioclim_12 --layer layers/BIOCLIM_17.tif Bioclim_17 --layer layers/BIOCLIM_1.tif Bioclim_1 --layer layers/BIOCLIM_7.tif Bioclim_7 --layer layers/CFR_Cowling2008_wgs84_2.5minute.tif CFR_Cowling --layer layers/GTOPO30_SLOPE_reduced.tif Slope --layer layers/GTOPO30_ELEVATION.tif Elevation --layer layers/ISRICSOILGRIDS_new_average_coarsefragmentpercent_reduced.tif Coarse_fragment --layer layers/ISRICSOILGRIDS_new_average_phx10percent_reduced.tif Ph_x_10 --layer layers/ISRICSOILGRIDS_new_average_sandpercent_reduced.tif Sand --layer layers/ISRICSOILGRIDS_new_average_soilorganiccarboncontent_reduced.tif Organic_content --layer layers/LandCover_1_Needleleaf.tif Needleleaf --layer layers/LandCover_6_Herbaceous.tif Herbaeous --layer layers/climate_distance_pairwiseavg_10m.precip.tif precip_distance --layer layers/climate_distance_pairwiseavg_10m.temp.tif temp_distance
  ```

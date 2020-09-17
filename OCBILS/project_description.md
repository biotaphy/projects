Summary of Ocbils project


----


Data Processing
===============

Python requirements:
 - gdal
 - lmpy - https://github.com/lifemapper/lmpy
 - BiotaphyPy - https://github.com/biotaphy/BiotaphyPy

1. Acquire study tree (Smith and Brown 2008)
2. Get accepted taxa names for the tips in the tree (get_accepted_names_for_tree.py)
3. Download data from iDigBio and GBIF
 - iDigBio: https://api.idigbio.org/v2/download/?rq={%22scientificname%22:%20{%22type%22:%20%22exists%22},%22kingdom%22:%20%22Plantae%22,%20%22geopoint%22:%20{%22type%22:%20%22exists%22}}&email={fill in email}
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
  $ process_occurrences.py -f $WRANGLER_CONFIG_DIR/decimal_precision_filter.json -f $WRANGLER_CONFIG_DIR/gbif_flag_filter.json -f $WRANGLER_CONFIG_DIR/accepted_taxon_filter.json -f $WRANGLER_CONFIG_DIR/gbif_to_common_map_modifier.json gbif_processed.csv species decimalLongitude decimalLatitude gbif.csv
  $ process_occurrences.py -f $WRANGLER_CONFIG_DIR/decimal_precision_filter.json -f $WRANGLER_CONFIG_DIR/idigbio_flag_filter.json -f $WRANGLER_CONFIG_DIR/accepted_taxon_filter.json -f $WRANGLER_CONFIG_DIR/idigbio_to_common_map_modifier.json -g idigbio_processed.csv species lon lat idigbio.csv
  ```
6. Split processed files into easier to manage chunks (split_occurrences.py)
  ```
  $ split_occurrences.py chunks/occurrences_ species x y 2 0 species gbif.csv idigbio.csv
  ```
7. Sort chunks (sort_occurrences.py)
  ```
  $ sort_occurrences.py chunks/occurrences_aa.csv sorted/occurrences_aa.csv species x y
  $ sort_occurrences.py chunks/occurrences_ab.csv sorted/occurrences_ab.csv species x y
  ...
  $ sort_occurrences.py chunks/occurrences_zz.csv sorted/occurrences_zz.csv species x y  
  ```
8. Process sorted chunks into one large file and filter duplicate localities, filter with KEW expert opinion localities, and minimum number of points (process_occurrences.py)
  ```
  $ process_occurrences.py -f $WRANGLER_CONFIG_DIR/duplicate_locality_filter.json -f $WRANGLER_CONFIG_DIR/kew_locality_filter.json -f $WRANGLER_CONFIG_DIR/minimum_points_filter.json processed_occurrences.csv species x y sorted/occurrences_aa.csv sorted/occurrences_ab.csv ... sorted/occurrences_zz.csv
  ```
9. For each region, process larger occurrence file into regional subset and filter out species without enough points (process_occurrences.py)
  ```
  $ process_occurrences.py -f $WRANGLER_CONFIG_DIR/africa_bbox_filter.json -f $WRANGLER_CONFIG_DIR/minimum_points_filter.json africa_occurrences.csv species x y processed_occurrences.csv
  $ process_occurrences.py -f $WRANGLER_CONFIG_DIR/australia_bbox_filter.json -f $WRANGLER_CONFIG_DIR/minimum_points_filter.json australia_occurrences.csv species x y processed_occurrences.csv
  $ process_occurrences.py -f $WRANGLER_CONFIG_DIR/south_america_bbox_filter.json -f $WRANGLER_CONFIG_DIR/minimum_points_filter.json south_america_occurrences.csv species x y processed_occurrences.csv
  ```
10. POST using Lifemapper / Biotaphy web UI (http://client.lifemapper.org/biotpahy/)
11. Calculate PAM stats, encode environment layers and create GeoJSON (join_env_and_pam_stats.py)
  ```
  $ join_env_and_pam_stats.py 
  ```

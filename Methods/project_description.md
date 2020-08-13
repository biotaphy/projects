Occurrence Data
===============



Seed Plants
-----------

To acquire occurrence data for all of seed plants in both GBIF and iDigBio, it
was not feasible to pull one species, or even one genus, at a time using the
synchronous APIs exposed by both data providers.  Therefore, data was retrieved
from the "download" APIs exposed by both providers.

iDigBio url: https://api.idigbio.org/v2/download/?rq={%22scientificname%22:%20{%22type%22:%20%22exists%22},%22kingdom%22:%20%22Plantae%22,%20%22geopoint%22:%20{%22type%22:%20%22exists%22}}&email=cjgrady@ku.edu


GBIF url: https://api.gbif.org/v1/occurrence/download/request

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

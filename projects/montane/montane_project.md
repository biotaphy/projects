Description
===========
Alpine climatic regions are defined by extreme environmental conditions.
Diverse groups of plants and animals across the Tree of Life not only persist,
and previous genetic studies have provided support that certain lineages have
diversified recently and rapidly in situ. Still, studies within and between
alpine climatic regions and montane areas have been limited to certain well-
studied lineages and areas. Largely due to the fact that such areas are remote
and often understudied, we know much less about the diversity of life across
alpine and montane ecosystems as a whole, and how diversity compares within and
between regions. In this study, we leverage one of the most complete syntheses
of collection information to address specific hypotheses about processes
generating biodiversity in montane and alpine climatic regions.


Configuration
=============

Study Area
----------
The study area for this project is the Americas with the bounding box (, , , )

Climate Data
------------
The climate data for this project comes from WorldClim 1.4.  The follwing
layers are used for modeling:
  * Bio 1
  * Bio 6
  * Bio 8
  * Bio 10
  * Bio 17
  * Bio 18
  * Bio 19
  * Aspect
  * Elevation
  * Slope
  * Percent coarse fragment
  * Percent silt
  * Percent organic content
  * Land cover: mixed trees
  * Land cover: shrubs


Tree
----
The phylogenetic tree used for this project comes from https://github.com/FePhyFoFum/big_seed_plant_trees/releases, (ALLOTB.tre file)


Occurrence Data
---------------
Occurrence data for this project comes from both GBIF and iDigBio.  The GBIF
accepted taxon names from the tips of the tree are used to pull the data from
both sources.

Occurrence Data Filters
-----------------------
Occurrence data is filtered using multiple methods

  1. Bounding Box
    Only occurrence records within the study area are kept (, , , )
  2. Aggregator Flags
    GBIF and iDigBio include flags within the data records indicating potential issues with the data.  Occurrence records that have the following flags are removed.
      a. GBIF
        * 
      b. iDigBio
  3. Known localities
    Plants of the World Online provides information about where a species is
    known to occur using TDWG codes.  The occurrence records are intersected
    against the corresponding locality shapefiles from () and any record that
    does not intersect with the specified localities is removed.


Species Distribution Modeling Algorithm
---------------------------------------
Species distribution models were created with Maxent (maxent link) using the
default parameters except for:

Presence Absence Matrix

Post Processing


Filters
=======
 * Bounding box ()
 * Aggregator flags
    * GBIF
    * iDigBio
 * Locality


Workflow
========



Tree
Get names from tree
Get accepted names
Get occurrence data
Get locality data
Filter data by
 Bounding box
 Aggregator flags
 Locality
Build occurrence file

Climate Data


Modeling algorithm / parameters

Post processing

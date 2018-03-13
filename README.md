# Organism World Map

Generate world maps displaying the distribution of biological species. This script uses the data from the
[catalogue of life](http://www.catalogueoflife.org) project and maps it onto a world map provided by [amcharts](https://www.amcharts.com/svg-maps/) under the Create Common License.


Usage
=====

__Example:__ Generating a map for Aspergillus niger.

Lookup the id on the [catalogue of life](http://www.catalogueoflife.org/col/search/) website by searching for Aspergillus niger. The id is displayed in the url bar of the browser: catalogueoflife.org/col/details/species/id/`ea00b3b8c44dbcf76443e20f78411dc2`.

Run the script:
````shell
python generate_map.py --id ea00b3b8c44dbcf76443e20f78411dc2
````

__Output:__

![Example](https://github.com/JuBra/organism-world-map/raw/docs/img/example.png)

Options
=======

`--id` Organism id from the Catalogue of Life

`--color` Fill color of the countries the organism has been sampled from __*(Optional)*__
  
`--out` Path of the resulting map file __*(Optional)*__
    

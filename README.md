# Organism World Map

Generate world maps displaying the distribution of biological species. This script uses the data from the
[catalogue of life](http://www.catalogueoflife.org) project and maps it onto a world map provided by [amcharts](https://www.amcharts.com/svg-maps/) under the Create Common License.


Usage
=====

__Example - Generate a map for Aspergillus niger__

1. Search for Aspergillus niger in the catalogue [catalogue of life](http://www.catalogueoflife.org/col/search/)
2. Get the organism id from the url bar of the browser: 
catalogueoflife.org/col/details/species/id/`ea00b3b8c44dbcf76443e20f78411dc2`
3. Run the script using the id:
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
    

# Organism World Map

Generate world maps displaying the distribution of biological species. This script uses the data from the
[Catalogue of Life](http://www.catalogueoflife.org) and maps it onto a world map provided by [amcharts](https://www.amcharts.com/svg-maps/).


Usage
=====

__Example:__
Generating a map for Aspergillus niger. 
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
    

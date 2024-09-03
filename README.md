## Processing of WRF simulations with Docker containers in Azure cloud environment
Running WRF simulation on a local or Virtual Machine takes up a **lot** of resources and requires above-average computers. Using docker allows a reduction in resources as well as the possibility of migrating containers into cloud environments, like *MS AZURE CLOUD*.

## Motivation
Reduction of computation costs associated with large CORE and RAM usage for *OOM*.

## Screenshots
![OOM logo](https://oom.arditi.pt/assets/OOM_Logo.png)

## Tech/framework used

<b>Built with</b>
- [WRF](https://www.mmm.ucar.edu/models/wrf)
- [Docker](https://www.docker.com/)
- [Pyhton](https://www.python.org/)
- [Bash](https://pt.wikipedia.org/wiki/Bash)

## Features
Allows automation of simulations for multiple domains. Performs verifications on input files. It kills the container in the case of **MPI ABORT**. 

For more detailed info, consult [documentation](WRF-documentation.pdf).

The `reduced_wrf_image.tar.gz` and `wrf_image.tar.gz` have the same contents, but the first is a compressed and improved version of the first one. Of the **32GB** around **20GB** comes from `WPS_GEOG` geographical data. 

The current resolution is 30 arc seconds. For reduced resolution, delete `lai_modis_30s` **(11 GB)** e `varsso` **(2.5GB)**, change `WPS-*/geogrid/GEOGRID.TBL.ARW` and alter *default:lai_modis_30s* for desired resolution. Ex: *default:lai_modis_10m*

Geographical data can be retrieved from [here](https://www2.mmm.ucar.edu/wrf/users/download/get_sources_wps_geog.html) or [here](http://www2.mmm.ucar.edu/wrf/src/wps_files/).

## Installation
<b>After downloading `reduced_wrf_image.tar.gz` *(3.3GB)* or `wrf_image.tar.gz` *(22.3 GB)* from SSD:</b>

- `docker load` -i /path/to/`reduced_wrf_image.tar.gz` -> This normally takes *15 minutes* for `reduced_wrf_image.tar.gz` and over an hour for `wrf_image.tar.gz`;
- On your **WDIR** install: `core_calc`;
- Provide the necessary input files: `instructions.txt`, `wps_input.txt` and `wrf_input.txt`;
- Example files are listed below. Change `instructions.txt` *processors* value for an adequate value;

## Input file example
- All necessary files are [here](Necessary_input_files/);
The number of processors should be changed [here](Necessary_input_files/instructions.txt)
- All other aspects must be changed in the remaining files.

## How to use?
- In main folder `./run.sh -e START_DATE=2024-09-01 -e END_DATE=2024-09-01_03:00:00`. Date format is either **%Y-%m-%d** or **%Y-%m-%d_%H:00:00** -> Time intervals must be multiples of 3h for *forecast mode* and 6h for *historic mode*;
- Validate output given in console with *y* or *n*;
- Data will be output in the `data` folder if no errors occur.

## Tests
For a quick test, try the input files, changing **max_dom=2** to 1 in `wps_input.txt` and `wrf_input.txt`. Simulation should take around 2 minutes and files should appear in the recently created `data` folder.

## Credits
<b>Made by:</b>
- Luís Fernando Nóbrega
- Ricardo Faria

## License
A short snippet describing the license (MIT, Apache etc)

MIT © [Fernando]()

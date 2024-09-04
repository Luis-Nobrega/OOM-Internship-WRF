## Processing of WRF simulations with Docker containers in Azure cloud environment
Running WRF simulation on a local or Virtual Machine takes up a **lot** of resources and requires above-average computers. Using docker allows a reduction in resources, as well as the possibility of migrating containers into cloud environments, like *[MS AZURE CLOUD](https://azure.microsoft.com/en-us)*.

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

## Installation if docker image was provided by OOM
<b>After downloading `reduced_wrf_image.tar.gz` *(3.3GB)* or `wrf_image.tar.gz` *(22.3 GB)* from SSD:</b>

- `docker load` -i /path/to/`reduced_wrf_image.tar.gz` -> This normally takes *15 minutes* for `reduced_wrf_image.tar.gz` and over an hour for `wrf_image.tar.gz`;
- On your **WDIR** install: `core_calc` and give it extra premissions with  `sudo chmod +x run.sh`;
- Provide the necessary input files: `instructions.txt`, `wps_input.txt` and `wrf_input.txt`;
- Example files are listed below. Change `instructions.txt` *processors* value for an adequate value;

## Installation if Docker image wasn't provided

### Starting Docker image

Check if docker is installed.
```
docker ps
```
If not, install it [here](https://docs.docker.com/engine/install/).

Start the docker container with the provided [Dockerfile](/CONFIGS/Dockerfile) in your desired directory. This may take some minutes.
```
docker build -t my_image_name . 
```

Enter the container in interactive mode:
```
docker run -it my_image_name
```

Download and execute the proper installation script [WRF4.6.0_Install.bash](https://github.com/bakamotokatas/WRF-Install-Script/blob/master/WRF4.6.0_Install.bash). This will take about an hour and 50 GB of space. 
```
bash WRF4.6.0_Install.bash
```

You can and **should** delete tar.gz files after installation and testing. Search them using:
```
find . -type f \( -name "*.tar" -o -name "*.tar.gz" \)
```

### Install other dependencies
In order for downloads to work:
```
apt-get update
apt install pip
pip install requests
```
### Seting up the interior of the container

Setup executables in CONFIGS folder. The files can be found [here](/CONFIGS/).
```
cd Build_WRF/
mkdir CONFIGS
cd CONFIGS/
ls 
forecast_download.py  forecast.sh  historic_download.py  instructions.txt  model_set.py  namelist_editer.py  processors.py  wps_input.txt  wrf_input.txt
```
Give permissions to `forecast.sh`:
```
chmod +x forecast.sh
```

Alter `WPS` directory:
```
cd --
cd Build_WRF/WPS-4.6.0/
mkdir GRIB_FILES
mkdir METGRIB_FILES
ln -s ungrib/Variable_Tables/Vtable.GFS Vtable
```

If you need to change simulation resolution, change `GEOGRID.TBL`.

Sections will be divided by '=====' and have names such as **name=LANDUSEF**. To change resolution, find:rel_path = default:**topo_gmted2010_30s**/ and change the **bold** term to the correct file.
```
nano geogrid/GEOGRID.TBL
```

All resolution files can be altered in:
```
cd --
cd Build_WRF/WPS_GEOG/
```

## Saving the image after editing
After everything is setup, list the containers and get the CONTAINER ID:
```
exit
# to list containers
docker ps -a 
docker commit CONTAINER_ID my_image_name
# to list images
docker ps -a 
```

If some step that [forecast.sh](/CONFIGS/forecast.sh) doens't make was forgotten, please consult [WPS](https://www2.mmm.ucar.edu/wrf/users/wrf_users_guide/build/html/wps.html) or [WRF](https://www2.mmm.ucar.edu/wrf/users/wrf_users_guide/build/html/running_wrf.html) for detailed initialization steps.

### Testing

Testing is recommended prior to exiting. Please alter alter the input files to run 1 domain and add some **GFS** [files](https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl) to `/Build_WRF/WPS-4.6.0/GRIB_FILES`. You can add them with `wget`.

Run `forecast.sh` and check for errors. Logfiles contain all info for eventual missing paramethers.

For additional debugging consult [WPS](https://www2.mmm.ucar.edu/wrf/users/wrf_users_guide/build/html/wps.html) or [WRF](https://www2.mmm.ucar.edu/wrf/users/wrf_users_guide/build/html/running_wrf.html).

## Seting up the local environment 

In a local directory, add [run.sh](/run.sh), [core_calc.py](/core_calc.py), [instructions.txt](/HOST/instructions.txt), [wps_input.txt](/HOST/wps_input.txt) and [wrf_input.txt](/HOST/wrf_input.txt).

**Change** `image_name="reduced_ubuntu_image"` in [run.sh](/run.sh) to match your image_name.

## Running 
- In main folder `./run.sh -e START_DATE=2024-09-01 -e END_DATE=2024-09-01_03:00:00`. Date format is either **%Y-%m-%d** or **%Y-%m-%d_%H:00:00** -> Time intervals must be multiples of 3h for *forecast mode* and 6h for *historic mode*;
- Validate output given in console with *y* or *n*;
- Data will be output in the `data` folder if no errors occur.

## Tests
For a quick test, try the input files, changing **max_dom=2** to 1 in `wps_input.txt` and `wrf_input.txt`. Simulation should take around 2 minutes and files should appear in the recently created `data` folder.

## Input files and host environment documentation
For information about the input files or *Azure Cloud* setup, click [here](HOST/).

## Internal functions documentation 
For information about the internal functions, purpose and future changes, click [here](CONFIGS/).

## Credits
<b>Made by:</b>
- Luís Fernando Nóbrega
- Ricardo Faria

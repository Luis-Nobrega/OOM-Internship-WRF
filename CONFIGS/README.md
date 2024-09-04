# Internal Docker files

All the provided files sit inside the `reduced_ubuntu_image` container in the `CONFIGS` folder. They are responsible for downloading, altering and delivering data in the appropriate time and place to **WRF** system.

## Internal files listing 
<b> Used files are: </b>
- `forecast.sh` -> main scipt executable;
- `*.txt` -> copied input files from *host*;
- `model_set.py` -> sets *forecast* or *historic* modes;
- `processors.py` -> sets adequate number of [processors](https://forum.mmm.ucar.edu/threads/choosing-an-appropriate-number-of-processors.5082/);
- `namelist_editer.py` -> edits internal namelists names;
- `forecast_download.py` -> downloads [gfs files](https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl); 
- `historic_download.py` -> downaloads [gfs files](https://rda.ucar.edu/datasets/d083003/dataaccess/#).

## core_calc.py 
This is by far the most important file as it performs all the necessary formating and checks prior to running.
<b>Actions performed</b>
- Formats [wps_input.txt](/HOST/wps_input.txt) and [wrf_input.txt](/HOST/wrf_input.txt) time variables;
- Formats almost the entirety of [instructions.txt](/HOST/instructions.txt);
- Calculates and limits proper [processor](https://forum.mmm.ucar.edu/threads/choosing-an-appropriate-number-of-processors.5082/) usage;
- Compares matching terms in [wps_input.txt](/HOST/wps_input.txt) and [wrf_input.txt](/HOST/wrf_input.txt) and **warns** about mismatches;
- Checks nested domains size and position validiy;
- Determines operation mode based on given `START_DATE` and `END_DATE`;
- Calculates approximate coordinate domain for simulation if in `forecast` mode;
- Checks for the presence of sensitive directories such as `/home/swe/Build_WRF/WPS-4.6.0/METGRIB_FILES`.

Always verify the script feedback before advancing. Just because it didn't `raise ValueError(...)` it doesn't mean that the input values are correct.

## Dockerfile and package installation
The [`Dockerfile`](/CONFIGS/Dockerfile) was used to create the container through `$dockerbuild`. It downloads a series of packages using *one* `RUN` statement. This ensures that only *one* layer is created. Altough image saving times might be higher, the disk usage is almost reduced by **half**. The same is true for `ENV` statement.

Aditionally other dependencies such as `pip` and the `requests` *python* package were installed.


The format of input files was chosen as **GFS** through the choosing of the right Vtable in `WPS/ungrib/Variable_Tables/Vtable.GFS` and the resolutions altered in `WPS/geogrid/GEOGRID.TBL`. 
## Simulation modes
There are two operating modes, **forecast** and **historic**.

### Forecast
- Time interval for dates chosen up to 7 days prior to `UTC` time;
- Can run up to 384h (16 days) after start_date;
- Allows data retireving intervals that are multiples of 3. By default, it will try to use 6h.
- Allows for selecting data based on the domain size and coordinates.

### Historic
- Time intervals for dates later than 7 days;
- Time limit of 9 years back;
- Data retrieval intervals of multiples of 6h (6h is recommended);
- Doesn't allow for selective data. GFS files will be substancially bigger in this mode (500 MB vs 50 MB);
- Lower data volumes for older start_dates;
- Max recommended period is one month.

The operating mode is automatically chosen by [core_calc.py](/core_calc.py), based on the input dates.
## Data download 
All data will be stored in the recently created `data` folder after a successful run. 

All output files will be simular to  `wrfout_d01_2024-08-01_00:00:00`. There should be a file for each interval chosen. 

Ex: if you chose to simulate from 00:00:00 to 09:00:00 in 3h intervals, there should be the corresponding 00:00:00, 03:00:00 and 06:00:00 wrfout files.

## File limitations and resolution

The maximum allowed resolution is *30 arc seconds*. If you desire to change it, alter the **default** keyword in `GEOGRID.TBL` to match the correct file name in `WPS_GEOG` folder. 

To add new geographical files, click [here](https://www2.mmm.ucar.edu/wrf/users/download/get_sources_wps_geog.html) or [here](http://www2.mmm.ucar.edu/wrf/src/wps_files/).

### Kept resolution files
- albedo_modis      	
- lai_modis_30s 
- modis_landuse_20class_30s_with_lakes  
- soiltemp_1deg 	
- soiltype_top_30s	
- varsso greenfrac_fpar_modis 
-  maxsnowalb_modis  
- orogwd_10m   
- soiltype_bot_30s   
- topo_gmted2010_30s
### Deleted resolution files
- varsso_10m 
- varsso_5m 
- varsso_2m 
- orogwd_2deg 
- orogwd_1deg 
- orogwd_30m 
- orogwd_20m 
- lai_modis_10m;

## Future modifications 

For altering the source of **GFS** files, the main function to alter is **get_links(...)** in either [historic_download.py](/CONFIGS/historic_download.py) or [forecast_download.py](/CONFIGS/forecast_download.py). 

Additionally, if a new source of historic files that allows for domain subsections (choosing coordinates) to be chosen is found, new global variables have to be extracted from [instructions.txt](/HOST/instructions.txt) such as `left, right, top, bot`.

The first two lines of the `coordinates(mode)` function in [core_calc.py](/core_calc.py) must also be commented for coordinates to update.

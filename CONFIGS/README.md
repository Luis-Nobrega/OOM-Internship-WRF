## Internal Docker files

All the provided files sit inside the `reduced_ubuntu_image` in the `CONFIGS` folder. They are responsible for downloading, altering and delivering data in the appropriate time and place to **WRF** system.

## Internal files listing 
<b> Used files are: </b>
- `forecast.sh` -> main scipt executable;
- `*.txt` -> copied input files from *host*;
- `model_set.py` -> sets *forecast* or *historic* modes;
- `processors.py` -> sets adequate number of [processors](https://forum.mmm.ucar.edu/threads/choosing-an-appropriate-number-of-processors.5082/);
- `namelist_editer.py` -> edits internal namelists names;
- `forecast_download.py` -> downloads [gfs files](https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl); 
- `historic_download.py` -> downaloads [gfs files](https://rda.ucar.edu/datasets/d083003/dataaccess/#).

## Dockerfile and package installation
The [`Dockerfile`](/CONFIGS/Dockerfile) was used to create the container through `$dockerbuild`. It downloads a series of packages using *one* **<font color="#CC0099">RUN</font>** statement. This ensures that only *one* layer is created. Altough image saving times might be higher, the disk usage is almost reduced by half. The same is true for **<font color="#CC0099">ENV</font>** statement.

Aditionally other dependencies such as `pip` and the `requests` *python* package were installed.

## Simulation modes

## Data download 

## File limitations and resolution

## Future modifications 

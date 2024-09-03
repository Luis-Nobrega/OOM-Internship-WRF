## Internal Docker files

All the provided files sit inside the `reduced_ubuntu_image`.

## Internal files
<b> Used files are: </b>
- `forecast.sh` -> main scipt executable 
- `*.txt` -> copied input files
- `model_set.py` -> sets *forecast* or *historic* modes
- `processors.py` -> sets adequate number of [processors](https://forum.mmm.ucar.edu/threads/choosing-an-appropriate-number-of-processors.5082/)
- `namelist_editer.py` -> edits internal namelists name for compatability
- `forecast_download.py` -> donwloads gfs [files](https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl)  
- `historic_download.py` -> downaloads gfs [files](https://rda.ucar.edu/datasets/d083003/dataaccess/#) 

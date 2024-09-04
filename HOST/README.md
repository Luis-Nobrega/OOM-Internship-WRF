# Input files 
In order to adapt your simulation to your needs, input files must be changed according to *WRF* rules.

## instructions.txt
The [intructions.txt](/HOST/instructions.txt) file is responsible for expressing time and mode information in a more readable way for the user and other scripts. Every **keyword**, except `processors` is automatically changed by [core_calc.py](/core_calc.py).

After running [core_calc.py](/core_calc.py), an interval will appear:
```
MIN processors: 1
MAX processors: 16
Now using: 4 
```
The program will throw an error if the requested cores are lower than the **minimum**, however, if the **maximum** is exceeded, user input will be required to continue. It is **not** recommended to exceed the maximum `processors` unless the simulation is failing due to a low processor count. 
```
You are exceeding the maximum number of processors 16: by using 40. Are you sure? y/n
```
The core boundaries were based on [this](https://forum.mmm.ucar.edu/threads/choosing-an-appropriate-number-of-processors.5082/) forum.

## wps_input.txt
The [wps_input.txt](/HOST/wps_input.txt) file is the file commonly known as `namelist.wps` that sits inside the `WPS-4.6.0/` folder. It is responsible for the `geogrid`, `ungrib` and `metgrib` instances. 

All the date related **keywords** are automatically altered by [core_calc.py](/core_calc.py), which includes **start_date**, **end_date** and **interval_seconds**. Therefore, everything else, especially **max_dom** (for choosing nested domains), must be manually altered.

The *file_section* that usually suffers modifications is **&geogrid**, and typically looks like this:
```
&geogrid                                                                                                 
 parent_id         =   1,1,2,3,                                                                          
 parent_grid_ratio =   1,3,5,5,                                                                          
 i_parent_start    =   1,20,10,12,                                                                       
 j_parent_start    =   1,30,10,12,                                                                       
 e_we              = 100,46,121,58,                                                                      
 e_sn              = 100,37,121,58,                                                                      
 geog_data_res = '30s','30s','30s','30s',                                                               
 dx = 15000,                                                                                             
 dy = 15000,                                                                                             
 map_proj = 'mercator',                                                                                  
 ref_lat   = 39.108285,                                                                                  
 ref_lon   = -7.326181,                                                                                 
 truelat1  = 39.108285,                                                                                  
 truelat2  = 0,                                                                                          
 stand_lon = -7.326181,                                                                                 
geog_data_path='../WPS_GEOG/',
/       
``` 

## wrf_input.txt 

The [wrf_input.txt](/HOST/wrf_input.txt) is commonly known as the `namelist.input` file that sits inside the `WRF-4.6.0-ARW/test/em_real/` folder. It is responsible for `real.exe` and `wrf.exe` instances. 

All the date related **keywords** are automatically altered by [core_calc.py](/core_calc.py). This includes every **keyword** before **interval_seconds** (inclusively). 

This is the most complex file that includes all **&physics** and **&dynamics** instructions. Between similar simulations, the most commonly **keywords** include **max_dom** **e_sn** and **e_we**. The most changed part is this:

```
 max_dom                             = 1,                                                                          
 e_we                                = 100,   46,   121,                                                           
 e_sn                                = 100,   37,   121,                                                           
 e_vert                              = 37,    37,    37,                                                           
 p_top_requested                     = 5000,                                                                       
 num_metgrid_levels                  = 34,                                                                         
 num_metgrid_soil_levels             = 4,                                                                          
 dx                                  = 15000, 5000,  1000,                                                         
 dy                                  = 15000, 5000,  1000,                                                         
 grid_id                             = 1,     2,     3,                                                            
 parent_id                           = 1,     1,     2,                                                            
 i_parent_start                      = 1,     20,    10,
```

## Nested domain rules
When working with nested domains it is necessary to follow several steps to ensure compatability. If their requirements aren't met, [core_calc.py](/core_calc.py) will throw an error. If the dimensions are correct, you should see something similar to this:
```
Valid nested domain sizes: 2 domains in use
```

![Image](https://www2.mmm.ucar.edu/wrf/users/wrf_users_guide/build/html/_images/wps_ij_parent_start.png)

<b> Rules to follow </b>
- `Parent domain needs to encapsulate the others` -> Ex: if **parent_id** = 1,1,2,3 all nested domains would be totally inside the previous one but if instead **parent_id** = 1,1,2,3,2 the fifth domain **can't** need to be inside the third, only the second;
- `Parent grid ratio of a child can't be bigger than the parent's domain` -> **parent_grid_ratio** = 1,3,5,5;
- `e_we and e_sn must match parent_grid_ratio` -> if **parent_grid_ratio** is 3, then **e_we** has to be a multiple of **3**, plus 1, as all grids start locally on (i,j) = (1,1). Ex: 31, 34, etc.. are valid.
- `Nested domains must fit in parent domain` -> Ex: if **e_we** = 100 and **i_parent_start** = 30 with a **parent_grid_ratio** = 3, then as there are 70 tiles left, the max **e_we** of the nested domain is 70*3 = 210; 

For more info about [nesting](https://www2.mmm.ucar.edu/wrf/users/wrf_users_guide/build/html/wps.html#wps-nested-domains).


## Debugging 
In 90% of cases, failures such as **MPI ABORT** happen because of incorrect input file information. As [run.sh](/run.sh) executes, a *logfile* is printed in the host console. It usually contains all the information necessary to correct the error.

<b>Possible *internal* error causes:</b>
- **topo_wind** is not set to `0` in [wrf_input.txt](/HOST/wrf_input.txt) for nested domains;
- Weak [internet speed](https://fast.com/pt/) caused `gfs` download failure; 
- Data sources discontinued -> [forecast](https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl) or [historic](https://rda.ucar.edu/datasets/d083003/dataaccess/#);
The download request was too big. Use a smaller period as `gfs` files can take up to 500 MB each (worst case);
- Invalid extra parameters that require extra configuration added;
- Unmathcing **keywords** in WPS and WRF input files;
- Missing mandatory parameters or deleted keywords;
- Skill issue;


<b>Useful information for debugging namelists:</b>
- [Documentation](/WRF-documentation.pdf)
- [Running WPS](https://www2.mmm.ucar.edu/wrf/users/wrf_users_guide/build/html/wps.html)
- [Running WRF](https://www2.mmm.ucar.edu/wrf/users/wrf_users_guide/build/html/running_wrf.html)
- [WPS namelist variables](https://www2.mmm.ucar.edu/wrf/users/wrf_users_guide/build/html/namelist_variables.html)
- [Compilation](https://www2.mmm.ucar.edu/wrf/users/wrf_users_guide/build/html/compiling.html)
- [General info](https://www.mmm.ucar.edu/models/wrf)

# Azure Cloud setup

The first step is to configure the local **VM** environment:
```
az login

az group create -- name myResearchGroup --location eastus

az vm create \\
    -- resource-group my ResearchGroup \\
    -- name myVM \\
    -- image UbuntuLTS \\
    -- size Standard_D32ls_v5 \\
    -- admin-username azureuser \\
    -- generate-shh-keys
```

Then the image needs to be saved to local environment, loaded, ran and stopped:

```
docker save -o mydockerimage.tar.gz 

scp mydockerimage.tar.gz azureuser@<vm-public-ip>:/home/azureuser/

docker load mydockerimage.tar.gz

docker run -d --name mycontainer -e START_DATE=2023-01-01 -e END_DATE=2023-01-28 \\
-v /mnt/data:/app/data myCOntainerRegistry.azurecr.io/mydockerimage

az vm stop- --resource-group myResourceGroup --name myVM

az vm delete --resource-group myResourceGroup --name myVM --yes --no-wait

```

Finally, check the output logs and download the data:

```
docker logs mycontainer

scp azureuser@<vm-public-ip>:/path/to/data /local/path
```

[def]: HOST/

#!/bin/bash

#################### READ_ME ####################
# year, month, day, hour, left, right, top, bot, forecast, 
# mode and processors must be given in instructions.txt
# wps_input.txt and wrf_input.txt must be changed prior 
# to executing this bash script -> Douple check pls 
#################### GET ONLINE FILES ####################

cd /home/swe/Build_WRF/WPS-4.6.0/GRIB_FILES
rm gfs.*
rm gdas*

cd /home/swe/Build_WRF/CONFIGS

PROCESSORS=$(python3 processors.py)
output=$(python3 model_set.py)
case "$output" in
    forecast)
        echo "Starting forecast mode"
        python3 namelist_editer.py # changes input files for contents in wps_input.txt and wrf_input.txt
        python3 forecast_download.py  # Dowloads all links given on "instructions.txt"
        ;;
    historic)
        echo "Starting historic mode"
        python3 namelist_editer.py
        python3 historic_download.py
        ;;
    *)
        echo "Unexpected usage mode: $output -> please use "forecast" or "historic""
        exit 1
        ;;
esac

cd /home/swe/Build_WRF/WPS-4.6.0/GRIB_FILES
ls -lh

#################### WPS SETUP ####################

######### GEOGRID #########

cd /home/swe/Build_WRF/WPS-4.6.0

echo "Running WPS setup"
rm geo_em.* # remove old files 

ls -ls geogrid/GEOGRID.TBL
echo "Running geogrid.exe..."
./geogrid.exe

# Check if geogrid.exe ran successfully
if [ $? -ne 0 ]; then
    echo "Error: geogrid.exe failed to run. Perhaps invalid namelist.wps file"
    exit 1
fi

FILES=$(find . -name "geo_em.*")

if [ -z "$FILES" ]; then
    echo "Error: No geo_em.* found."
    exit 1
fi

######### UNGRIB #########

rm GRIBFILE.*
rm GFS:*

case "$output" in
    forecast)
        ./link_grib.csh ~/Build_WRF/WPS-4.6.0/GRIB_FILES/gfs*.
        ;;
    historic)
        ./link_grib.csh ~/Build_WRF/WPS-4.6.0/GRIB_FILES/gdas*.
        ;;
    *)
        echo "Unexpected usage mode: $output -> please use "forecast" or "historic""
        exit 1
        ;;
esac

GRIBFILES=$(find . -name "GRIBFILE.*")
if [ -z "$GRIBFILES" ]; then
    echo "Error: No /GRIBFILE.* found. Check /GRIB_FILES to see if gfs.* files exist and are not corrupted"
    exit 1
fi

echo "Running ungrib.exe..."
./ungrib.exe

if [ $? -ne 0 ]; then
    echo "Error: ungrib.exe failed to run. Perhaps invalid namelist.wps file."
    exit 1
fi
GFS=$(find . -name "GFS:*")
if [ -z "$GFS" ] ; then
    echo "Error: No GFS files found. Check log and try again"
    exit 1
fi

######### METGRIB #########
cd /home/swe/Build_WRF/WPS-4.6.0/METGRIB_FILES
rm met_em.*

cd /home/swe/Build_WRF/WPS-4.6.0
ln -sf metgrid/METGRID.TBL.ARW .
echo "Running metgrid.exe..."
./metgrid.exe
 
if [ $? -ne 0 ]; then
    echo "Error: metgrib.exe failed to run. Perhaps invalid namelist.wps file."
    exit 1
fi

cd /home/swe/Build_WRF/WPS-4.6.0/METGRIB_FILES
MET_EM=$(find . -name "met_em.*")
if [ -z "$MET_EM" ] ; then
    echo "Error: No met files found. Check log and try again"
    exit 1
fi

#################### WRF SETUP ####################

cd /home/swe/Build_WRF/WRF-4.6.0-ARW/test/em_real
echo "Running WRF setup"

######### RUNNING WRF #########

rm wrfinput_d*
rm wrfout_d*
rm wrfbdy_*
rm met_em.*

ln -sf /home/swe/Build_WRF/WPS-4.6.0/METGRIB_FILES/met_em* .
MET_EM2=$(find . -name "met_em.*")

if [ $? -ne 0 ] || [ -z "$MET_EM2" ]; then
    echo "Error: met_em symbolic vars weren't created."
    exit 1
fi

echo "Running real.exe..."
mpiexec -n $PROCESSORS ./real.exe & # everything will be written in the real.log file  
pid=$! # Capture the process ID of real.exe

tail -f rsl.out.0000 & # Run tail -f in the background to monitor the log file
tail_pid_real=$!
wait $pid
kill $tail_pid_real

if [ $? -ne 0 ]; then
    echo "Error: real.exe failed to run. Perhaps invalid namelist.input file."
    cat rsl.out.0000
    exit 1
fi
WRF_IN=$(find . -name "wrfinput_d*")
if  [ -z "$WRF_IN" ]; then
    echo "Error: wrf_in files not found. Perhaps invalid namelist.input file."
    exit 1
fi

echo "Warning -> Running wrf.exe on background -> This may take hours! -> To see progress: ps aux | grep wrf.exe OR tail -f rsl.error.0000 OR tail -f rsl.out.0000 rsl.log "
mpiexec -n $PROCESSORS ./wrf.exe > rsl.out.0000 & # remover 2>&1 e & ?
wrf_pid=$! # Capture the process ID of wrf.exe

tail -f rsl.out.0000 & # Run tail -f in the background to monitor the log file
tail_pid=$!
wait $wrf_pid
kill $tail_pid # kill the unwanted tail 

if [ $? -ne 0 ]; then
    echo "Error: wrf.exe failed to run. Perhaps invalid namelist.input file."
    cat rsl.out.0000
    exit 1
fi
WRF_OUT=$(find . -name "wrfout*")

if [ -z "$WRF_OUT" ]; then
    echo "Error: wrf_out files not found. Perhaps invalid namelist.input file."
    exit 1
    else
    echo "SUCESS: wrf.exe has run. Please check files for corruption with ncdump or ncview."
fi

#!/bin/bash

# Set up necessary variables
in_file="instructions.txt"
wps_file="wps_input.txt"
wrf_file="wrf_input.txt"
container_directory="/home/swe/Build_WRF/CONFIGS"
container_output_directory="/home/swe/Build_WRF/WRF-4.6.0-ARW/test/em_real"
current_dir=$(pwd)
new_dir_name="data"
container_name="wrf_container"
#image_name="my-ubuntu-22.04-image"
image_name="reduced_ubuntu_image"
executable="forecast.sh"
pattern="wrfout_d*"

# Environment variables 
START_DATE=""
END_DATE=""

while getopts "e:" opt; do
  case ${opt} in
    e)
      # Extract environment variable name and value
      VAR_NAME=$(echo "$OPTARG" | cut -d '=' -f 1)
      VAR_VALUE=$(echo "$OPTARG" | cut -d '=' -f 2)
      # Set the corresponding variable
      if [ "$VAR_NAME" == "START_DATE" ]; then
        START_DATE="$VAR_VALUE"
        export START_DATE="$VAR_VALUE"
      elif [ "$VAR_NAME" == "END_DATE" ]; then
        END_DATE="$VAR_VALUE"
        export END_DATE="$VAR_VALUE"
      else
        echo "Unsupported environment variable: $VAR_NAME"
        exit 1
      fi
      ;;
    *)
      echo "Usage: $0 -e START_DATE=2023-01-01 -e END_DATE=2023-12-31"
      exit 1
      ;;
  esac
done

# Check if the required environment variables are set
if [ -z "$START_DATE" ] || [ -z "$END_DATE" ]; then
  echo "START_DATE and END_DATE must be provided. Ex: ./run.sh -e START_DATE=2023-01-01 -e END_DATE=2023-01-02_03:00:00"
  exit 1
fi

# check weather the simulation inputs are even valid and set dates 
python3 core_calc.py

if [ $? -ne 0 ]; then
    echo "Aborted due to user choice"
    exit 1
else
    # Create directory for storing data
    mkdir -p "$current_dir/$new_dir_name"
    new_dir_path="$current_dir/$new_dir_name"

    # Run the container in the background
    echo "Starting container..."
    docker run -d --name $container_name $image_name /bin/bash -c "while true; do sleep 3600; done"

    # Wait for the container to start
    echo "Waiting for the container to start..."
    sleep 5  # Adjust sleep duration if needed

    # Copy instruction files from the host to the container
    echo "Copying data to the container..."
    docker cp "$current_dir/$in_file" $container_name:$container_directory
    docker cp "$current_dir/$wps_file" $container_name:$container_directory
    docker cp "$current_dir/$wrf_file" $container_name:$container_directory

    # Verify copied files
    echo "Verifying copied files in the container..."
    docker exec -w $container_directory $container_name ls -l

    echo "Following container logs..."
    docker logs -f $container_name &
    log_pid=$!


    ############################ testing area 
    #docker exec -w "/home/swe/Build_WRF/WPS_GEOG" $container_name rm -rf "lai_modis_10m"
    #docker exec -w "/home/swe/Build_WRF/WPS_GEOG" $container_name rm -rf "orogwd_10m"
    #docker exec -w "/home/swe/Build_WRF/WPS_GEOG" $container_name rm -rf "varsso_10m"
    #docker exec -w "/home/swe/Build_WRF/WPS_GEOG" $container_name rm -rf "varsso_5m"


    ###########################

    # Run the main bash file
    echo "Running $executable inside the container..."
    docker exec -w $container_directory $container_name ./$executable &
    exec_pid=$!

    # Follow the logs to see the progress

    # Wait for the forecast process to complete
    echo "Waiting for $executable to complete..."
    wait $exec_pid

    # Check if forecast.sh ran successfully
    if [ $? -ne 0 ]; then
        echo "Error: $executable failed to run inside the container."
        docker exec -it $container_name cat /home/swe/Build_WRF/WRF-4.6.0-ARW/test/em_real/rsl.out.0000
        docker stop $container_name
        docker rm $container_name
        exit 1
    else
        # Stop following logs
        echo "Stopping log following..."
        kill $log_pid

        # Copy wrfout* files from container to host
        echo "Copying wrfout* files from container to host..."
        docker exec -w $container_output_directory $container_name ls -l

        files=$(docker exec $container_name sh -c "ls $container_output_directory/$pattern")

        # Loop through each file and copy it to the host
        for file in $files; do
            filename=$(basename $file)
            echo "Copying $filename to $new_dir_path"
            docker cp $container_name:$container_output_directory/$filename $new_dir_path
        done

        # Stop and remove the container
        echo "Stopping and removing the container..."
        docker stop $container_name
        docker rm $container_name

        echo "Container has been stopped and removed. Check for saved data in $new_dir_path"
    fi
fi

# Reset vars for console not to close in case of error or rerun 
unset START_DATE
unset END_DATE


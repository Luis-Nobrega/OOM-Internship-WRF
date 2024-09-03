import os 

################### paths and files 

main_path = "/home/swe/Build_WRF/CONFIGS"

wps_path = "/home/swe/Build_WRF/WPS-4.6.0"
wps_input_file = "wps_input.txt" # new namelist must be provided to main path 
wps_output_file = "namelist.wps"

wrf_path = "/home/swe/Build_WRF/WRF-4.6.0-ARW/test/em_real"
wrf_input_file = "wrf_input.txt"# new namelist must be provided to main path
wrf_output_file = "namelist.input" 

################### delete the old files 

def file_replacer(directory: str, filename: str, final_directory: str, alternative_filename: str):
    try:
        os.chdir(directory)
        with open(filename, "r") as data:
            content = data.read()
    except FileNotFoundError:
        print(f"The file {filename} was not found in directory {directory}.")
        return
    except OSError as e:
        print(f"Error while accessing the file or directory: {e}")
        return
    
    try:
        if not os.path.exists(final_directory):
            raise ValueError("Final directory does not exist")
        os.chdir(final_directory)
        with open(alternative_filename, "w") as new_file:
            new_file.write(content)
    except OSError as e:
        print(f"Error while writing the file to the final directory: {e}")

################### testing area 

file_replacer(main_path, wps_input_file, wps_path, wps_output_file) # change namelist.wps
file_replacer(main_path, wrf_input_file, wrf_path, wrf_output_file) # change namelist.input
print("Input files successfully altered")
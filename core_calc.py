############################################### 
# made by: nobregaluisfernando@gmail.com 
# and ricardo.faria@oom.arditi.pt 
# made for OOM @ ARDITI
############################################### 

import os
import math
import sys
from datetime import datetime, timedelta, timezone

############################################### 
# Change wps_input.txt
############################################### 

main_path = os.getcwd()
terms = ["e_we", "e_sn"] 
file_name1 = "wps_input.txt"
file_name2 = "wrf_input.txt"
file_name3 = "instructions.txt"
dom_size = "max_dom"

def find_values_for_term(directory, filename, search_term, single=0):
    os.chdir(directory)
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        values = []
        for line in lines:
            # Strip any leading/trailing whitespace and split the line at '='
            parts = [part.strip() for part in line.strip().split('=')]
            
            if len(parts) == 2:
                term, val = parts
                if term == search_term:
                    # Split the values by comma and strip any whitespace
                    values = [v.strip() for v in val.split(',')]
                    values = [x for x in values if x != '']
                    break

        if values:
            if single == 0:
                return values
            elif single == 2:
                return int(max(values))
            try:
                return int(values[0])
            except ValueError:
                return values[0]
        else:
            print(f"Parameter {search_term} missing from {filename}")
            raise ValueError
    
    except FileNotFoundError:
        print(f"The file {filename} was not found in directory {directory}.")
    except Exception as e:
        print(f"An error occurred: {e}")

############################################### 
# Check processor usage
############################################### 

def get_largest_smallest(list1, list2, max_dom):
    if not isinstance(max_dom, int) or max_dom < 1:
        raise ValueError("Invalid number of domains")
    if len(list1) < max_dom or len(list2) < max_dom:
        raise ValueError("Invalid list sizes -> Check if max_dom > values given in wps_input.txt")
    list1 = list1[:max_dom]
    list2 = list2[:max_dom]
    areas = [int(list1[x]) * int(list2[x]) for x in range(len(list1))]

    # Find the indexes of the largest and smallest values
    return (areas.index(max(areas)), areas.index(min(areas)))

def max_processors(e_we, e_sn): # for smallest-sized domain
    e_we, e_sn = int(e_we), int(e_sn)
    if e_we <= 0 or e_sn <= 0:
        raise ValueError("e_we or e_sn are not positive - Invalid arguments")
    val = (e_we / 25) * (e_sn / 25)
    return math.floor(val)

def min_processors(e_we, e_sn): # for largest-sized domain
    e_we, e_sn = int(e_we), int(e_sn)
    if e_we <= 0 or e_sn <= 0:
        raise ValueError("e_we or e_sn are not positive - Invalid arguments")
    val = (e_we / 100) * (e_sn / 100)
    return math.ceil(val)

try:
    max_dom = int(find_values_for_term(main_path, file_name1, dom_size)[0])
    e_we = find_values_for_term(main_path, file_name1, terms[0])
    e_sn = find_values_for_term(main_path, file_name1, terms[1])
    
    largest_idx, smallest_idx = get_largest_smallest(e_we, e_sn, max_dom)

    min_procs = min_processors(e_we[smallest_idx], e_sn[smallest_idx])
    max_procs = max_processors(e_we[largest_idx], e_sn[largest_idx])

    print(f"MIN processors: {min_procs}")
    print(f"MAX processors: {max_procs}")

except ValueError as ve:
    print(f"ValueError: {ve}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# https://forum.mmm.ucar.edu/threads/choosing-an-appropriate-number-of-processors.5082/ for processor calculation

n_procs = find_values_for_term(main_path,file_name3,"processors",1)
if not (min_procs <= n_procs ):
        raise ValueError(f"Invalid minimum number of processors {n_procs}") 
if n_procs > max_procs:
    entry = input(f"You are exceeding the maximum number of processors {max_procs}: by using {n_procs}. Are you sure? y/n")
    if entry.upper() != "Y":
        raise ValueError(f"Invalid maximum number of processors {n_procs}")
print(f"Now using: {n_procs}")
print("-----")

############################################### 
# Check matching keys in wrf and wps files
############################################### 

def find_common_vals(directory, filename1, filename2, size): 
    os.chdir(directory)
    try:
        with open(filename1, 'r') as file1:
            lines1 = file1.readlines()
        
        with open(filename2, 'r') as file2:
            lines2 = file2.readlines()

        # Create dictionaries to store terms and their corresponding values
        dict1 = {}
        dict2 = {}
        
        for line in lines1:
            parts = [part.strip() for part in line.strip().split('=')]
            if len(parts) == 2:
                term, val = parts
                values = [v.strip() for v in val.split(',')]
                values = [x for x in values if x != '']
                dict1[term] = values
        
        for line in lines2:
            parts = [part.strip() for part in line.strip().split('=')]
            if len(parts) == 2:
                term, val = parts
                values = [v.strip() for v in val.split(',')]
                values = [x for x in values if x != '']
                dict2[term] = values

        common_terms = set(dict1.keys()) & set(dict2.keys())
        common = []

        for term in common_terms:
            values1 = dict1[term][:size]
            values2 = dict2[term][:size]
            if values1 == values2:
                common.append((term, values1))
            else: 
                print(f"WARNING: wps and wrf input files do not have the same {term}")
        
        if common:
            return common
        else:
            print("Empy list, check for missing or empty files.")
    
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

vals = find_common_vals(main_path,file_name1, file_name2, max_dom) # to check if wrf and wps input files are ok

############################################### 
# Check nested domains size validity 
############################################### 

# max_doms e_we and e_sn are already defined -> map lists to use integers 
i_parent = list(map(int, find_values_for_term(main_path, file_name1, "i_parent_start", single=0)))[:max_dom]
j_parent = list(map(int, find_values_for_term(main_path, file_name1, "j_parent_start", single=0)))[:max_dom]
parent_grid_ratio = list(map(int, find_values_for_term(main_path, file_name1, "parent_grid_ratio", single=0)))[:max_dom]
parent_id = list(map(int, find_values_for_term(main_path, file_name1, "parent_id", single=0)))[:max_dom]
e_we_aux = list(map(int, find_values_for_term(main_path, file_name1, "e_we", single=0)))[:max_dom]
e_sn_aux = list(map(int, find_values_for_term(main_path, file_name1, "e_sn", single=0)))[:max_dom]


def grid_side_ratios(parent_index, child_index):
    return  (e_sn_aux[child_index]-1) % parent_grid_ratio[child_index] == 0 and (e_we_aux[child_index]-1) % parent_grid_ratio[child_index] == 0

def does_it_fit(parent_index, child_index):
    child_true_size = [e_we_aux[parent_index]/parent_grid_ratio[child_index], e_sn_aux[child_index]/parent_grid_ratio[child_index]]
    return e_we_aux[parent_index] > i_parent[child_index] + child_true_size[0] and e_sn_aux[parent_index] > j_parent[child_index] + child_true_size[1]

def parent_finder():
    n = 1 
    for element in parent_id[1:]:
        if grid_side_ratios(element-1 ,n) and does_it_fit(element-1 ,n):
            n += 1
            continue
        else:
            raise ValueError(f"Incorrect size: Nested domain {n}")
    print(f"Valid nested domain sizes: {n} domains in use")
    
############################################### 
# change files automatically based on input 
############################################### 

def update_file_with_values(file_name, terms, values):
    # Check that terms and values lists are of the same length
    if len(terms) != len(values):
        raise ValueError("The length of 'terms' and 'values' must be the same.")
    
    # Read the current contents of the file
    with open(file_name, 'r') as file:
        lines = file.readlines()
    
    # Create a dictionary from terms and values
    term_value_dict = dict(zip(terms, values))
    
    # Update lines based on the terms
    updated_lines = []
    for line in lines:
        # Split line into term and value
        if '=' in line:
            term, value = line.split('=', 1)
            term = term.strip()
            value = value.strip()
            
            # If the term is in our dictionary, replace the value
            if term in term_value_dict:
                updated_lines.append(f"{term}={term_value_dict[term]}\n")
            else:
                updated_lines.append(line)
        else:
            updated_lines.append(line)
    
    # Write the updated contents back to the file
    with open(file_name, 'w') as file:
        file.writelines(updated_lines)


############################################### 
# Simulation time and operating mode 
############################################### 

def changer():
    # setup the correct date format based on env variables
    start_date = os.environ.get('START_DATE')  # strings
    end_date = os.environ.get('END_DATE')

    date_format = '%Y-%m-%d'
    date_format_with_time = '%Y-%m-%d_%H:%M:%S'

    def is_valid_date(date_str, date_format):
        try:
            datetime.strptime(date_str, date_format)  # see if format is right
            return True
        except ValueError:
            return False

    def convert_to_midnight(date_str, date_format):
        try:
            # Parse the date string
            date_obj = datetime.strptime(date_str, date_format)
            # Set time to midnight
            date_obj = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
            return date_obj
        except ValueError:
            return None

    # Validate and convert start_date
    if start_date is None:
        raise ValueError("START_DATE environment variable is empty")
    elif is_valid_date(start_date, date_format):
        start_date = convert_to_midnight(start_date, date_format)
    elif is_valid_date(start_date, date_format_with_time):
        start_date = datetime.strptime(start_date, date_format_with_time)
    else:
        raise ValueError("Invalid START_DATE format")

    # Validate and convert end_date
    if end_date is None:
        raise ValueError("END_DATE environment variable is empty")
    elif is_valid_date(end_date, date_format):
        end_date = convert_to_midnight(end_date, date_format)
    elif is_valid_date(end_date, date_format_with_time):
        end_date = datetime.strptime(end_date, date_format_with_time)
    else:
        raise ValueError("Invalid END_DATE format")

    ############################################### 
    # Operating mode - forecast or historic 
    ###############################################  

    utc_now = datetime.now(timezone.utc) # for sake of consistency, will use utc time 
    utc_now = datetime(utc_now.year, utc_now.month, utc_now.day ,utc_now.hour,utc_now.minute, utc_now.second) # this stops the non static date error  

    min_hours = timedelta(hours=7)
    max_period = timedelta(days = 3285) # approx 9 years 
    historic_period = timedelta(days=7)
    simulation_mode = ""
    time_interval = 0


    if (utc_now - start_date) <= timedelta(seconds=10) or (start_date >= end_date):
        raise ValueError(f"Invalid dates ; UTC time is now {utc_now}")
    
    elif (utc_now - start_date) < historic_period:
        simulation_mode = "forecast"
     
        if (utc_now - start_date) <= min_hours:
            print("WARNING: Start date is too close to data availability -> check https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl for files before proceeding!")
        
        ############################################### 
        # Change instructions.txt
        ############################################### 
        instructions_terms = ["year", "month", "day", "hour", "mode", "forecast", "jump"] 
        instructions_values = [start_date.year, start_date.month, start_date.day, start_date.hour, simulation_mode, "", ""]

        if (end_date-start_date) > timedelta(hours=384):
            raise ValueError("Forecast period exceeded")
        if (end_date-start_date) % timedelta(hours=6) == timedelta():
            instructions_values[6] = 6
            time_interval = 21600
            instructions_values[5] = int((end_date-start_date).total_seconds() // 3600)
        elif (end_date-start_date) % timedelta(hours=3) == timedelta():
            instructions_values[6] = 3 
            time_interval = 10800 
            instructions_values[5] = int((end_date-start_date).total_seconds() // 3600)
        else: 
            raise ValueError ("Interval must be divisible into 3h intervals (or multiples of 3)")
        print(f"WARNING: Based on provided date divisibility, will use {instructions_values[6]}h time interval for forecast mode.") # just to make sure 

        update_file_with_values(file_name3, instructions_terms, instructions_values) # alter instructions for new file 

    else: 
        simulation_mode = "historic"
        if (utc_now - start_date) > max_period:
            raise ValueError(f"Invalid historic date -> max is 9 years back or {utc_now - max_period}")
        # alter instructions.txt with correct values for historic mode 

        if (end_date-start_date) % timedelta(hours=6) != timedelta():
            raise ValueError("By default, historic mode data comes in 6h intervals. Change your dates to have an interval divisible by 6h")

        instructions_terms = ["year", "month", "day", "final_year", "final_month", "final_day", "mode"] 
        alt_date = end_date - timedelta(days=1) # by default this date is one day less than the end date
        instructions_values = [start_date.year, start_date.month, start_date.day, alt_date.year, alt_date.month, alt_date.day, simulation_mode]
        time_interval = 21600
        update_file_with_values(file_name3, instructions_terms, instructions_values) # alter instructions for new file

    ############################################### 
    # Change wps_input.txt
    ############################################### 

    wps_terms = ["start_date", "end_date" , "interval_seconds"]
    aux_date1 = start_date.strftime("%Y-%m-%d_%H:%M:%S") # this is needed for formating 
    aux_date2 = end_date.strftime("%Y-%m-%d_%H:%M:%S") # fstring doesn't accept operation inside 
    print(aux_date1, aux_date2)

    wps_values = [ f"'{aux_date1}',"*max_dom , f"'{aux_date2}',"*max_dom , f"{time_interval},"]
    update_file_with_values(file_name1, wps_terms, wps_values)

    ############################################### 
    # Change wrf_input.txt
    ############################################### 

    wrf_terms = ["start_year", "start_month", "start_day", "start_hour", "start_minute", "start_second",
                 "end_year", "end_month", "end_day", "end_hour", "end_minute", "end_second",
                 "run_days", "run_hours", "run_minutes", "run_seconds",
                 "interval_seconds"]
    
    time_difference = end_date - start_date
    # setup terms 
    wrf_values = [f"{start_date.year}," * max_dom, f"{start_date.month}," * max_dom, f"{start_date.day}," * max_dom, f"{start_date.hour}," * max_dom, f"{start_date.minute}," * max_dom, f"{start_date.second}," * max_dom,
    f"{end_date.year}," * max_dom, f"{end_date.month}," * max_dom, f"{end_date.day}," * max_dom, f"{end_date.hour}," * max_dom, f"{end_date.minute}," * max_dom, f"{end_date.second}," * max_dom,
    f"{time_difference.days},", f"{time_difference.seconds // 3600},", f"{(time_difference.seconds % 3600) // 60},", f"{time_difference.seconds % 60},",
    f"{time_interval},"]

    update_file_with_values(file_name2, wrf_terms, wrf_values)
    
    return simulation_mode

############################################### 
# Coordinates and critical terms
############################################### 

def coordinates(mode):
        if mode != "forecast":
            return "Domain partition skipped, not in forecast mode. Will use full domain."
          
        coord_terms3 = ["left", "right", "bot", "top"]
        coord_terms1 = ["e_we", "e_sn", "dx", "dy", "ref_lat", "ref_lon"]
        coord_aux = [float(find_values_for_term(main_path, file_name1, x,1)) for x in coord_terms1]

        # to guarantee that the biggest coordinate for sn or we is chosen -> unecessary bc domains get smaller inisde parent domain
        #aux = [max(find_values_for_term(main_path, file_name1, x)[:max_dom]) for x in ["e_we", "e_sn"]]
        #coord_aux[0] = float(aux[0])
        #coord_aux[1] = float(aux[1])
        
        # Convert ref_lat from degrees to radians for cosine calculation
        ref_lat_rad = math.radians(coord_aux[4])

        # Calculate North and South boundaries using e_sn and dy
        n_bound = coord_aux[4] + ((coord_aux[1] - 1) * coord_aux[3]) / 111000.0
        s_bound = coord_aux[4] - ((coord_aux[1] - 1) * coord_aux[3]) / 111000.0

        # Calculate East and West boundaries using e_we and dx, with correct cosine for longitude
        e_bound = coord_aux[5] + ((coord_aux[0] - 1) * coord_aux[2]) / (111000.0 * math.cos(ref_lat_rad))
        w_bound = coord_aux[5] - ((coord_aux[0] - 1) * coord_aux[2]) / (111000.0 * math.cos(ref_lat_rad))

        update_file_with_values(file_name3,coord_terms3,[math.floor(w_bound),math.ceil(e_bound),math.floor(s_bound),math.ceil(n_bound)])

        # Check if the calculated bounds are outside the domain coordinates
        
        print(f"Domain coords: s->{round(s_bound,2)}° ; n->{round(n_bound,2)}° ; w->{round(w_bound,2)}° ; e->{round(e_bound,2)}°")
        return(f"Simulation coords: s->{math.floor(s_bound)}° ; n->{math.ceil(n_bound)}° ; w->{math.floor(w_bound)}° ; e->{math.ceil(e_bound)}°")

################## In order to see if all needed terms exits 

def critical_terms():
    crit_terms = ["year", "month", "day", "processors", "mode", "hour", "left", "right", "top", "bot", "forecast", "jump", "final_year", "final_month", "final_day"]
    for element in crit_terms:
        find_values_for_term(main_path, file_name3, element, 0)
    
    update_file_with_values(file_name1, ["geog_data_path"], ["'../WPS_GEOG/',"]) # THESE PATHS MUST BE THERE 
    update_file_with_values(file_name1, ["opt_output_from_metgrid_path"], ["'/home/swe/Build_WRF/WPS-4.6.0/METGRIB_FILES',"])

############################################### 
# Testing zone 
############################################### 

mode = changer() # set forecast or historic mode 
update_file_with_values(file_name3, ["mode"], [mode]) # changes values in instructions.txt
print(f"{mode} mode chosen")
print("-----")
print(coordinates(mode)) # To give estimate on coordinates used 
critical_terms() # To ensure right internal architecture
print("-----")
parent_finder() # for validity of nested domains 

print("-----")
order = input("Do you want to proceed with the simulation (Y or N) -> CHECK ALL 3 files prior to continuing!")
if order.upper() != "Y":
    sys.exit(1)

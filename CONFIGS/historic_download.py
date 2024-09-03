import os 
import requests
from urllib.parse import urlparse
import datetime

################### global variables -> won't change 
main_path = "/home/swe/Build_WRF/CONFIGS"
install_path = "/home/swe/Build_WRF/WPS-4.6.0/GRIB_FILES"
instructions = "instructions.txt"
jump = 6
year, month, day, final_year, final_month, final_day = 0,0,0,0,0,0
terms = ("year", "month", "day", "final_year", "final_month", "final_day")

################### get instructions from instructions.txt

def find_value_for_term(directory, filename, search_term):
    os.chdir(directory)
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        value = None
        for line in lines:
            # Strip any leading/trailing whitespace and split the line at '='
            parts = [part.strip() for part in line.strip().split('=')]
            
            if len(parts) == 2: # each var will have ONLY 1 numerical value associated with it 
                term, val = parts
                if term == search_term:
                    value = val
                    break

        if value is not None:
            return value
        else:
            print("Parameter missing from instructions.txt")
            raise ValueError
    
    except FileNotFoundError:
        print(f"The file {filename} was not found in directory {directory}.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_vals(directory, filename, terms):
    for term in terms:
        if term in globals():
            # Find the value for the term
            value = find_value_for_term(directory, filename, term)
            # Try to convert the value to an integer if possible
            try:
                globals()[term] = int(value)
            except ValueError:
                globals()[term] = value
        else:
            print(f"Parameter '{term}' missing from instructions.txt")
            raise ValueError

get_vals(main_path, instructions, terms) # this changes the values of the global vars 

################### Read main instructions  

os.chdir(install_path) # change to the install directory 

start_date = datetime.date(year, month, day) # set significant dates 
end_date = datetime.date(final_year, final_month, final_day)

if end_date < start_date:
    raise ValueError("Invalid arguments -> check if end_date is after start_date")
print("Valid date formats -> proceeding")

def converter(arg, size=1):  # Function to put dates in the right format
    arg = str(arg)
    return arg.zfill(size)

def get_links(year, month, day, hour):
    url = f"https://data.rda.ucar.edu/d083003/{year}/{year}{converter(month, 2)}/gdas1.fnl0p25.{year}{converter(month, 2)}{converter(day, 2)}{converter(hour, 2)}.f00.grib2"
    return url

def get_links_forecast(year, month, day, final_year, final_month, final_day, jump=6):
    start_date = datetime.date(year, month, day)
    end_date = datetime.date(final_year, final_month, final_day)
    links = []

    delta = datetime.timedelta(days=1)
    
    # Iterate over the range of dates
    while start_date <= end_date:
        # Generate links for the specific hours of the current day
        for hour in range(0, 24, jump):
            link = get_links(start_date.year, start_date.month, start_date.day, hour)
            links.append(link)
        start_date += delta

    links.append(get_links(start_date.year, start_date.month, start_date.day, 0))
    return links

################### Download files to the correct directory


def download_file(url, destination_directory):
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Extract filename from headers or URL
        filename = url.split('/')[-1]
        # Ensure the directory exists
        os.makedirs(destination_directory, exist_ok=True)
        
        # Full path to save the file
        destination = os.path.join(destination_directory, filename)
        
        print(f"Downloading: {url}")
        
        # Write the content in chunks to avoid loading large files into memory
        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"File downloaded successfully and saved to {destination}")
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")

def downloads(links, install_lib):
    for url in links:
        download_file(url, install_lib)

# Example usage
links = get_links_forecast(year, month, day, final_year, final_month, final_day)
downloads(links, install_path)

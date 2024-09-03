import os 
import requests
from urllib.parse import urlparse

################### global variables -> won't change 
main_path = "/home/swe/Build_WRF/CONFIGS"
install_path = "/home/swe/Build_WRF/WPS-4.6.0/GRIB_FILES"
instructions = "instructions.txt"
jump = 3
year, month, day, hour, left, right, top, bot, forecast = 0,0,0,0,0,0,0,0,0 # initialize variables 
terms = ("year", "month", "day", "hour", "left", "right", "top", "bot", "forecast", "jump")

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
            
            if len(parts) == 2: # each var will have ONLY 1 numeriacal value associated with it 
                term, val = parts
                if term == search_term:
                    value = val
                    break

        if value is not None:
            return value
        else:
            print("Paramether missing from inscructions.txt")
            raise ValueError
    
    except FileNotFoundError:
        print(f"The file {filename} was not found in directory {directory}.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_vals(directory, filename, terms):
    for term in terms:
        # print(term)
        if term in globals():
            # Find the value for the term
            value = find_value_for_term(directory, filename, term)
            # Try to convert the value to an integer if possible
            try:
                globals()[term] = int(value)
                # print(globals()[term])
            except ValueError:
                globals()[term] = value
        else:
            print(f"Parameter '{term}' missing from instructions.txt")
            raise ValueError

get_vals(main_path,instructions,terms) # this changes the values of the global vars 

################### Read main instructions  

def converter(arg, size=1): # to put dates in right format 
    arg = str(arg)
    return arg.zfill(size)

def get_links(year, month, day, hour, left=0, right=360, top=90, bot=-90, forecast=0): 
    # Validate the forecast value
    if forecast % 3 != 0 or not (0 <= forecast <= 384):
        print("INVALID forecast arguments")
        raise ValueError
 
    # Build the URL
    url = (
        f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?"
        f"file=gfs.t{converter(hour, 2)}z.pgrb2.0p25.f{converter(forecast, 3)}&"
        f"all_lev=on&all_var=on&"
        f"subregion=&"
        f"leftlon={left}&rightlon={right}&toplat={top}&bottomlat={bot}&"
        f"dir=%2Fgfs.{year}{converter(month, 2)}{converter(day, 2)}%2F{converter(hour, 2)}%2Fatmos"
    )

    return url

def get_links_forescast(year, month, day, hour, left=0, right=360, top=90, bot=-90, forecast_len = 0):
    if forecast_len < 0:
        print("INVALID forecast lenght arguments")
        raise ValueError
    
    links = [get_links(year, month, day, hour, left, right, top, bot, x) for x in range(0,forecast_len+1,jump)] 
    return links

################### Download files to the correct directory

def get_filename_from_headers(response):
    if 'Content-Disposition' in response.headers:
        content_disposition = response.headers['Content-Disposition']
        filename = content_disposition.split('filename=')[-1].strip('"')
        return filename
    return None

def get_filename_from_url(url):
    return os.path.basename(urlparse(url).path)

def download_file(url, destination_directory):
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Extract filename from headers or URL
        filename = get_filename_from_headers(response)
        if filename is None:
            filename = get_filename_from_url(url)
        
        if not filename:
            print(f"Unable to determine filename from URL: {url}")
            return
        
        # Full path to save the file
        destination = os.path.join(destination_directory, filename)
        
        # Ensure the directory exists
        os.makedirs(destination_directory, exist_ok=True)
        print(f"Dowloading: {url}")
        
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

########################################### Working area 

links = get_links_forescast(year, month, day, hour, left, right, top, bot, forecast)
downloads(links, install_path)


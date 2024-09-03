import os

################### base variables

main_path = "/home/swe/Build_WRF/CONFIGS"
term = "mode" # possible values are "forecast" and "historic"
instructions = "instructions.txt"

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

print(find_value_for_term(main_path,instructions,term))
import matplotlib.pyplot as plt
import numpy as np
import io
import glob
import os
import re
from datetime import datetime

# to extract data using a directory:
directory_path = r"G:\My Drive\ACCL_L3B_3180"

# checking if the directory is found
# if os.path.isdir(directory_path):
#   print("Google Drive directory found.")
# else: 
#   print("Directory not found.")

# print all of the file names with "_QUENCH" in the folder using a loop (using glob module)
results = glob.glob(directory_path + '/**/*QUENCH.txt', recursive=True) # force this to have a number before _QUENCH
print(f"Found {len(results)} matching QUENCH text files:")
# print(results) # results is a list
filtered_results = [f for f in results if re.search(r"\d+_QUENCH", f)]
print(f"Found {len(filtered_results)} matching '##_QUENCH' text files:")
print(filtered_results)


for file in filtered_results: 
    print("\nProcessing file: " + file)
    
    # getting PV and timestamp information from {file}
    # line below splits the file in to 4 parts (after the '\') and gets the last part (filename)
    filename = file.split("\\", 4)[-1].replace('.txt','') 
    print(filename)
    parts = filename.split('_') # splits the filename into parts at each '_'
    pv_base = parts[0] + ":" + parts[1] + ":" + parts[2]    # ex: pt(1): ACCL, pt(2): L3B, pt(3):3180
    timestamp_raw = parts[3] + "_" + parts[4]               # ex: pt(3): 20221028, pt(4): 235218
    # line below formats the timestamp to match the file layout
    timestamp = datetime.strptime(timestamp_raw, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d_%H:%M:%S.")
    print("PV label: " + pv_base)
    print("Timestamp: " + timestamp)

    # constructing PV label strings
    cavity_faultname = pv_base + ':CAV:FLTAWF'  # ex: ACCL:L3B:3180:CAV:FLTAWF
    forward_pow = pv_base + ':FWD:FLTAWF'       # ex: ACCL:L3B:3180:FWD:FLTAWF
    reverse_pow = pv_base + ':REV:FLTAWF'       # ex: ACCL:L3B:3180:REV:FLTAWF
    decay_ref = pv_base + ':DECAYREFWF'         # ex: ACCL:L3B:3180:DECAYREFWF    
    time_range = pv_base + 'CAV:FLTTWF'         # ex: ACCL:L3B:3180:CAV:FLTTWF

    # creating a function to extract the waveform data from each file
    def extracting_data(file, faultname, timestamp): # change this so that we do not need the timestamp, we search for it later
        section_lines = []
        with open(file, 'r') as f:
            for line in f:
                if f"{faultname} {timestamp}" in line:
                    section_lines.append(line)
        
        if not section_lines:
           print("No matching lines found.")
        else:
            section_data = io.StringIO("".join(section_lines))
            num_cols = len(section_lines[0].strip().split())
            usecolumns = list(range(2, num_cols))
            data_array = np.loadtxt(section_data, delimiter = None, usecols=usecolumns)
            print(f"{faultname} data was extracted: first point is {data_array[0]}, and last point is {data_array[-1]}")

            return data_array
    
    # extract each waveform using defined function
    cavity_data = extracting_data(file, cavity_faultname, timestamp)
    forward_data = extracting_data(file, forward_pow, timestamp)
    reverse_data = extracting_data(file, reverse_pow, timestamp)
    decay_data = extracting_data(file, decay_ref, timestamp)
    # time_data = extracting_data(file, time_range, timestamp)     # timestamp for time range is different






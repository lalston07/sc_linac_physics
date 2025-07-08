import matplotlib.pyplot as plt
import numpy as np
import glob
import re
import pandas as pd
from datetime import datetime

# step one - loop through files and extract timestamp data for the x-axis
directory_path = r"G:\My Drive\ACCL_L3B_3180"
results = glob.glob(directory_path + '/**/*QUENCH.txt', recursive=True) # force this to have a number before _QUENCH
# print(f"Found {len(results)} matching QUENCH text files:")
# print(results) 
quench_files = [f for f in results if re.search(r"\d+_QUENCH", f)]
print(f"Found {len(quench_files)} matching '##_QUENCH' text files:")
print(quench_files)
timestamps = []
for file in quench_files:
    # line below splits the file in to 4 parts (after the '\') and gets the last part (filename)
    filename = file.split("\\", 4)[-1].replace('.txt','') 
    parts = filename.split('_') # splits the filename into parts at each '_'
    timestamp_raw = parts[3]   # ex: pt(3): 20221028, pt(4): 235218
    # line below formats the timestamp to match the file layout
    timestamp = datetime.strptime(timestamp_raw, "%Y%m%d")
    timestamps.append(timestamp)

# step two - converting list to datetime or series object
# timestamp_index = pd.to_datetime(timestamps)  # pandas datetime object
timestamp_index = pd.Series(timestamps)         # pandas series object

# step three - count the number of quenches per timestamp for the y-axis
# frequency = timestamp_index.value_counts()
frequency = timestamp_index.count()
print(frequency)

# # step four - create a Data Frame using two lists (timestamps and count of quenches)
# df_frequency_time = pd.DataFrame({'time' : timestamps, 'frequency' : frequency})
# print(df_frequency_time)

# # step five - plot the quench frequency data
# plt.figure(figsize=(12,6))
# plt.plot(df_frequency_time['time'], df_frequency_time['frequency'], marker='--')
# # alternative plot method: "df_frequency_time.plot('time', 'frequency')"
# plt.xlabel("")
# plt.ylabel("")
# plt.title("Quench Frequency Over Time")
# plt.grid(True)
# plt.tight_layout()
# plt.show()


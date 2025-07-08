import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

filename = 'ACCL_L3B_3180_20220630_164905_QUENCH.txt'
timestamp = '2022-06-30_16:49:05.440831'
time_timestamp = '2022-06-30_15:46:04.712966'

# PV labels
cavity_faultname = 'ACCL:L3B:3180:CAV:FLTAWF'
forward_pow = 'ACCL:L3B:3180:FWD:FLTAWF'
reverse_pow = 'ACCL:L3B:3180:REV:FLTAWF'
decay_ref = 'ACCL:L3B:3180:DECAYREFWF'
time_range = 'ACCL:L3B:3180:CAV:FLTTWF'

def extracting_data(path_name, faultname, timestamp):
    usecols = list(range(2, 2051))  
    data_array = pd.read_csv(path_name, usecols=usecols, skiprows=51, nrows=1, header=None)

    values = data_array.values[0]  # extracting the first row as a numpy array

    print(f"{faultname} Information:")
    print(f"Length: {len(values)}")
    print(f"First: {values[0]}, Last: {values[-1]}")
    print(f"Min: {np.min(values)}, Max: {np.max(values)}\n")

    return values

cavity_data = extracting_data(filename, cavity_faultname, timestamp)

plt.figure(figsize=(14,6))
plt.plot(cavity_data, label="Cavity", color='blue', linewidth=2)
plt.xlabel("Sample Index")
plt.ylabel("Amplitude (MV)")
plt.title("Cavity Quench Waveform")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

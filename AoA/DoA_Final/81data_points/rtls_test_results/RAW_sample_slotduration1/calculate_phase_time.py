import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import math

new_data = pd.read_csv('info_dec.csv')

data_size = len(new_data)
N = int(data_size/288)
info_per_ant =[]
for n in range(N):
    for k in range(0 + n*288, 288*(n+1), 4):
        info_per_ant.append({"pkt": new_data['pkt'][k], "channel": new_data['Channel'][k], "phi_ant1": new_data['phi_info'][k + 3],
                             "phi_ant2": new_data['phi_info'][k], "phi_ant3": new_data['phi_info'][k + 1], "phi_ant4": new_data['phi_info'][k + 2],
                             "t_ant1": new_data['time_stamp'][k+3], "t_ant2": new_data['time_stamp'][k], "t_ant3": new_data['time_stamp'][k+1],
                             "t_ant4": new_data['time_stamp'][k+2],
                             "meg_ant1": new_data['mag_info'][k + 3], "meg_ant2": new_data['mag_info'][k],
                             "meg_ant3": new_data['mag_info'][k + 1], "meg_ant4": new_data['mag_info'][k + 2]})
result = pd.DataFrame(info_per_ant)
result.to_csv('info_per_ant.csv', index=False)
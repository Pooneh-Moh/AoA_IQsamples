from pyargus.directionEstimation import *
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import math

def cal_magnitude(q_value,i_value):
    return math.sqrt(math.pow(q_value,2)+math.pow(i_value,2))

new_data = pd.read_csv('04_06_2021_14_08_36_rtls_raw_iq_samples_f88a5e2d7808_0.csv')
angle_res = []
angle_per_anetnna =[]
time_stamp = []
info =[]
info_per_ant =[]
channel = []
data_size = len(new_data)
N = int(data_size/624)
print('Number of pakts are, but we use int(N/2)', N, int(N/2))
t = np.arange(0, 157*33, 0.25)
for n in range(33):
    for i in range(40+n*624, 624*(n+1), 8):
        for j in range(i, i+4):
            info.append({"pkt": n, "Channel": new_data['channel'][j], "ant_info": complex(new_data['i'][j], new_data['q'][j]),
                         "phi_info": np.arctan2(new_data['i'][j], new_data['q'][j]) * 180 / np.pi,
                         "mag_info":cal_magnitude(new_data['q'][j], new_data['i'][j]),
                         "theta_info": np.degrees(np.arcsin(np.arctan2(new_data['i'][j], new_data['q'][j]) /120)), "time_stamp": t[j]})
    info_dec = pd.DataFrame(info)
    info_dec.to_csv('info_dec_4.csv', index=False)
print('Finished')





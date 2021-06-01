from pyargus.directionEstimation import *
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
from itertools import chain
import math

init_notebook_mode(connected=True)
cf.go_offline()

d = 4.17 # Inter element spacing [lambda]
M = 4  # number of antenna elements in the antenna system (ULA)
theta = 45  # incident angle of the test signal [deg]
Landa = 12.5

def cal_magnitude(q_value,i_value):
    return math.sqrt(math.pow(q_value,2)+math.pow(i_value,2))

new_data = pd.read_csv('03_26_2021_16_55_16_rtls_raw_iq_samples_f88a5e2d7808_0.csv')
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
            # all_ant.append(complex(new_data['i'][j], new_data['q'][j]))
            # all_phi.append(np.arctan2(new_data['i'][j], new_data['q'][j]) * 180 / np.pi)
            # all_mag.append(cal_magnitude(new_data['q'][j], new_data['i'][j]))
            # all_theta.append(np.degrees(np.arcsin(np.arctan2(new_data['i'][j], new_data['q'][j]) /120))) # teta = arcsin(landa* (phase/(2pi*d)))
            # time_stamp.append(t[j])
            # channel.append(new_data['channel'][j])
            info.append({"pkt": n, "Channel": new_data['channel'][j], "ant_info": complex(new_data['i'][j], new_data['q'][j]),
                         "phi_info": np.arctan2(new_data['i'][j], new_data['q'][j]) * 180 / np.pi,
                         "mag_info":cal_magnitude(new_data['q'][j], new_data['i'][j]),
                         "theta_info": np.degrees(np.arcsin(np.arctan2(new_data['i'][j], new_data['q'][j]) /120)), "time_stamp": t[j]})
    info_dec = pd.DataFrame(info)
    info_dec.to_csv('info_dec.csv', index=False)
print('Finished')





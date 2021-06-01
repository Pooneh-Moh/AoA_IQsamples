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

def cal_magnitude(q_value,i_value):
    return math.sqrt(math.pow(q_value,2)+math.pow(i_value,2))

new_data = pd.read_csv('C:/ti/simplelink_cc13x2_26x2_sdk_4_40_04_04/tools/ble5stack/rtls_agent/examples/3ANT/rtls_aoa_iq_with_rtls_util_export_into_csv_3ant_AoA_log/04_09_2021_17_31_26_rtls_raw_iq_samples_f88a5e2d7808_0.csv')
angle_res = []
angle_per_anetnna =[]
time_stamp = []
info =[]
info_per_ant =[]
channel = []
data_size = len(new_data)
N = int(data_size/624)
print('Number of pakts are', N, int(N/2))
t = np.arange(0, 157*N, 0.25)
for n in range(N):
    for i in range(40+n*624, 624*(n+1), 8):
        for j in range(i, i+4):
            info.append({"pkt": n, "Channel": new_data['channel'][j], "ant_info": complex(new_data['i'][j], new_data['q'][j]),
                         "phi_info": np.arctan2(new_data['i'][j], new_data['q'][j]) * 180 / np.pi,
                         "mag_info":cal_magnitude(new_data['q'][j], new_data['i'][j]),
                         "theta_info": np.degrees(np.arcsin(np.arctan2(new_data['i'][j], new_data['q'][j]) /120)), "time_stamp": t[j],
                         "sample_idx":new_data['sample_idx'][j]})
    info_dec = pd.DataFrame(info)
    # info_dec.to_csv('info_dec_AoA_3ANT.csv', index=False)
print(info_dec)
print('Finished')





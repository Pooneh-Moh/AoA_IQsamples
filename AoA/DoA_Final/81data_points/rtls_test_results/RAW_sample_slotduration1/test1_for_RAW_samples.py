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
phi_1 = []
phi_2 = []
phi_3 = []
phi_4 = []
mag_2 = []
mag_1 = []
mag_3 = []
mag_4 = []
angle_res = []
all_ant = []
all_mag =[]
all_phi = []
all_theta = []
angle_per_anetnna =[]
time_stamp = []
info =[]
data_size = len(new_data)
N = int(data_size/624)
t = np.arange(0, 155*2, 0.25)
for n in range(2):
    for i in range(40+n*624, 611*(n+1), 8):
        for j in range(i, i+4):
            all_ant.append(complex(new_data['i'][j], new_data['q'][j]))
            all_phi.append(np.arctan2(new_data['i'][j], new_data['q'][j]) * 180 / np.pi)
            all_mag.append(cal_magnitude(new_data['q'][j], new_data['i'][j]))
            all_theta.append(np.degrees(np.arcsin(np.arctan2(new_data['i'][j], new_data['q'][j]) /120))) # teta = arcsin(landa* (phase/(2pi*d)))
            time_stamp.append(t[j])
            # print(j - (n+1)*j)
            info.append({"pkt": n, "Channel": new_data['channel'][j], "ant_info": complex(new_data['i'][j], new_data['q'][j]),
                         "phi_info": np.arctan2(new_data['i'][j], new_data['q'][j]) * 180 / np.pi,
                         "mag_info":cal_magnitude(new_data['q'][j], new_data['i'][j]),
                         "theta_info": np.degrees(np.arcsin(np.arctan2(new_data['i'][j], new_data['q'][j]) /120)), "time_stamp": t[j]})
            info_dec = pd.DataFrame(info)
            info_dec.to_csv('info_dec.csv', index=False)
        # print(info_dec)

    # print('j out',j)
    for k in range(0, len(all_ant), 4):
        phi_2.append(all_phi[k])
        phi_3.append(all_phi[k + 1])
        phi_4.append(all_phi[k + 2])
        phi_1.append(all_phi[k + 3])
        mag_2.append(all_mag[k])
        mag_3.append(all_mag[k + 1])
        mag_4.append(all_mag[k + 2])
        mag_1.append(all_mag[k + 3])


    angle_per_anetnna.append({"pkt": n, "Channel": new_data['channel'][j], "Phase_ant1": np.average(phi_1), "Phase_ant2": np.average(phi_2),
                              "Phase_ant3": np.average(phi_3), "Phase_ant4": np.average(phi_4), "Magnitude_ant1": np.average(mag_1), "Magnitude_ant2": np.average(mag_2),
                              "Magnitude_ant3": np.average(mag_3), "Magnitude_ant4": np.average(mag_4)})
    results_per_ant = pd.DataFrame(angle_per_anetnna)
    # print(results_per_ant)
    results_per_ant.to_csv('Results_per_antenna.csv', index=False)
    angle_res.append({"pkt": n, "Channel": new_data['channel'][j],  "phase_all_antenna": np.average(all_phi)})
    result = pd.DataFrame(angle_res)
    result.to_csv('Average_phase_per_channel.csv', index=False)
npa_ang_final = np.average(all_phi)
npa_tet_final = np.average(all_theta)
angle_res_ave = []
angle_res_ave.append(
    {"Phi_Ave": npa_ang_final, "Theta_Ave": npa_tet_final})
angle = pd.DataFrame(angle_res_ave)
angle.to_csv('Final_ave_total.csv', index=False)
print('The phi final angle is', npa_ang_final,'\nThe tetha final angle is', npa_tet_final)



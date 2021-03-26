from pyargus.directionEstimation import *
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
from itertools import chain

init_notebook_mode(connected=True)
cf.go_offline()

d = 4.17 # Inter element spacing [lambda]
M = 4  # number of antenna elements in the antenna system (ULA)
theta = 45  # incident angle of the test signal [deg]
Landa = 12.5

new_data = pd.read_csv('C:/ti/simplelink_cc13x2_26x2_sdk_4_40_04_04/tools/ble5stack/rtls_agent/examples/rtls_aoa_iq_with_rtls_util_export_into_csv_A0A_log/03_17_2021_14_38_27_rtls_raw_iq_samples_f88a5e2d7808_0.csv')
ant_1 = []
ant_2 = []
ant_3 = []
ant_4 = []
phi_1 = []
phi_2 = []
phi_3 = []
phi_4 = []
tet_1 = []
tet_2 = []
tet_3 = []
tet_4 = []
angle_res = []
data_size = len(new_data)
N = int(data_size/44)
for n in range(N):
    for i in range(8+n*44, 43*(n+1), 4):
        ant_2.append(complex(new_data['i'][i], new_data['q'][i]))
        ant_3.append(complex(new_data['i'][i + 1], new_data['q'][i+1]))
        ant_4.append(complex(new_data['i'][i + 2], new_data['q'][i + 2]))
        ant_1.append(complex(new_data['i'][i + 3], new_data['q'][i + 3]))
        phi_2.append(np.arctan2(new_data['i'][i], new_data['q'][i]) * 180 / np.pi)
        phi_3.append(np.arctan2(new_data['i'][i + 1], new_data['q'][i + 1]) * 180 / np.pi)
        phi_4.append(np.arctan2(new_data ['i'][i + 2], new_data['q'][i + 2]) * 180 / np.pi)
        phi_1.append(np.arctan2(new_data['i'][i + 3], new_data['q'][i + 3]) * 180 / np.pi)
        tet_2.append(np.degrees(np.arcsin(np.arctan2(new_data['i'][i], new_data['q'][i]) /120))) # teta = arcsin(landa* (phase/(2pi*d)))
        tet_3.append(np.degrees(np.arcsin(np.arctan2(new_data['i'][i+1], new_data['q'][i+1]) / 120))) # when d = landa/3 and phase = arctan(Q/I)* pi/180
        tet_4.append(np.degrees(np.arcsin(np.arctan2(new_data['i'][i+2], new_data['q'][i+2]) / 120))) # therfore teta = arcsin(phase* 3/2pi)
        tet_1.append(np.degrees(np.arcsin(np.arctan2(new_data['i'][i+3], new_data['q'][i+3]) / 120)))

    npa_ang_final = (np.average(phi_1)+ np.average(phi_2) + np.average(phi_3) + np.average(phi_4))*0.25
    angle_res.append({"pkt": n, "angle_ant1": np.average(phi_1), "angle_ant2": np.average(phi_2), "angle_ant3": np.average(phi_3), "angle_ant4": np.average(phi_4), "Total_angle_average": npa_ang_final,
                      "tetha_ant1": np.average(tet_1), "tetha_ant2": np.average(tet_2), "tetha_ant3": np.average(tet_3), "tetha_ant4": np.average(tet_4)})
    # print('The average phi at pkt' , n, 'antenna','\n antenna 1', np.average(phi_1), '\n antenna 2', np.average(phi_2), '\n antenna 3', np.average(phi_3), '\n antenna 4', np.average(phi_4),)
    result = pd.DataFrame(angle_res)
    # result.to_csv('Average_phase_per_pkt3.csv', index=False)
npa_ang_final = (np.average(phi_1)+ np.average(phi_2) + np.average(phi_3) + np.average(phi_4))*0.25
npa_tet_final = (np.average(tet_1)+ np.average(tet_2) + np.average(tet_3) + np.average(tet_4))*0.25
print('The phi final angle is', npa_ang_final,'\nThe tetha final angle is', npa_tet_final)


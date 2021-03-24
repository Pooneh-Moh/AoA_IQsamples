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

new_data = pd.read_csv('C:/ti/simplelink_cc13x2_26x2_sdk_4_40_04_04/tools/ble5stack/rtls_agent/examples/rtls_aoa_iq_with_rtls_util_export_into_csv_log/02_25_2021_14_06_32_rtls_raw_iq_samples_f88a5e2d8f14_0.csv')

ant_1 = []
ant_2 = []
ant_3 = []
ant_4 = []
ant_ref = []
teta_1 = []
teta_2 = []
teta_3 = []
teta_4 = []
teta_ref = []
ant_final = []
data_size = len(new_data)
N = 112
calc = 0
for i in range(0, 560, 16):
    if (calc == 0) or (calc % 5 == 0):
        for j in range(0, 16):
            ant_ref.append(complex(new_data['i'][j], new_data['q'][j]))
            teta_ref.append(np.arctan2(new_data['i'][j], new_data['q'][j]) * 180 / np.pi)
            # print(i,j, calc)
            calc += 1

    elif (calc % 5 == 1):
        for j in range(0, 16):
            ant_1.append(complex(new_data['i'][j], new_data['q'][j]))
            teta_1.append(np.arctan2(new_data['i'][j], new_data['q'][j]) * 180 / np.pi)
            # print('------------------', i, j, calc)
            calc += 1

    elif (calc % 5 == 2):
        for j in range(0, 16):
            ant_2.append(complex(new_data['i'][j], new_data['q'][j]))
            teta_2.append(np.arctan2(new_data['i'][j], new_data['q'][j]) * 180 / np.pi)
            # print('********************', i, j, calc)
            calc += 1
    elif (calc % 5 == 3):
        for j in range(0, 16):
            ant_3.append(complex(new_data['i'][j], new_data['q'][j]))
            teta_3.append(np.arctan2(new_data['i'][j], new_data['q'][j]) * 180 / np.pi)
            # print('%%%%%%%%%%%%%%%%%%%%', i, j, calc)
            calc += 1
    elif (calc % 5 == 4):
        for j in range(0, 16):
            ant_4.append(complex(new_data['i'][j], new_data['q'][j]))
            teta_4.append(np.arctan2(new_data['i'][j], new_data['q'][j]) * 180 / np.pi)
            # print('@@@@@@@@@@@@@@@@@@@@@', i, j, calc)
            calc += 1

# ant_final.append(ant_ref)
ant_final.append(ant_1)
ant_final.append(ant_2)
ant_final.append(ant_3)
ant_final.append(ant_4)


teta_final = []
teta_final.append(teta_1)
teta_final.append(teta_2)
teta_final.append(teta_3)
teta_final.append(teta_4)
print(len(teta_final), len(ant_final))

## Calculate the phase diffrence between each antenna!
p1 = []
p2 = []
p3 = []
p4 = []
for i in range(len(ant_1)):
    multi1 = ant_1[i] * np.conj(ant_ref[i])
    multi2 = ant_2[i] * np.conj(ant_ref[i])
    multi3 = ant_3[i] * np.conj(ant_ref[i])
    multi4 = ant_4[i] * np.conj(ant_ref[i])
    p1.append(np.arctan2(multi1.real, multi1.imag)* 180/np.pi)
    p2.append(np.arctan2(multi2.real, multi2.imag)* 180/np.pi)
    p3.append(np.arctan2(multi3.real, multi3.imag)* 180/np.pi)
    p4.append(np.arctan2(multi4.real, multi4.imag)* 180/np.pi)

ant_1_ang = np.multiply(p1, 1/6*np.pi)
ant_2_ang = np.multiply(p2, 1/6*np.pi)
ant_3_ang = np.multiply(p3, 1/6*np.pi)
ant_4_ang = np.multiply(p4, 1/6*np.pi)
print('the average of each ', np.average(ant_1_ang), np.average(ant_2_ang), np.average(ant_3_ang), np.average(ant_4_ang))
incident_angles= np.arange(0,181,1)
# # Generate scanning vectors with the general purpose function
x = np.arange(0, M, 1) * d # x coordinates
y = np.zeros(M) # y coordinates

npa_ang_final = np.asarray(teta_final)
# Array response vector of the test signal
# a = np.exp(np.arange(0,M,1)*1j*2*np.pi*d*(1/Landa)*np.cos(np.deg2rad(theta)))
a = np.exp(np.arange(0,M,1)*1j*2*np.pi*d*(1/Landa))
angles = np.cos(np.deg2rad(npa_ang_final))
# # print(a[1], len(a), type(a))
# print('angle', len(angles), len(angles[0]))
angle_teta = []
for i in range(len(a)):
    angle_teta.append(a[i]*angles[i])
# print('angle_teta', len(angle_teta), len(angle_teta[0]))
#
flatten_list = list(chain.from_iterable(angle_teta))
#
noise = np.random.normal(0,np.sqrt(10**-1),(M,N))
noise2 = np.random.normal(0,np.sqrt(10**-1),(M,N*4))
soi_mat = noise + angle_teta
soi_mat2 = noise2 + flatten_list
#
R = (corr_matrix_estimate(soi_mat.T, imp="mem_eff"))
R2 = (corr_matrix_estimate(soi_mat2.T, imp="mem_eff"))
# print('R matrix', len(R), len(R[0]), '\n The R0 is', R[0])
#
scanning_vectors = gen_scanning_vectors(M, x, y, incident_angles)
MUSIC = DOA_MUSIC(R, scanning_vectors, signal_dimension = 1)
Bartlett = DOA_Bartlett(R, scanning_vectors)
MUSIC2 = DOA_MUSIC(R2, scanning_vectors, signal_dimension = 1)
Bartlett2 = DOA_Bartlett(R2, scanning_vectors)

axes = plt.axes()
# Plot results on the same fiugre
# DOA_plot(Bartlett, incident_angles, log_scale_min = -50, axes=axes, alias_highlight=False)
DOA_plot(MUSIC, incident_angles, axes=axes, alias_highlight=False)
DOA_plot(MUSIC2, incident_angles, axes=axes, alias_highlight=False)
axes.legend(("MUSIC", "MUSIC2"))
plt.show()
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

ant_ref = []
teta_ref = []
teta_final = []
ant_final = []
data_size = len(new_data)
N = 112
calc = 0
for i in range(0, 521, 104):
    for j in range(0, 40):
        ant_ref.append(complex(new_data['i'][j], new_data['q'][j]))
ant_ref_arr = np.asarray(ant_ref)
ant_ref_arr = np.reshape(ant_ref_arr, (6,40))

for j in range(6):
    for i in range(104*j+ 40,104*(j+1)):
        ant_final.append(complex(new_data['i'][i], new_data['q'][i]))
ant_final = np.asarray(ant_final)
ant_resh = ant_final.reshape(6, 64) # contains the first group of info
ant_1 = []
ant_2 = []
ant_3 = []
ant_4 = []
for i in range(len(ant_resh)):
    for j in range(16):
        ant_1.append(ant_resh[i][j])
        ant_2.append(ant_resh[i][j+16])
        ant_3.append(ant_resh[i][j + 32])
        ant_4.append(ant_resh[i][j + 48])

for i in range(len(ant_resh)):
    for j in range(16):
        multi = ant_resh[i]

dphi1 = []
for i in range(len(ant_ref_arr)):
    for j in range(len(ant_resh)):
        for k in range(16):
            multi1 = ant_resh[j][k] * np.conj(ant_ref_arr[i][k])
            dphi1.append(np.arctan2(multi1.real, multi1.imag)* 180/np.pi) #gives angle in degree
            # print(i,j, k)
dphi = np.asarray(dphi1)
dphi = np.reshape(dphi, (6,96)) # the phase difference of each antenna in 6 group
## Calculate the phase diffrence between each antenna!
dphi_1 = []
dphi_2 = []
dphi_3 = []
dphi_4 = []
for i in range(len(dphi)):
    for j in range(16):
        dphi_1.append(dphi[i][j])
        dphi_2.append(dphi[i][j + 16])
        dphi_3.append(dphi[i][j + 32])
        dphi_4.append(dphi[i][j + 48])

print(np.average(dphi_1), np.average(dphi_2), np.average(dphi_3), np.average(dphi_4))


# incident_angles= np.arange(0,181,1)
# # # Generate scanning vectors with the general purpose function
# x = np.arange(0, M, 1) * d # x coordinates
# y = np.zeros(M) # y coordinates
#
# npa_ang_final = np.asarray(teta_final)
# # Array response vector of the test signal
# # a = np.exp(np.arange(0,M,1)*1j*2*np.pi*d*(1/Landa)*np.cos(np.deg2rad(theta)))
# a = np.exp(np.arange(0,M,1)*1j*2*np.pi*d*(1/Landa))
# angles = np.cos(np.deg2rad(npa_ang_final))
# # # print(a[1], len(a), type(a))
# # print('angle', len(angles), len(angles[0]))
# angle_teta = []
# for i in range(len(a)):
#     angle_teta.append(a[i]*angles[i])
# # print('angle_teta', len(angle_teta), len(angle_teta[0]))
# #
# flatten_list = list(chain.from_iterable(angle_teta))
# #
# noise = np.random.normal(0,np.sqrt(10**-1),(M,N))
# noise2 = np.random.normal(0,np.sqrt(10**-1),(M,N*4))
# soi_mat = noise + angle_teta
# soi_mat2 = noise2 + flatten_list
# #
# R = (corr_matrix_estimate(soi_mat.T, imp="mem_eff"))
# R2 = (corr_matrix_estimate(soi_mat2.T, imp="mem_eff"))
# # print('R matrix', len(R), len(R[0]), '\n The R0 is', R[0])
# #
# scanning_vectors = gen_scanning_vectors(M, x, y, incident_angles)
# MUSIC = DOA_MUSIC(R, scanning_vectors, signal_dimension = 1)
# Bartlett = DOA_Bartlett(R, scanning_vectors)
# MUSIC2 = DOA_MUSIC(R2, scanning_vectors, signal_dimension = 1)
# Bartlett2 = DOA_Bartlett(R2, scanning_vectors)
#
# axes = plt.axes()
# # Plot results on the same fiugre
# # DOA_plot(Bartlett, incident_angles, log_scale_min = -50, axes=axes, alias_highlight=False)
# DOA_plot(MUSIC, incident_angles, axes=axes, alias_highlight=False)
# DOA_plot(MUSIC2, incident_angles, axes=axes, alias_highlight=False)
# axes.legend(("MUSIC", "MUSIC2"))
# plt.show()
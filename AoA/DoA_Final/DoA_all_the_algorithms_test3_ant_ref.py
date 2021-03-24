from pyargus.directionEstimation import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
from itertools import chain
init_notebook_mode(connected=True)
cf.go_offline()

d = 6.25  # Inter element spacing [lambda] (it's probably ~d/2)
M = 3  # number of antenna elements in the antenna system (ULA)
theta = 45  # incident angle of the test signal [deg]
N = 3*160  # sample size signal received in this pahse(this will increase in our case)
Landa = 12.5 #  The wave lenght of the signal


# new_data = pd.read_csv('C:/ti/simplelink_cc13x2_26x2_sdk_4_30_00_54/tools/ble5stack/rtls_agent/examples/rtls_aoa_iq_with_rtls_util_export_into_csv_test_log/02_17_2021_11_03_17_rtls_raw_iq_samples.csv')
# new_data = pd.read_csv('02_17_2021_18_00_12_rtls_raw_iq_samples_f88a5e2d8f14_0.csv')
new_data = pd.read_csv('rtls_true_iq_samples_passif_0_90_3.csv')
# new_data = pd.read_csv('rtls_raw_iq_samples_13.csv')

# This is a dump way to separate the ant_element data.
ant_1 = []
ant_2 = []
ant_3 = []
ant_ref = []
ant_final = []
teta_1 = []
teta_2 = []
teta_3 = []
teta_ref = []
teta_final = []
calc = 0
# attention: only using data from one channel. to do more, we need to separate the cahnnels
for i in range(0, 560, 16):
    if (calc == 0) or (calc % 4 == 0):
        for j in range(0, 15):
            ant_ref.append(complex(new_data['i'][j], new_data['q'][j]))
            teta_ref.append(np.arctan2(new_data['i'][j], new_data['q'][j]) * 180 / np.pi)
            print(i,j, calc, calc % 4 )
            calc += 1

    elif (calc % 4 == 1):
        for j in range(0, 15):
            ant_1.append(complex(new_data['i'][j], new_data['q'][j]))
            teta_1.append(np.arctan2(new_data['i'][j], new_data['q'][j]) * 180 / np.pi)
            # print('------------------', i, j, calc)
            calc += 1

    elif (calc % 4 == 2):
        for j in range(0, 15):
            ant_2.append(complex(new_data['i'][j], new_data['q'][j]))
            teta_2.append(np.arctan2(new_data['i'][j], new_data['q'][j]) * 180 / np.pi)
            # print('********************', i, j, calc)
            calc += 1
    elif (calc % 4 == 3):
        for j in range(0, 15):
            ant_3.append(complex(new_data['i'][j], new_data['q'][j]))
            teta_3.append(np.arctan2(new_data['i'][j], new_data['q'][j]) * 180 / np.pi)
            # print('%%%%%%%%%%%%%%%%%%%%', i, j, calc)
            calc += 1


ant_final.append(ant_1)
ant_final.append(ant_2)
ant_final.append(ant_3)
teta_final.append(teta_1)
teta_final.append(teta_2)
teta_final.append(teta_3)

# print(ant_final,'this is ant_final')
p1 = []
p2 = []
p3 = []
for i in range(len(ant_1)):
    multi1 = ant_1[i] * np.conj(ant_ref[i-1])
    multi2 = ant_2[i] * np.conj(ant_ref[i-1])
    multi3 = ant_3[i] * np.conj(ant_ref[i-1])
    p1.append(np.arctan2(multi1.real, multi1.imag) * 180/ np.pi)
    p2.append(np.arctan2(multi2.real, multi2.imag) * 180 / np.pi)
    p3.append(np.arctan2(multi3.real, multi3.imag) * 180 / np.pi)

ant_1_ang = np.multiply(p1, 1/np.pi)
ant_2_ang = np.multiply(p2, 1/np.pi)
ant_3_ang = np.multiply(p3, 1/np.pi)
print('the average of each ', np.average(ant_1_ang), np.average(ant_2_ang), np.average(ant_2_ang))

axes = plt.axes()
plt.plot(ant_1_ang,ant_3_ang)
plt.show()
incident_angles= np.arange(0,181,1)

# Generate scanning vectors with the general purpose function
x = np.arange(0, M, 1) * d  # x coordinates
y = np.zeros(M) # y coordinates
scanning_vectors = gen_scanning_vectors(M, x, y, incident_angles)

# final list of the complex I/Q numbers
npa_ant_final = np.asarray(ant_final)
npa_teta_final = np.asarray(teta_final)

# Array response vector of the test signal
a = np.exp(np.arange(0,M,1)*1j*2*np.pi*d*(1/Landa))
angles = np.cos(np.deg2rad(npa_teta_final))
# angles_cos = np.cos(np.deg2rad(npa_teta_final))
angle_teta = []
angle_teta_cos = []
for i in range(len(angles)):
    angle_teta.append(a[i]*angles[i])
    angle_teta_cos.append(a[i] * angles_cos[i])

flatten_list = list(chain.from_iterable(angle_teta))

# Generate multichannel uncorrelated noise
noise = np.random.normal(0,np.sqrt(10**-1),(M,N))
noise2 = np.random.normal(0,np.sqrt(10**-1),(M,160))

# Create received signal array
rec_signal = flatten_list + noise
rec_signal_2 = angle_teta + noise2
rec_signal_cos = angle_teta_cos + noise2

# Estimating the spatial correlation matrix
# R = corr_matrix_estimate(rec_signal.T, imp="mem_eff")
# R2 = corr_matrix_estimate(rec_signal_2.T, imp="mem_eff")
# R_cos = corr_matrix_estimate(rec_signal_cos.T, imp="mem_eff")
#
# Bartlett = DOA_Bartlett(R, scanning_vectors)
# Capon = DOA_Capon(R, scanning_vectors)
# MUSIC = DOA_MUSIC(R, scanning_vectors, signal_dimension = 1)
#
# Bartlett2 = DOA_Bartlett(R2, scanning_vectors)
# Capon2 = DOA_Capon(R2, scanning_vectors)
# MUSIC2 = DOA_MUSIC(R2, scanning_vectors, signal_dimension = 1)
#
# MUSIC_cos = DOA_MUSIC(R_cos, scanning_vectors, signal_dimension = 1)
# Get matplotlib axes object
# axes = plt.axes()
#
# # Plot results on the same fiugre
# # DOA_plot(Bartlett, incident_angles, log_scale_min = -50, axes=axes, alias_highlight=False)
# # DOA_plot(Capon, incident_angles, log_scale_min = -50, axes=axes, alias_highlight=False)
# DOA_plot(MUSIC, incident_angles, log_scale_min = -50, axes=axes, alias_highlight=False)
#
# # DOA_plot(Bartlett2, incident_angles, log_scale_min = -50, axes=axes, alias_highlight=False)
# DOA_plot(MUSIC2, incident_angles, log_scale_min = -50, axes=axes, alias_highlight=False)
#
# # DOA_plot(MUSIC_cos, incident_angles, log_scale_min = -50, axes=axes, alias_highlight=False)
#
# axes.legend(("MUSIC", "MUSIC2"))
# plt.show()

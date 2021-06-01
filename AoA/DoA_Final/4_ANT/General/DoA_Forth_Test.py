from pyargus.directionEstimation import *
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
# %matplotlib inline
import seaborn as sns
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
import plotly
from IPython.display import IFrame
init_notebook_mode(connected=True)
import math
cf.go_offline()



d = 5.6 # Inter element spacing [lambda]
M = 3  # number of antenna elements in the antenna system (ULA)
theta = 45  # incident angle of the test signal [deg]
N = 3*160  # sample size signal received in this pahse (This will increase in our case)
Landa = 12.5

# Reading the csv  file and extracting the I/Q samples
# new_data = pd.read_csv('rtls_raw_iq_samples_10.csv')
# new_data = pd.read_csv('rtls_raw_iq_samples_passif_0.csv')
# new_data = pd.read_csv('C:/ti/simplelink_cc13x2_26x2_sdk_4_30_00_54/tools/ble5stack/rtls_agent/examples/rtls_aoa_iq_with_rtls_util_export_into_csv_test_log/02_17_2021_11_03_17_rtls_raw_iq_samples.csv')
new_data = pd.read_csv('rtls_true_iq_samples_passif_0_45_1.csv')

ant_1 = []
ant_2 = []
ant_3 = []
ant_final = []
calc = 0
for i in range(16, 496, 16):
    if (calc == 0) or (calc % 3 == 0):
        for j in range(i - 16, i):
            ant_1.append(complex(new_data['i'][j], new_data['q'][j]))
            calc += 1

    elif (calc % 3 == 1):
        for j in range(i - 16, i):
            ant_2.append(complex(new_data['i'][j], new_data['q'][j]))
            calc += 1

    elif (calc % 3 == 2):
        for j in range(i - 16, i):
            ant_3.append(complex(new_data['i'][j], new_data['q'][j]))
            calc += 1

ant_final.append(ant_1)
ant_final.append(ant_2)
ant_final.append(ant_3)

# print(len(ant_final[0]))

# angle_teta_list = []
#
# for j in range(len(ant_final[0])):
#     angle_teta_list.append(np.arctan2(ant_final[0][j].imag, ant_final[0][j].real)*180 / np.pi)
#     angle_teta_list.append(np.arctan2(ant_final[1][j].imag, ant_final[1][j].real)*180 / np.pi)
#     angle_teta_list.append(np.arctan2(ant_final[2][j].imag, ant_final[2][j].real)*180 / np.pi)
#
#
# # final_angle_teta_one_list = []
# # for i in range(len(ant_final)):
# #     for j in range(len(ant_final[i])):
# #         final_angle_teta_one_list.append(np.arctan2(ant_final[i][j].imag, ant_final[i][j].real)*180 / np.pi)
#
# # incident_angles = np.asarray(final_angle_teta)
# incident_angles = np.asarray(angle_teta_list)
incident_angles= np.arange(0,181,1)

# Generate scanning vectors with the general purpose function
x = np.arange(0, M, 1) * d  # x coordinates
y = np.zeros(M) # y coordinates
# scanning_vectors = gen_scanning_vectors(M, x, y, incident_angles)

# final list of the complex I/Q numbers
npa_ant_final = np.asarray(ant_final)

# R_2 = corr_matrix_estimate(npa_ant_final.T, imp="mem_eff")
# Array response vector of the test signal
a = np.exp(np.arange(0,M,1)*1j*2*np.pi*d*(1/Landa)*np.cos(np.deg2rad(theta)))
print(a)
# Generate multichannel test signal
# soi = np.random.normal(0,1,N)  # Signal of Interest

soi_matrix  = np.outer(npa_ant_final, a).T

# Generate multichannel uncorrelated noise
noise = np.random.normal(0,np.sqrt(10**-1),(M,N))

# Create received signal array
rec_signal = soi_matrix + noise

# Estimating the spatial correlation matrix
R = corr_matrix_estimate(rec_signal.T, imp="mem_eff")

# incident_angles= np.arange(0,181,1)

# Generate scanning vectors with the general purpose function
x = np.arange(0, M, 1) * d  # x coordinates
y = np.zeros(M) # y coordinates
scanning_vectors = gen_scanning_vectors(M, x, y, incident_angles)


# Estimate DOA with the Bartlett method
Bartlett = DOA_Bartlett(R, scanning_vectors)
# print(rec_signal, len(rec_signal))
MUSIC = DOA_MUSIC(R, scanning_vectors, signal_dimension= 1, angle_resolution= 1)
DOA_plot(MUSIC, incident_angles, log_scale_min = -50, alias_highlight=True, d=d)

DOA_plot(Bartlett, incident_angles, log_scale_min = -50, alias_highlight=True, d=d)

plt.show()


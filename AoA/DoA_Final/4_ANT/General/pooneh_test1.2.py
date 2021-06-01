from pyargus.directionEstimation import *
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
init_notebook_mode(connected=True)
import math
cf.go_offline()

d = 0.3 # Inter element spacing [lambda]
M = 4  # number of antenna elements in the antenna system (ULA)
theta = 45  # incident angle of the test signal [deg]
Landa = 1

# we should use 8bits not 16 bits.
# new_data = pd.read_csv('02_17_2021_18_00_12_rtls_raw_iq_samples_f88a5e2d8f14_0.csv')
# new_data = pd.read_csv('02_19_2021_11_29_34_rtls_raw_iq_samples_f88a5e2d8f14_0.csv')
# new_data = pd.read_csv('C:/ti/simplelink_cc13x2_26x2_sdk_4_30_00_54/tools/ble5stack/rtls_agent/examples/rtls_aoa_iq_with_rtls_util_export_into_csv_test_log/02_23_2021_16_44_46_rtls_raw_iq_samples.csv')
# new_data = pd.read_csv('C:/ti/simplelink_cc13x2_26x2_sdk_4_40_04_04/tools/ble5stack/rtls_agent/examples/rtls_aoa_iq_with_rtls_util_export_into_csv_log/02_23_2021_11_05_57_rtls_raw_iq_samples_f88a5e2d8f14_0.csv')
new_data = pd.read_csv('C:/ti/simplelink_cc13x2_26x2_sdk_4_40_04_04/tools/ble5stack/rtls_agent/examples/rtls_aoa_iq_with_rtls_util_export_into_csv_log/02_25_2021_14_06_32_rtls_raw_iq_samples_f88a5e2d8f14_0.csv')

ant_1 = []
ant_2 = []
ant_3 = []
ant_4 = []
ant_final = []
calc = 0
data_size = len(new_data)

for i in range(17, 496, 8):
    if (calc == 0) or (calc % 4 == 0):
        for j in range(i - 17, i):
            ant_1.append(complex(new_data['i'][j], new_data['q'][j]))
            calc += 1

    elif (calc % 4 == 1):
        for j in range(i - 17, i):
            ant_2.append(complex(new_data['i'][j], new_data['q'][j]))
            calc += 1

    elif (calc % 4 == 2):
        for j in range(i - 17, i):
            ant_3.append(complex(new_data['i'][j], new_data['q'][j]))
            calc += 1
    elif (calc % 4 == 3):
        for j in range(i - 17, i):
            ant_4.append(complex(new_data['i'][j], new_data['q'][j]))
            calc += 1

ant_final.append(ant_1)
ant_final.append(ant_2)
ant_final.append(ant_3)
ant_final.append(ant_4)

N = len(ant_1)*4
incident_angles = np.arange(0,181,1)

# Generate scanning vectors with the general purpose function
x = np.arange(0, M, 1) * d  # x coordinates
y = np.zeros(M) # y coordinates
scanning_vectors = gen_scanning_vectors(M, x, y, incident_angles)

# final list of the complex I/Q numbers
npa_ant_final = np.asarray(ant_final)
# Array response vector of the test signal
a = (np.exp(np.arange(0,M,1)*1j*2*np.pi*d*(1/Landa)*np.cos(np.deg2rad(theta))))


soi_matrix = (np.outer(npa_ant_final, a).T)

# Generate multichannel uncorrelated noise
noise = np.random.normal(0,np.sqrt(10**-1),(M,N))

# Create received signal array
rec_signal = soi_matrix + noise

R = corr_matrix_estimate(rec_signal.T, imp="mem_eff")
MUSIC = DOA_MUSIC(R, scanning_vectors, signal_dimension = 1)

axes = plt.axes()
DOA_plot(MUSIC, incident_angles, log_scale_min = -50, axes=axes, alias_highlight=False)
axes.legend(("MUSIC"))
plt.show()

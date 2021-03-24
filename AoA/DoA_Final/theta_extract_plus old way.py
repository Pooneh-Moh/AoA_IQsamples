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
# theta = 45  # incident angle of the test signal [deg]
Landa = 12.5

new_data = pd.read_csv('C:/ti/simplelink_cc13x2_26x2_sdk_4_40_04_04/tools/ble5stack/rtls_agent/examples/rtls_aoa_iq_with_rtls_util_export_into_csv_log/02_25_2021_14_06_32_rtls_raw_iq_samples_f88a5e2d8f14_0.csv')

ant_1 = []
ant_2 = []
ant_3 = []
ant_4 = []
teta_1 = []
teta_2 = []
teta_3 = []
teta_4 = []
ant_final = []
data_size = len(new_data)
N = 153
calc = 0
for i in range(17, 592, 16):
    if (calc == 0) or (calc % 4 == 0):
        for j in range(i - 17, i):
            ant_1.append(complex(new_data['i'][j], new_data['q'][j]))
            teta_1.append(np.arctan2(new_data['i'][j], new_data['q'][j]) * 180 / np.pi)
            # print(i, j, calc)
            calc += 1

    elif (calc % 4 == 1):
        for j in range(i - 17, i):
            ant_2.append(complex(new_data['i'][j], new_data['q'][j]))
            teta_2.append(np.arctan2(new_data['i'][j], new_data['q'][j]) * 180 / np.pi)
            calc += 1

    elif (calc % 4 == 2):
        for j in range(i - 17, i):
            ant_3.append(complex(new_data['i'][j], new_data['q'][j]))
            teta_3.append(np.arctan2(new_data['i'][j], new_data['q'][j]) * 180 / np.pi)
            calc += 1
    elif (calc % 4 == 3):
        for j in range(i - 17, i):
            ant_4.append(complex(new_data['i'][j], new_data['q'][j]))
            teta_4.append(np.arctan2(new_data['i'][j], new_data['q'][j]) * 180 / np.pi)
            calc += 1

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
incident_angles= np.arange(0,181,1)
# Generate scanning vectors with the general purpose function
x = np.arange(0, M, 1) * d # x coordinates
y = np.zeros(M) # y coordinates

# final list of the complex I/Q numbers
npa_ant_final = np.asarray(ant_final)
npa_ang_final = np.asarray(teta_final)
# Array response vector of the test signal
a = np.exp(np.arange(0,M,1)*1j*2*np.pi*d*(1/Landa))
angles = np.cos(np.deg2rad(npa_ang_final))

angle_teta = []
for i in range(len(a)):
    angle_teta.append(a[i]*angles[i])
flatten_list = list(chain.from_iterable(angle_teta))

print('angle_teta', len(angle_teta), len(angle_teta[0]))
print('flated data points', len(flatten_list))

noise = np.random.normal(0,np.sqrt(10**-1),(M,N))
noise_flat = np.random.normal(0,np.sqrt(10**-1),(M,N*4))
soi_mat = noise + angle_teta # 4x 153
soi_mat_flat = noise_flat + flatten_list # 4x625

R = (corr_matrix_estimate(soi_mat.T, imp="mem_eff"))
R2 = (corr_matrix_estimate(soi_mat_flat.T, imp="mem_eff"))

scanning_vectors = gen_scanning_vectors(M, x, y, incident_angles)
MUSIC = DOA_MUSIC(R, scanning_vectors, signal_dimension = 1)
Bartlett = DOA_Bartlett(R, scanning_vectors)
MUSIC2 = DOA_MUSIC(R2, scanning_vectors, signal_dimension = 1)
Bartlett2 = DOA_Bartlett(R2, scanning_vectors)
print('Signal angle is',np.argmax(MUSIC), 'and the Flatted signal angle is', np.argmax(MUSIC2))
axes = plt.axes()
# Plot results on the same fiugre
DOA_plot(MUSIC, incident_angles, axes=axes, alias_highlight=False)
DOA_plot(MUSIC2, incident_angles, axes=axes, alias_highlight=False)

axes.legend(("MUSIC", "MUSIC_flat"))
plt.show()
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
# print(new_data['i'][0])
new_data.drop([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
new_data ['teta'] = np.arctan2(new_data['i'], new_data['q']) * 180 / np.pi

incident_angles= np.arange(0,181,1)
# Generate scanning vectors with the general purpose function
x = np.arange(0, M, 1) * d # x coordinates
y = np.zeros(M) # y coordinates
# Array response vector of the test signal
a = np.exp(np.arange(0,M,1)*1j*2*np.pi*d*(1/Landa))
angles = np.cos(np.deg2rad(new_data ['teta']))

angle_teta = []
for i in range(len(a)):
    angle_teta.append(a[i]*angles)
N = len(angles)
noise = np.random.normal(0,np.sqrt(10**-1),(M,N))
soi_mat = noise + angle_teta

R = (corr_matrix_estimate(soi_mat.T, imp="mem_eff"))

print('R matrix', len(R), len(R[0]), '\n The R0 is', R[0])

scanning_vectors = gen_scanning_vectors(M, x, y, incident_angles)
MUSIC = DOA_MUSIC(R, scanning_vectors, signal_dimension = 1)
Bartlett = DOA_Bartlett(R, scanning_vectors)
print('The angle is', np.argmax(MUSIC))
# axes = plt.axes()
# DOA_plot(MUSIC, incident_angles, axes=axes, alias_highlight=False)
# print()
# axes.legend(("MUSIC"))
# plt.show()
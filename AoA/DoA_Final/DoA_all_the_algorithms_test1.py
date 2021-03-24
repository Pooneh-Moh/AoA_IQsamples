from pyargus.directionEstimation import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
init_notebook_mode(connected=True)
cf.go_offline()



d = 5.6 # Inter element spacing [lambda] (it's probably ~d/2)
M = 3  # number of antenna elements in the antenna system (ULA)
theta = 45  # incident angle of the test signal [deg]
N = 3*160  # sample size signal received in this pahse(this will increase in our case)
Landa = 12.5 #  The wave lenght of the signal


# new_data = pd.read_csv('C:/ti/simplelink_cc13x2_26x2_sdk_4_30_00_54/tools/ble5stack/rtls_agent/examples/rtls_aoa_iq_with_rtls_util_export_into_csv_test_log/02_17_2021_11_03_17_rtls_raw_iq_samples.csv')
new_data = pd.read_csv('02_17_2021_18_00_12_rtls_raw_iq_samples_f88a5e2d8f14_0.csv')

# This is a dump way to separate the ant_element data.
ant_1 = []
ant_2 = []
ant_3 = []
ant_final = []
calc = 0
# attention: only using data from one channel. to do more, we need to separate the cahnnels
for i in range(16, 496, 16): # Attention: should be devided by 8 if using 1us
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

print(ant_final,'this is ant_final')

incident_angles= np.arange(0,181,1)

# Generate scanning vectors with the general purpose function
x = np.arange(0, M, 1) * d  # x coordinates
y = np.zeros(M) # y coordinates
# scanning_vectors = gen_scanning_vectors(M, x, y, incident_angles)

# final list of the complex I/Q numbers
npa_ant_final = np.asarray(ant_final)

# Array response vector of the test signal
a = np.exp(np.arange(0,M,1)*1j*2*np.pi*d*(1/Landa)*np.cos(np.deg2rad(theta)))


print(a)
# Generate multichannel test signal
# Signal of Interest
soi_matrix  = np.outer(npa_ant_final, a).T

# Generate multichannel uncorrelated noise
noise = np.random.normal(0,np.sqrt(10**-1),(M,N))

# Create received signal array
rec_signal = soi_matrix + noise

# Estimating the spatial correlation matrix
R = corr_matrix_estimate(rec_signal.T, imp="mem_eff")

# Generate scanning vectors with the general purpose function
x = np.arange(0, M, 1) * d  # x coordinates
y = np.zeros(M) # y coordinates
scanning_vectors = gen_scanning_vectors(M, x, y, incident_angles)

Bartlett = DOA_Bartlett(R, scanning_vectors)
Capon = DOA_Capon(R, scanning_vectors)
MUSIC = DOA_MUSIC(R, scanning_vectors, signal_dimension = 1)

# Get matplotlib axes object
axes = plt.axes()

# Plot results on the same fiugre
DOA_plot(Bartlett, incident_angles, log_scale_min = -50, axes=axes, alias_highlight=False)
DOA_plot(Capon, incident_angles, log_scale_min = -50, axes=axes, alias_highlight=False)
DOA_plot(MUSIC, incident_angles, log_scale_min = -50, axes=axes, alias_highlight=False)

axes.legend(("Bartlett","Capon","MUSIC"))
plt.show()

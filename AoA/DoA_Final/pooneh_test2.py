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

d = 4.15 # Inter element spacing [lambda]
M = 4  # number of antenna elements in the antenna system (ULA)
theta = 135  # incident angle of the test signal [deg]
Landa = 12.5

# new_data = pd.read_csv('02_17_2021_18_00_12_rtls_raw_iq_samples_f88a5e2d8f14_0.csv')
new_data = pd.read_csv('02_19_2021_11_29_34_rtls_raw_iq_samples_f88a5e2d8f14_0.csv')
data_size = len(new_data)
N = data_size-16  # sample size signal received in this pahse
ant_1 = []
ant_2 = []
ant_3 = []
ant_4 = []
ant_final = []
calc = 0
for i in range(16, data_size, 16):
    if (calc == 0) or (calc % 4 == 0):
        for j in range(i - 16, i):
            ant_1.append(complex(new_data['i'][j], new_data['q'][j]))
            calc += 1

    elif (calc % 4 == 1):
        for j in range(i - 16, i):
            ant_2.append(complex(new_data['i'][j], new_data['q'][j]))
            calc += 1

    elif (calc % 4 == 2):
        for j in range(i - 16, i):
            ant_3.append(complex(new_data['i'][j], new_data['q'][j]))
            calc += 1
    elif (calc % 4 == 3):
        for j in range(i - 16, i):
            ant_4.append(complex(new_data['i'][j], new_data['q'][j]))
            calc += 1

ant_final.append(ant_1)
ant_final.append(ant_2)
ant_final.append(ant_3)
ant_final.append(ant_4)

incident_angles= np.arange(0,181,1)

# Generate scanning vectors with the general purpose function
x = np.arange(0, M, 1) * d  # x coordinates
y = np.zeros(M) # y coordinates
scanning_vectors = gen_scanning_vectors(M, x, y, incident_angles)


# final list of the complex I/Q numbers
npa_ant_final = np.asarray(ant_final)
# print(ant_final[0], 'this is ant_final', len(ant_final), '\n this is nap_ant_final', npa_ant_final[0])

# Array response vector of the test signal
# this should be different here
a = np.exp(np.arange(0,M,1)*1j*2*np.pi*d*(1/Landa)*np.sin(np.deg2rad(theta)))
print(a, len(a))

soi_matrix = np.outer(npa_ant_final[0], a).T
# Generate multichannel uncorrelated noise
# do we really have to? why?
noise = np.random.normal(0,np.sqrt(10**-1),(M,N))
# Create received signal array
rec_signal = soi_matrix + noise
R = corr_matrix_estimate(rec_signal.T, imp="mem_eff")

Bartlett = DOA_Bartlett(R, scanning_vectors)
Capon = DOA_Capon(R, scanning_vectors)
MUSIC = DOA_MUSIC(R, scanning_vectors, signal_dimension = 1)

# Get matplotlib axes object
axes = plt.axes()

# Plot results on the same fiugre
DOA_plot(Bartlett, incident_angles, log_scale_min = -50, axes=axes, alias_highlight=False)
# DOA_plot(Capon, incident_angles, log_scale_min = -50, axes=axes, alias_highlight=False)
DOA_plot(MUSIC, incident_angles, log_scale_min = -50, axes=axes, alias_highlight=False)

axes.legend(("Bartlett","MUSIC"))
plt.show()

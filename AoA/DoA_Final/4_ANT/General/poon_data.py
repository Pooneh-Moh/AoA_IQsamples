import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
import scipy.signal as signal
import seaborn as sns
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
import plotly
from IPython.display import IFrame
from pyargus.directionEstimation import gen_ula_scanning_vectors

init_notebook_mode(connected=True)
import math
cf.go_offline()

# This the max number of samples that can be stored in the RF Core RAM
AOA_RES_MAX_SIZE = 511


# Note this is a direct port of AOA.c::AOA_calcNumOfCteSamples
# this class makes all the samples the same size of 511!
def num_iqsamples_per_evt(cte_scan_ovs, cte_offset, cte_time):
    samp_per_evt = (((cte_time * 8) - cte_offset) * cte_scan_ovs)

    if samp_per_evt > AOA_RES_MAX_SIZE:
        samp_per_evt = AOA_RES_MAX_SIZE

    return samp_per_evt


# calculate the phase and the magnetude of the signal (sqrt(I^2 + Q^2)) and arct(Q/I)
def cal_magnitude(q_value, i_value):
    return math.sqrt(math.pow(q_value, 2) + math.pow(i_value, 2))


def cal_phase(q_value, i_value):
    return math.degrees(math.atan2(q_value, i_value))


if __name__ == "__main__":
    df = pd.read_csv('rtls_raw_iq_samples_f88a5e2d88c5_0.csv')
    aoa_cte_scan_ovs = 4
    aoa_cte_offset = 4
    aoa_cte_time = 20
    aoa_iq_samples_per_ce = num_iqsamples_per_evt(aoa_cte_scan_ovs, aoa_cte_offset, aoa_cte_time)

    # remove dublicates
    df = df.drop_duplicates()

    df['phase'] = df.apply(lambda row: cal_phase(row['q'], row['i']), axis=1)
    df['magnitude'] = df.apply(lambda row: cal_magnitude(row['q'], row['i']), axis=1)

    # Plot all the I/Q collected. Each channel will have a plot which contains I/Q samples.
    # If you have collected I/Q data on 37 data channels, then there will be 37 windows popped up
    grouped = df.groupby('channel')
    # axes = grouped[['i', 'q']].plot(title="I/Q samples", grid=True)

    # Create 4 plots and each plot has x number of subplots. x = number of channels
    indexed = df.set_index(['channel', 'sample_idx'])
    # drop the dublicates
    indexed_modified = indexed.drop_duplicates()
    indexed_modified = indexed_modified[~indexed_modified.index.duplicated(keep='first')]
    # indexed_modified.unstack(level=0)[['phase']].plot(subplots=True, title="Phase information",
    #                                                   xlim=[0, aoa_iq_samples_per_ce], ylim=[-190, +190])
    # indexed_modified.unstack(level=0)[['magnitude']].plot(subplots=True, title="Signal magnitude",
    #                                                       xlim=[0, aoa_iq_samples_per_ce])
    # indexed_modified.unstack(level=0)[['i']].plot(subplots=True, title="I samples", xlim=[0, aoa_iq_samples_per_ce])
    # indexed_modified.unstack(level=0)[['q']].plot(subplots=True, title="Q samples", xlim=[0, aoa_iq_samples_per_ce])

    M = 3  # number of elements in atnetta array
    d = 0.35  # Inter element spacing [lambda]
    array_alignment = np.arange(0, M, 1) * d

    ning_vectors = gen_ula_scanning_vectors(array_alignment, indexed_modified.unstack(level=0)[['phase']])

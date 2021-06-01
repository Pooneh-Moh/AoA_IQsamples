# from pyargus.directionEstimation import gen_ula_scanning_vectors
from pyargus.directionEstimation import *
import pandas as pd
import csv
# import matplotlib.pyplot as plt
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
from itertools import chain
from datetime import datetime
import os
import sys


def theta_cal(file_name):

    angle_res = []
    init_notebook_mode(connected=True)
    cf.go_offline()

    d = 4.17 # Inter element spacing [lambda]
    M = 4  # number of antenna elements in the antenna system (ULA)
    theta = 56  # incident angle of the test signal [deg]
    Landa = 12.5

    # new_data = pd.read_csv(file_name)    #names=['sample_idx','channel','i', 'q']
    new_data = pd.read_csv(
        'C:/ti/simplelink_cc13x2_26x2_sdk_4_40_04_04/tools/ble5stack/rtls_agent/examples/rtls_aoa_iq_with_rtls_util_export_into_csv_log/02_25_2021_14_06_32_rtls_raw_iq_samples_f88a5e2d8f14_0.csv')
    ant_1 = []
    ant_2 = []
    ant_3 = []
    ant_4 = []
    ant_final = []
    calc = 0
    pkt_list = []
    channle_list = []

    for i, row in new_data.iterrows():
        q = row['pkt']
        c = row['channel']
        if q not in pkt_list:
            pkt_list.append(q)
            channle_list.append(c)

    # print('pkt_list is',len(pkt_list),'\n and cahnnel list is',len(channle_list))
    for pkt in pkt_list:
        print("+++++++++++", pkt)
        res = new_data.loc[new_data.pkt == pkt]
        print('res len is', len(res))
        idx = np.asarray(res.index)
        # print(idx[0])

        for i in range(17+idx[0], 592, 16):
            if (calc == 0) or (calc % 4 == 0):
                for j in range(i - 17, i):
                    ant_1.append(complex(res['i'][j], res['q'][j]))
                    # print(i, j, calc)
                    calc += 1

            elif (calc % 4 == 1):
                for j in range(i - 17, i):
                    ant_2.append(complex(res['i'][j], res['q'][j]))
                    calc += 1

            elif (calc % 4 == 2):
                for j in range(i - 17, i):
                    ant_3.append(complex(res['i'][j], res['q'][j]))
                    calc += 1

            elif (calc % 4 == 3):
                for j in range(i - 17, i):
                    ant_4.append(complex(res['i'][j], res['q'][j]))
                    calc += 1

        ant_final.append(ant_1)
        ant_final.append(ant_2)
        ant_final.append(ant_3)
        ant_final.append(ant_4)

        incident_angles= np.arange(0,181,1)
        # Generate scanning vectors with the general purpose function
        x = np.arange(0, M, 1) * d # x coordinates
        y = np.zeros(M) # y coordinates

        # final list of the complex I/Q numbers
        npa_ant_final = np.asarray(ant_final)
        try:
            if len(npa_ant_final)> 4:
                # print('len(npa_ant_final) before', len(npa_ant_final))
                N = len(npa_ant_final) - 4
                a_list = list(range(0,N))
                # print(a_list)
                npa_ant_final = np.delete(npa_ant_final, [a_list], 0)
                # print('len(npa_ant_final) after', len(npa_ant_final))
            else:
                print('we rae here')
        except:
            pass

        a = np.exp(np.arange(0, M, 1) * 1j * 2 * np.pi * d * (1 / Landa) * np.cos(np.deg2rad(theta)))
        soi_matrix = np.outer(npa_ant_final, a).T

        try:
            N = len(soi_matrix[0])
            print('N is ', N, len(soi_matrix))
            noise = np.random.normal(0, np.sqrt(10 ** -1), (M, N))
            # noise = np.random.normal(0,np.sqrt(10**-1),(M,len(rec_sig[0])))
            # soi_mat = noise + rec_sig
            rec_sig = soi_matrix + noise

            R = (corr_matrix_estimate(rec_sig.T, imp="mem_eff"))
            # R = (corr_matrix_estimate(soi_mat.T, imp="mem_eff"))

            scanning_vectors = gen_scanning_vectors(M, x, y, incident_angles)
            MUSIC = DOA_MUSIC(R, scanning_vectors, signal_dimension = 1)
            # Bartlett = DOA_Bartlett(R, scanning_vectors)
            print('The angle is', np.argmax(MUSIC))
            angle_res.append({"pkt": pkt, "angle": np.argmax(MUSIC)})
        except:
            pass


    return angle_res

def main():
    angle_result = []
    pkt_lst = []
    channel_lst = []
    file_names = 'C:/Users/pooneh/Documents/GitHub/AoA_IQsamples/AoA/DoA_Final/81data_points/rtls_test_results/RAW_sample_slotduration1/test'
    for root, dirs, files in os.walk(file_names):
        # break
        for file in files:
            if file.endswith(".csv"):
                channel_lst.append(file)
                # print(os.path.join(file))
                # file_names.append(os.path.join(file))
    print(channel_lst)
    # for name in file_names:
    angle_list = theta_cal(file_names)
    for info in angle_list:
        angle_result.append(info["angle"])
        pkt_lst.append(info["pkt"])
        # channel_lst.append(info["channel"])

    res_dict = {"pkt": pkt_lst, "angle": angle_result}

    result = pd.DataFrame(res_dict)
    # result.to_csv('angel_equal_list_oldway.csv', index=False)
    

if __name__ =="__main__":
    t = datetime.now()
    print(t)
    main()
    print("Time:", datetime.now() - t)
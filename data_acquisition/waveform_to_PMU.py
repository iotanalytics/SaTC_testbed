# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 12:57:58 2022

@author: Steph, Qi Li
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import read_csv
from pathlib import Path
from scipy import fft

def feature_extract(X, f_s):
    """
    Params:
        X is the waveform signal. Channel in rows.
        f_s is the sampling frequency of the signal 
    """
    rows = X.shape[0]
    Nn = X.shape[1]  # Nn = number of columns in X
    num_time_periods = 1  # setting to 1, not using sub-windowing

    dataWindow = f_s

    slipSize = int(round(dataWindow - Nn) / num_time_periods)

    # Note! When Phase Angle is added, "rows*3" will change to "rows*4"
    dataFFT = np.zeros((rows*4, num_time_periods))
    df = f_s / Nn  # resolution
    for num_i in range(0, num_time_periods):
        for signalNum in range(0, rows):
            dataFeature = X[signalNum, num_i * slipSize:num_i * slipSize + Nn]
            y = dataFeature - np.mean(dataFeature)
            han = np.hanning(Nn)  # Nn is the le
            y = han * y  # add a hanning window to prevent FFT leakage
            # ======================================================================
            f_x = np.arange(Nn) * df
            t_x0 = f_x - f_s / 2;
            fft_y = fft.fft(y)  # FFT
            y_x0 = np.abs(fft_y) / len(y) * 2  # reshape the y-axis and obtain the real amplitude
            t_x = t_x0[int(len(t_x0) / 2):int(len(t_x0))]  # reshape the x-axis
            y_x = y_x0[0:int(len(t_x0) / 2)]  # for current

            # correct the amplitude and frequency 1
            for ii in range(0, len(t_x)):
                if t_x[ii] <= 10:
                    y_x[ii] = 0.000001
                    
            Ah = np.zeros((len(y_x), 1))
            Ah[:, 0] = y_x
            Amaxh = np.max(Ah)
            kh = np.argmax(Ah)
            if (kh >= 2) & (kh + 1 < int(Nn / 2)):
                if Ah[kh - 1] > Ah[kh + 1]:
                    deltfh = (Ah[kh] / Ah[kh - 1] - 2) / (1 + Ah[kh] / Ah[kh - 1])
                    f0h = (kh + deltfh) * f_s / Nn
                    amh = 2 / np.sinc(deltfh) * Amaxh * (1 - deltfh ** 2)
                else:
                    deltfh = (Ah[kh] / Ah[kh + 1] - 2) / (1 + Ah[kh] / Ah[kh + 1])
                    f0h = (kh - deltfh) * f_s / Nn
                    amh = 2 / np.sinc(deltfh) * Amaxh * (1 - deltfh ** 2)
                y_x[kh] = amh
                t_x[kh] = f0h
                Ah[kh] = amh
            
            # ======================================================================
            positionF = np.argmax(y_x)
            # obtain THD
            for j in range(0, int(len(t_x))):
                if abs(t_x[j] - 60 * 2) < df:  # df=f_s/Nn is resolution
                    J2 = j
                if abs(t_x[j] - 60 * 3) < df:
                    J3 = j
                if abs(t_x[j] - 60 * 4) < df:
                    J4 = j
                if abs(t_x[j] - 60 * 5) < df:
                    J5 = j
                if abs(t_x[j] - 60 * 6) < df:
                    J6 = j
                if abs(t_x[j] - 60 * 7) < df:
                    J7 = j
            sumF = y_x[J2] ** 2 + y_x[J3] ** 2 + y_x[J4] ** 2 + y_x[J5] ** 2 + y_x[J6] ** 2 + y_x[J7] ** 2
            thd = np.sqrt(sumF) / y_x[positionF]
            dataFFT[signalNum * 4, num_i] = y_x[positionF]
            dataFFT[signalNum * 4 + 1, num_i] = t_x[positionF]
            # put phase angle here, updtate thd array position data
            dataFFT[signalNum * 4 + 2, num_i] =  np.angle(fft_y[kh],deg=True)
            #dataFFT[signalNum * 3 + 2, num_i] = thd
            dataFFT[signalNum * 4 + 3, num_i] = thd
            # output shape: I1_M,I1_F,I1_A,I1_T,I2_M,I2_F,I2_T,I3_M,I3_F,I3_T,U1_M,U1_F,U1_T

    return dataFFT
import time #measure proceeding time to calculate Hz
import Adafruit_BBIO.ADC as ADC #use analog read
ADC.setup() 
import numpy as np
import requests #connect IFTTT
from scipy import signal #detect peak
from time import sleep

import scipy

# parameters
analogPin_X="P9_36"
analogPin_Y="P9_38"
analogPin_Z="P9_40"
sample_number = 2000
repeat_number = 10

vibration_data_X = []
vibration_data_Y = []
vibration_data_Z = []

# IFTTT_Webhook
def ifttt_webhook(eventid):
    payload = {"value1": Vibration_abs_mean_data_X,
                "value2": Vibration_abs_mean_data_Y,
                "value3": Vibration_abs_mean_data_Z } #payloads is just plan. We have to revise after completion prototype.
    url = "https://maker.ifttt.com/trigger/" + eventid + "/with/key/lw1KadV3UH4bdfDwquxSEPvAOSj0FrNo_iPm1UjD-Ey"
    response = requests.post(url, data=payload)

# Starting measurement sound data


# Caribration to revise vibration data center to 0
for i in range(sample_number):
    vibration_data_X_t = ADC.read(analogPin_X)
    vibration_data_X.append(vibration_data_X_t)
    vibration_data_average_for_calibration_X = np.mean(vibration_data_X)

    vibration_data_Y_t = ADC.read(analogPin_Y)
    vibration_data_Y.append(vibration_data_Y_t)
    vibration_data_average_for_calibration_Y = np.mean(vibration_data_Y)

    vibration_data_Z_t = ADC.read(analogPin_Z)
    vibration_data_Z.append(vibration_data_Z_t)
    vibration_data_average_for_calibration_Z = np.mean(vibration_data_Z)

    vibration_data_X = []   #vibration_data_X resset
    vibration_data_Y = []   #vibration_data_Y resset
    vibration_data_Z = []   #vibration_data_Z resset

# Starting mesurement
for n in range(repeat_number):
 
    start_time = time.time()  #measureing time to calculate the frequency

    for i in range(sample_number):
        vibration_data_X_t = ADC.read(analogPin_X) - vibration_data_average_for_calibration_X
        vibration_data_Y_t = ADC.read(analogPin_Y) - vibration_data_average_for_calibration_Y
        vibration_data_Z_t = ADC.read(analogPin_Z) - vibration_data_average_for_calibration_Z

        vibration_data_X.append(vibration_data_X_t)
        vibration_data_Y.append(vibration_data_Y_t)
        vibration_data_Z.append(vibration_data_Z_t)

    end_time = time.time()    #measureing time to calculate the frequency
    total_time = end_time - start_time    #measureing calculation time from start to end regarding getting sound data

    np.savetxt('raw_vibration_data_X'+str(n)+'.csv',vibration_data_X)  #for test. output csv data about raw sound data 
    np.savetxt('raw_vibration_data_Y'+str(n)+'.csv',vibration_data_Y)  #for test. output csv data about raw sound data 
    np.savetxt('raw_vibration_data_Z'+str(n)+'.csv',vibration_data_Z)  #for test. output csv data about raw sound data 


    #fast Fourier transform and revise the data
    FX = np.fft.fft(vibration_data_X)    #fast Fourier transform to vibration_data_X
    FY = np.fft.fft(vibration_data_Y)    #fast Fourier transform to vibration_data_Y
    FZ = np.fft.fft(vibration_data_Z)    #fast Fourier transform to vibration_data_Z

    F_abs_X = np.abs(FX)    #absolutely FFT_X
    F_abs_Y = np.abs(FY)    #absolutely FFT_Y
    F_abs_Z = np.abs(FZ)    #absolutely FFT_Z

    F_abs_X[0] = 0  #delete dc component FFT_X
    F_abs_Y[0] = 0  #delete dc component FFT_Y
    F_abs_Z[0] = 0  #delete dc component FFT_Z

    F_abs_X = F_abs_X/sample_number*2  #translate the value
    F_abs_Y = F_abs_Y/sample_number*2  #translate the value
    F_abs_Z = F_abs_Z/sample_number*2  #translate the value

    for num in range(sample_number/2,sample_number): #delete after Nyquist constant value
       F_abs_X[num] = 0
       F_abs_Y[num] = 0
       F_abs_Z[num] = 0

    np.savetxt('sound'+str(n)+'.csv',F_abs_X)  #output csv data about F_abs_X
    # np.savetxt('sound'+str(n)+'.csv',F_abs_Y)  #output csv data about F_abs_Y
    # np.savetxt('sound'+str(n)+'.csv',F_abs_Z)  #output csv data about F_abs_Z

    F_abs_sum_X = np.sum(F_abs_X)   #sum all frequency of amplitude X
    F_abs_sum_Y = np.sum(F_abs_Y)   #sum all frequency of amplitude Y
    F_abs_sum_Z = np.sum(F_abs_Z)   #sum all frequency of amplitude Z

    #making frequency data
    freq = np.arange(0, 1/total_time*1000*2, 1/total_time/sample_number*1000*2) # making Hz axis" 11/15 add *2"

    np.savetxt('sound_freq'+str(n)+'.csv',freq)   #output csv data about freq

    Kurt_X = scipy.stats.kurtosis(vibration_data_X)
    Kurt_Y = scipy.stats.kurtosis(vibration_data_Y)
    Kurt_Z = scipy.stats.kurtosis(vibration_data_Z)

    print("Kurt_X"+str(Kurt_X))

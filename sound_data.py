import time #measure proceeding time to calculate Hz
import Adafruit_BBIO.ADC as ADC #use analog read
ADC.setup() 
import numpy as np
import requests #connect IFTTT
from scipy import signal #detect peak

# parameters
analogPin="P9_39"
sample_number = 2000
repeat_number = 2

sound_data = []
Gx = []
Gy = []

# IFTTT_Webhook
def ifttt_webhook(eventid):
    payload = {"value1": Gx_i,
                "value2": Gy_i,
                "value3": freq[maximal_idx] }
    url = "https://maker.ifttt.com/trigger/" + eventid + "/with/key/xxxxxxxxxxxxxxxxxxx"
    response = requests.post(url, data=payload)

# Starting measurement sound data

for i in range(10000):  #cutting launch time peak? noise?
    sound_data_t = ADC.read(analogPin)
    sound_data.append(sound_data_t)
    sound_data = []   #sound_data resset

for n in range(repeat_number):
 
    start_time = time.time()  #measureing time to calculate the frequency

    for i in range(sample_number):
        sound_data_t = ADC.read(analogPin)
        sound_data.append(sound_data_t)

    end_time = time.time()    #measureing time to calculate the frequency
    total_time = end_time - start_time    #measureing calculation time from start to end regarding getting sound data

    np.savetxt('raw_sound'+str(n)+'.csv',sound_data)  #for test. output csv data about raw sound data 

    #fast Fourier transform and revise the data
    F = np.fft.fft(sound_data)    #fast Fourier transform
    F_abs = np.abs(F)    #absolutely
    F_abs[0] = 0  #delete dc component
    F_abs = F_abs/sample_number*2  #translate the value
    for num in range(sample_number/2,sample_number): #delete after Nyquist constant value
       F_abs[num] = 0
    np.savetxt('sound'+str(n)+'.csv',F_abs)  #output csv data about F_abs

    F_abs_sum = np.sum(F_abs)   #sum all frequency of amplitude

    #making frequency data
    freq = np.arange(0, 1/total_time*1000*2, 1/total_time/sample_number*1000*2) # making Hz axis" 11/15 add *2"

    np.savetxt('sound_freq'+str(n)+'.csv',freq)   #output csv data about freq

    maximal_idx = signal.argrelmax(F_abs, order=100) #detect peak in FFT data
    print('peak Hz', freq[maximal_idx])
    print('peak Amplitude', F_abs[maximal_idx])

    #print("F_abs")   #for test
    #print(F_abs)    #for test
    #print("total_time")    #for test
    #print(total_time)    #for test

    Gx_i = np.dot(F_abs/F_abs_sum, freq)
    Gy_i = np.dot(F_abs/F_abs_sum, F_abs/2)
    Gx.append(Gx_i)
    Gy.append(Gy_i)

    # start
    if __name__ == '__main__':
        print ("IFTTT connecting start")

        # IFTTT_Webhook
        ifttt_webhook("BBB_sound_data")

        print ("IFTTT connecting end")

    sound_data = []
    freq[maximal_idx]=[]
    F_abs[maximal_idx]=[]
print("Gx")
print(Gx)    #the center of gravity about frequency
print("Gy")
print(Gy)    #the center of gravity about amplitude

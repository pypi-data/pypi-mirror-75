import scipy.io.wavfile as wavf
from scipy.io.wavfile import read
import numpy as np

def mix(source1,source2,dest,amp=1,freq=1):
    a = read(source1)    # to Read WAV file
    b = read(source2)

    sample1 = np.array(a[1])    # to convert it to numpy array
    sample2 = np.array(b[1])
    if len(sample1)>len(sample2) :
        sample1,sample2=sample2,sample1
    for i in range(len(sample1)):
        sample1[i]=sample1[i]+amp*sample2[i]  # Superimposing
        
    fs = 44100*freq    #frequency of sampling
    wavf.write(dest, fs, sample1)    #converting array to wav

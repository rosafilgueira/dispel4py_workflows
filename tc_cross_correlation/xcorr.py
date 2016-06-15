# -*- coding: utf-8 -*-
"""
Created on Mon Apr 07 09:32:54 2014

@author: abell5
"""

from obspy.signal.util import nextpow2
from scipy.fftpack import fft, ifft
from numpy import complex, conjugate, roll, copy

def xcorrf(trace1, trace2, shift=None):
    """
    Cross-correlation of numpy arrays data1 and data2 in frequency domain.
    """
    data1 = trace1.data
    data2 = trace2.data

    complex_result = (data1.dtype == complex or data2.dtype == complex)
    N1 = len(data1)
    N2 = len(data2)

    data1 = data1.astype('float64')
    data2 = data2.astype('float64')

    # Always use 2**n-sized FFT, perform xcorr
    size = max(2 * shift + 1, (N1 + N2) // 2 + shift)
    nfft = nextpow2(size)
    print size
    #Calculate fft of data1 and data2

    IN1 = fft(data1, nfft)
    IN2 = fft(data2, nfft)

    IN1 *= conjugate(IN2)

    ret = ifft(IN1)

    del IN1, IN2

    if not complex_result:
        ret = ret.real
    # shift data for time lag 0 to index 'shift'

    ret = roll(ret, -(N1 - N2) // 2 + shift)[:2 * shift + 1]

    return copy(ret)


def xcorrf_noFFT(IN1, IN2, shift=None):
    """
    Multiplication and IFFT of numpy arrays IN1 and IN2, already in frequency domain.
    """


    IN = IN1*conjugate(IN2)
    ret = ifft(IN)

    ret = ret.real
    ret = roll(ret, shift)[:2 * shift + 1]

    return copy(ret)



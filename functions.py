from scipy.interpolate import interp1d
import numpy as np
import scipy.signal as sg
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def trend_reduce(sample_data):
    """Wolfgang's MATLAB trend reduce code, adapted for Python"""
    data = np.asarray(sample_data)*1e9
    width = 400
    slope = 0.070
    dataLength = len(data)
    Time = np.arange(0, dataLength)

    r1 = np.arange(dataLength, 0, -1)*slope
    r2 = -1*(slope*width/np.pi)*np.sin(np.arange(0,width+1)*(np.pi/width))
    r3 = np.arange(0, dataLength)*slope
    CompareLong = np.array(r1)
    CompareLong = np.append(CompareLong, r2)
    CompareLong = np.append(CompareLong, r3)

    upperBoundary = np.amax(data)+0*data
    Compare = []
    for i in range(0,len(CompareLong)-dataLength-1):
        Compare = CompareLong[i:-1]
        Compare = Compare[0:dataLength]
        Compare = Compare + np.amax(data-Compare)
        upperBoundary = np.minimum(upperBoundary, Compare)

    FindUpperPoints = abs(upperBoundary - data)<(slope/4)
    upperLine = interp1d(Time[np.where(FindUpperPoints)], upperBoundary[np.where(FindUpperPoints)], kind='quadratic', fill_value='extrapolate')
    
    

    lowerBoundary = np.amin(data)+0*data
    Compare = []
    for i in range(0,len(CompareLong)-dataLength-1):
        Compare = -CompareLong[i:-1]
        Compare = Compare[0:dataLength]
        Compare = Compare - np.amax(Compare-data)
        lowerBoundary = np.maximum(lowerBoundary, Compare)

    FindLowerPoints = abs(lowerBoundary - data)<(slope/4)

    lowerLine = interp1d(Time[np.where(FindLowerPoints)], lowerBoundary[np.where(FindLowerPoints)], kind='quadratic', fill_value='extrapolate')

    middleLine = (upperLine(Time)+lowerLine(Time))/2
    middle = (upperBoundary+lowerBoundary)/2

    '''
    fig_t0 = plt.figure()
    plt_t0 = fig_t0.add_subplot(111)
    plt_t0.plot(Time, data)
    plt_t0.scatter(Time[np.where(FindUpperPoints)], upperBoundary[np.where(FindUpperPoints)], c='r')
    plt_t0.plot(Time, upperLine(Time))
    plt_t0.plot(Time, lowerBoundary, c='r')
    plt_t0.plot(Time, upperBoundary, c='r')
    plt_t0.scatter(Time[np.where(FindLowerPoints)], lowerBoundary[np.where(FindLowerPoints)], c='r')
    plt_t0.plot(Time, lowerLine(Time))
    plt_t0.plot(Time, middleLine)
    plt_t0.plot(Time, middle)

    plt.close()
    '''
    return (sample_data - middle/1e9)


def gaussian(x, amp, wid, cen):
    """Simple Gaussian curve function"""
    return amp*np.exp(-(x-cen)**2/(2*wid**2))


def double_gaussian(x, a1, w1, c1, a2, w2, c2):
    a = gaussian(x, a1, w1, c1)
    b = gaussian(x, a2, w2, c2)
    return a + b


def solve_quadratic(a,b,c):
    disc = b**2-4*a*c

    x1 = (-b + np.sqrt(disc))/(2*a)
    x2 = (-b - np.sqrt(disc))/(2*a)

    return x1, x2


def lorentzian(f, A, fc):
    """Defining a Lorentzian curve with coefficient A and cutoff frequency fc"""
    return A/(1+(2*np.pi*f/fc)**2)


def butter_lowpass_filter(data, cutoff, fs, order):
    nyq = 0.5 * fs
    cut = cutoff / nyq

    i, u = sg.butter(order, cut, btype='lowpass')
    y = sg.filtfilt(i, u, data)
    return y


def butter_highpass_filter(data, cutoff, fs, order):
    nyq = 0.5 * fs
    cut = cutoff / nyq

    i, u = sg.butter(order, cut, btype='highpass')
    y = sg.filtfilt(i, u, data)
    return y


def butter_bandstop_filter(data, lowcut, highcut, fs, order):
    """
    Used to create a bandstop region

    Parameters
    ----------
    data : array
        The data to filter

    lowcut : int or float
        -3dB point on low side (cutoff freq)
        
    highcut : int or float
        -3dB point on high side (cutoff freq)

    fs : float
        Sampling frequency of data

    order : int
        Order of butterworth filter
    
    Returns
    -------
    y : ndarray
        Filtered data
    """

    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq

    i, u = sg.butter(order, (low, high), btype='bandstop')
    y = sg.filtfilt(i, u, data)
    return y


def find_nearest(array, value):
    """ Finds the index closest in 'array' closest to 'value.' """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def calc_running_mean(x, n):
    cumulative_sum = np.cumsum(np.insert(x, 0, 0))
    return (cumulative_sum[n:] - cumulative_sum[:-n]) / float(n)


def many_gauss(x, *params):
    y = np.zeros_like(x)
    for i in range(0, len(params), 3):
        ctr = params[i]
        #print(ctr)
        amp = params[i+1]
        #print(amp)
        wid = params[i+2]
        #print(wid)
        y = y + amp * np.exp( -((x - ctr)/wid)**2)
        #print(y)
    return y

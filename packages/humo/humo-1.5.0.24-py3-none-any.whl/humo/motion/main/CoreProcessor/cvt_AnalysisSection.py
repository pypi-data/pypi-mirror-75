import functools
import numpy as np
from scipy.interpolate import splev, splrep

#This is a decorator that outputs the analysis section.
#Receives data output by div method and data at start and end of analysis section.
#The start time and the end time are data stored in the list.

def output_AnalysisSections(func):
    """Summary line.

    Parameters
    ----------
    arg1 : str
        Name of markers.

    Returns
    -------
    array(3 dimension)
        It is output in the order of x axis, y axis, z axis.

    Note
    -------
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data, sp, ep = func(*args, **kwargs)
        maxlength = (ep - sp).max()
        if type(args[1]) == list:
            analysissectionData = []
            for eachdata in data:
                analysissectionData_ = []
                for s, e, eachData in zip(sp, ep, eachdata):
                    mat = np.full([maxlength,3], np.nan)
                    mat[:(e-s),:] = eachData[s:e]
                    analysissectionData_.append(mat)
                analysissectionData.append(analysissectionData_)
            analysissectionData = np.array(analysissectionData)
                #    analysissectionData_.append(eachData[sp[trial]:ep[trial],:])
                #analysissectionData.append(analysissectionData_)
            #analysissectionData = np.array(analysissectionData)
        else:
            analysissectionData = []
            for s, e, eachdata  in zip(sp, ep, data):
                mat = np.full([maxlength,3],np.nan)
                mat[:(e-s), :] = eachdata[s:e,:]
                analysissectionData.append(mat)
            analysissectionData =  np.array(analysissectionData)
            #for trial, eachData in enumerate((data)):
            #    analysissectionData.append(eachData[sp[trial]:ep[trial],:])
            #analysissectionData = np.array(analysissectionData)
        return analysissectionData
    return wrapper

def output_AnalysisSections4EMG(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data, sp, ep = func(*args, **kwargs)
        maxlength = (ep - sp).max()
        if type(args[1]) == list:
            analysissectionData = []
            for i in data:
                analysissectionData_ = []
                for s, e, eachData in zip(s,e,i):
                    mat = np.full(maxlength, np.nan)
                    mat[:(e-s)] = eachData[s:e]
                    analysissectionData_.append(mat)
                analysissectionData.append(analysissectionData_)
                    #analysissectionData_.append(eachData[sp[trial]:ep[trial]])
                #analysissectionData.append(analysissectionData_)
            analysissectionData = np.array(analysissectionData)
        else:
            analysissectionData = []
            for s, e, eachData in zip(sp,ep,data):
                mat = np.full(maxlength, np.nan)
                mat[:(e-s)] = eachData[s:e]
                analysissectionData.append(mat)
            analysissectionData = np.array(analysissectionData)
                #analysissectionData.append(eachData[sp[trial]:ep[trial]])
            #analysissectionData = np.array(analysissectionData)
        return analysissectionData
    return wrapper


def time_normalize(data, length):
    x = np.arange(0,len(data[:,0]))
    interpolated_x = np.linspace(0, x[-1], length)
    interpolated_y = []
    for i in range(3):
        y = data[:,i]
        tck = splrep(x,y)
        interpolated_y.append(splev(interpolated_x, tck))
    return np.array(interpolated_y).T

def time_normalize4EMG(data, length):
    x = np.arange(0,len(data))
    y = data
    tck = splrep(x,y)
    interpolated_x = np.linspace(0, x[-1], length)
    interpolated_y = splev(interpolated_x, tck)
    return interpolated_y


def output_NormalizedSections(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data, length = func(*args, **kwargs)
        if type(args[1]) == list:
            normlaizedData = []
            for i in data:
                normlaizedData_ = []
                for eachData in i:
                    eachData = eachData[~np.isnan(eachData).any(axis=1),:]
                    normlaizedData_.append(time_normalize(eachData, length))
                normlaizedData.append(normlaizedData_)
            normlaizedData = np.array(normlaizedData)
        else:
            normlaizedData = []
            for i in data:
                i = i[~np.isnan(i).any(axis=1),:]
                normlaizedData.append(time_normalize(i, length))
            normlaizedData = np.array(normlaizedData)
        return normlaizedData
    return wrapper

def output_NormalizedSections4EMG(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data, length = func(*args, **kwargs)
        if type(args[1]) == list:
            normlaizedData = []
            for i in data:
                normlaizedData_ = []
                for eachData in i:
                    eachData = eachData[~np.isnan(eachData).any(axis=1),:]
                    normlaizedData_.append(time_normalize4EMG(eachData, length))
                normlaizedData.append(normlaizedData_)
            normlaizedData = np.array(normlaizedData)
        else:
            normlaizedData = []
            for i in data:
                i = eachData[~np.isnan(i).any(axis=1),:]
                normlaizedData.append(time_normalize4EMG(i, length))
            normlaizedData = np.array(normlaizedData)
        return normlaizedData
    return wrapper

import numpy as np

from numba import njit

@njit
def ply(arr, n=1000000):
    return arr1 * n

@njit
def div(arr1, arr2):
    return arr1 / arr2

@njit
def diff(values):
    values = values - np.roll(values, 1)
    values[0] = np.nan 
    return values

@njit
def growth(values):
    shift = np.roll(values, 1)
    shift[0] = np.nan
    return values / shift

@njit
def log(values):
    return np.log(values)

@njit
def log10(values):
    return np.log10(values)
    
@njit
def roll_mean(arr, n=3):
    if np.isnan(arr).all():
        return arr
    else:
        non_arr = arr[~np.isnan(arr)][1:]
        ret = np.cumsum(non_arr)
        ret[n:] = ret[n:] - ret[:-n]
        new_a = ret[n - 1:] / n
        if new_a.shape[0] == 0:
            
            return np.array([np.nan]*arr.shape[0])
        else:
            concat = np.concatenate((arr[np.isnan(arr)], np.array([np.nan]*(n)), new_a))
            return concat

@njit
def sum_axis(arr):
    arr = np.where(np.isnan(arr), 0, arr)
    return arr.sum(axis=1)

@njit
def nieve_interpo(arr1, arr2):
    midpoint = np.array([np.mean(np.array([arr1[-1], arr2[0]]))])
    return np.concatenate((arr1, midpoint, arr2))

@njit
def redistribute(prenegs, newsum):
    return (prenegs / prenegs[-1]) * newsum

@njit
def redistribute_jumps(new, countarr, jump, precount):
    """
    Redistributes large jumps in counts backwards through the count distribution

    Has to avoid NaN values in the early part of the dataset, therefore,
    only operates on the slice of newarr that comes after the early grouping
    of continuous NaNs
    """
    if precount.size != 0:
        countarr = np.concatenate((precount, countarr[precount.size:]))

    newarr = np.where(
        np.isnan(new), 
        countarr,
        new
    )
    nans_index = np.where(np.isnan(newarr))[0]
    num_nans = nans_index.shape[0]
    
    i = 0
    while True:
        i += 1
        if nans_index[0] == 0 and nans_index[-i] == num_nans - 1:
            last_nan = nans_index[-1]
            break
        num_nans -= 1
    
    newarr[last_nan + 1:] = (newarr[last_nan + 1:] / countarr[-1] * jump).cumsum() + countarr[last_nan + 1:]

    return newarr

@njit
def earlier_is_better(values, scale_factor=1):
    """
    Takes array of values and scales it so that
    earlier values are worth more than later ones

    When scale_factor == 1, y will be an array between 1 and ~0
    If scale_factor is > 1, then y.min() will increase
    So for scale_factor == 20, y.min() ~= 0.4
    """
    x = np.array([i for i in range(1, values.shape[0] + 1)])
    y = np.log(x) / np.log(1/values.shape[0]/scale_factor) + 1
    return np.multiply(values, y)

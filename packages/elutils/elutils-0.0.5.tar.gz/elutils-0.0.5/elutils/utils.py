'''Various misc utils that do not fit elsewhere'''
from collections import Counter
from collections.abc import Iterable
from datetime import datetime

# DICT INTERFACE
def sum_dicts(dicts:Iterable):
    '''takes a list of dicts as input and returns one dict with all values summed togeher'''

    if len(dicts)==0:
        return {}

    counter_dicts = [Counter(d) for d in dicts]

    result_dict = counter_dicts[0]
    for d in counter_dicts[1:]:
        result_dict += d
    return result_dict

# TIME
def current_time(sep='-'):
    '''Returns the current time as HH-MM-SS format
    can specify the separator between times, default to -'''
    now = datetime.now()
    current_time = now.strftime(f"%H{sep}%M{sep}%S")
    return current_time


def epoch_to_datetime(epoch_time,fmt=None):
    '''If fmt is provided it returns a string, otherwise datetime object'''
    converted= datetime.fromtimestamp(epoch_time)
    if fmt is None:
        return converted
    else:
        return datetime.strftime(converted,fmt)



if __name__ == '__main__':

    import time
    a=epoch_to_datetime(time.time())
    print(a)
    b = epoch_to_datetime(time.time(), fmt='%M:%H:%S')
    print(b)
    a = {"apples":4,"beets":12}
    b = {"apple":2,"beets":1,"oranges":2}
    
    print(sum_dicts([a,b]))

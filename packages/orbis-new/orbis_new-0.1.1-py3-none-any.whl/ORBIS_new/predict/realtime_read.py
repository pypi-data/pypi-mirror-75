# @Author : Donglai
# @Time   : 7/12/2020 2:02 AM
# @Email  : dma96@atmos.ucla.edu donglaima96@gmail.com

from datetime import datetime,timedelta
import numpy as np
import os
from scipy.io import savemat,loadmat

def datetime_to_datenum(date_time):
    """
    Convert Python datetime to Matlab datenum
    :param date_time: Datetime object
    :return: date_num in float
    """
    # change date to timestamp
    mdn = date_time + timedelta(days=366)
    frac = (date_time - datetime(date_time.year, date_time.month, date_time.day, 0, 0, 0)).seconds / (
            24.0 * 60.0 * 60.0)
    return mdn.toordinal() + frac


def pdframe_to_mat(pdframe, real_dir, res='1min'):
    """
    Change pdframe to a mat file
    the pdframe is like:
                         proton_density  flowspeed  flow_pressue
date
2020-05-29 00:00:00             3.8      291.1      0.644018
2020-05-29 00:01:00             3.6      292.7      0.616848
2020-05-29 00:02:00             3.8      293.0      0.652452
2020-05-29 00:03:00             4.0      292.6      0.684918
2020-05-29 00:04:00             4.1      293.2      0.704923

    # Change the datetime to datenum, I always to expand dims in matlab
        # In our dataset, all the datafile is composed of 'tdata' and 'data'
        # Each parameter has one name like'bz_gsm', 'flowspeed'...
        # The format is like source + name + resolution.mat
        # For OMNI it's like : 'omni_bz_gsm_1min.mat'
        # This time it's real so:'real_bz_gsm_1min.mat'
    @param pdframe:pdframe
    @param matname:the target mat file name
    @param dir:directory
    @return:1
    """
    tdata_datetime = pdframe.index.to_pydatetime()
    tdata = np.expand_dims(np.array([datetime_to_datenum(tdata_datetime[i])
                                     for i in range(0, len(tdata_datetime))]), axis=1)
    column_list = pdframe.columns.values

    if not os.path.exists(real_dir):
        os.makedirs(real_dir)
    for column_name in column_list:
        # The dir have a '/'
        file_name =real_dir + 'real_' + column_name + '_' + res + '.mat'
        data = np.expand_dims(pdframe[column_name].to_numpy(), axis=1)
        savemat(file_name, {'tdata': tdata, 'data': data})


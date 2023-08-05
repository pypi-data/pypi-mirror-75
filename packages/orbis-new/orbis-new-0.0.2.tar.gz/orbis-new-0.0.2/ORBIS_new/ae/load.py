# @Author : Donglai
# @Time   : 7/12/2020 2:47 AM
# @Email  : dma96@atmos.ucla.edu donglaima96@gmail.com
import os
from.config import CONFIG
import shutil
import urllib.request as request
from contextlib import closing
import pandas as pd
from datetime import datetime,timedelta
from ..predict.realtime_read import pdframe_to_mat


def load(time_now = None,time_history = 30,no_update  = False):
    """
    This funtion is load the ae real time data from 'http://mms.rice.edu/realtime/'
    @param time_history:
    @return: pdframe
    """
    if not os.path.exists(CONFIG['local_data_dir']):
        os.makedirs(CONFIG['local_data_dir'])

    file_name = 'archive_Rice_ae_1hr.txt'
    url = CONFIG['remote_data_dir'] + file_name
    file = CONFIG['local_data_dir'] + file_name

    with closing(request.urlopen(url)) as r:
        if os.path.exists(file) and no_update is True:
            print('File exist:',file)
        else:

            with open(file, 'wb') as f:
                shutil.copyfileobj(r, f)
                print('Downloading  %s' % file)

    AE_all = pd.read_csv(file,sep='\s+',parse_dates=[[5, 1, 2, 3]],header= None)
    AE_frame = AE_all.iloc[:,[0,3,4,5]]
    AE_frame.columns = ['date', 'ae_Boyel', 'ae_Ram', 'ae_Newell']

    # Add one hor prediction
    AE_predict_base = AE_frame[-1:]
    for i in range(4):
        predict = AE_frame[-1:].copy()
        predict['date'] += (i+1)*timedelta(minutes = 15)
        AE_predict_base = AE_predict_base.append(predict,ignore_index = True)




    AE_frame_new = AE_frame.append(AE_predict_base[1:],ignore_index = True)

    AE_frame_new.set_index('date',inplace = True, drop = True)

    if time_now is None:
        date_now = datetime.utcnow()
    else:
        date_now = time_now


    date_str = (date_now - timedelta(days = time_history)).strftime("%Y%m%d")
    AE_select = AE_frame_new[date_str:]
    pdframe_to_mat(AE_select,real_dir=CONFIG['real_data_dir'],res='15m')
    print('Finished')
    return AE_select


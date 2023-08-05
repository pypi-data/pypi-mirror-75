# @Author : Donglai
# @Time   : 7/12/2020 2:47 AM
# @Email  : dma96@atmos.ucla.edu donglaima96@gmail.com
import os
import numpy as np
from.config import CONFIG
from datetime import datetime, timedelta
import shutil
import urllib.request as request
from contextlib import closing
import pandas as pd
from scipy.io import savemat
from ..predict.realtime_read import pdframe_to_mat



def load(time_now = None,
         instrument = 'mag',
         res = '1m',

         no_update = False,

         time_history = 30,
         shift_min = 40):
    """
    This function loads data from the ACE realtime website
    @param start_time: start time of the trange(np.datetime64)
    @param end_time: end time of the trange(np.datetime64)
    @param instrument: 'mag' or 'swepam'
    @param res:'1min' or '5min'
    @param downloadonly: bool; True is only download the data
    @param shift_min: shift minutes to bow shock nose point
    @return:
    """
    if not os.path.exists(CONFIG['local_data_dir']):
        os.makedirs(CONFIG['local_data_dir'])
    if time_now is None:
        date_now = datetime.utcnow()
    else:
        date_now = time_now

    date_str_list = [(date_now - timedelta(days=x)).strftime("%Y%m%d")
                         for x in range(time_history)]
    date_str_list.sort()


    ###########
    # real time is false:
    #########

    name_suffix = 'ace_' + instrument + '_' + res +'.txt'

    filenames = [CONFIG['local_data_dir'] + x + '_' + name_suffix for x in date_str_list]
    urls = [CONFIG['remote_data_dir'] + x + '_'+ name_suffix for x in date_str_list]
    filenames.append(CONFIG['local_data_dir'] + name_suffix )
    urls.append(CONFIG['remote_data_dir'] + name_suffix)

    # download the file
    if no_update is True:
        pass
    else:
        no_update_list = filenames[:-2]
        for url,file in zip(urls,filenames):
            if os.path.exists(file) and file in no_update_list:
                print('File exist:',file)
                continue
            with closing(request.urlopen(url)) as r:
                with open(file, 'wb') as f:
                    shutil.copyfileobj(r, f)
                    print('Downloaded  %s'%file)

    # READ the file
    if instrument is 'mag':
        mag_pdframe_list = []
        for f in filenames:
            daily = pd.read_csv(f, skiprows=20, header=None, sep='\s+', na_values='-999.9',
                                parse_dates=[[0, 1, 2, 3]])
            daily_bz = daily.iloc[:, [0, 6]]
            daily_bz.columns = ['date', 'bz_gsm']
            # Add 40 minutes to simulate the bow shock nose point
            daily_bz.loc[:,'date'] +=timedelta(minutes=shift_min)

            daily_bz.set_index('date', inplace=True, drop=True)
            mag_pdframe_list.append(daily_bz)

        mag_all_raw = pd.concat(mag_pdframe_list)
        # Remove the conflict values in real data and the value in the latest'YYYYHHMM' file
        mag_all = mag_all_raw.groupby(mag_all_raw.index).first()
        pdframe_to_mat(mag_all,real_dir=CONFIG['real_data_dir'],res=res)
        return mag_all
    elif instrument is 'swepam':
        swepam_pdframe_list = []
        for f in filenames:
            daily = pd.read_csv(f, skiprows=18, header=None, sep='\s+', na_values='-9999.9',
                                parse_dates=[[0, 1, 2, 3]])
            daily_SW = daily.iloc[:, [0, 4, 5]]
            daily_SW.columns = ['date', 'proton_density', 'flowspeed']
            # Add timeshift to simulate the bow shock nose point
            daily_SW.loc[:, 'date'] += timedelta(minutes=shift_min)
            daily_SW.set_index('date', inplace=True, drop=True)
            swepam_pdframe_list.append(daily_SW)

        swepam_all_raw = pd.concat(swepam_pdframe_list)
        swepam_all = swepam_all_raw.groupby(swepam_all_raw.index).first()
        swepam_all['flow_pressure'] = 2e-6 * swepam_all['proton_density'] * (swepam_all['flowspeed']) ** 2
        pdframe_to_mat(swepam_all,real_dir=CONFIG['real_data_dir'],res=res)
        return swepam_all










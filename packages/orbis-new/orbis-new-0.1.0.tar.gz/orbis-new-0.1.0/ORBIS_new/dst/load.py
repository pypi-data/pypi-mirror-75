# @Author : Donglai
# @Time   : 7/20/2020 3:55 PM
# @Email  : dma96@atmos.ucla.edu donglaima96@gmail.com

from tkinter import *
# from functools import partial
#
# import argparse
# import time
import glob
# import traceback
import requests
import json
from datetime import datetime,timedelta
from requests.auth import HTTPDigestAuth, HTTPBasicAuth
from.config import CONFIG
import os
import numpy as np
import pandas as pd
from ..predict.realtime_read import pdframe_to_mat

def download_file(url,username,password):
    # Splits the URL to Get Filename

    local_filename = CONFIG['local_data_dir']+url.split('/')[-1]
    print(local_filename)
    # Downloads the File

    r = requests.get(url, stream=True, auth=HTTPBasicAuth(username, password))

    with open(local_filename, 'wb') as f:

        for chunk in r.iter_content(chunk_size=1024):

            if chunk:
                f.write(chunk)

    return local_filename


def load(time_now = None,time_history = 30, no_update = False):
    if not os.path.exists(CONFIG['local_data_dir']):
        os.makedirs(CONFIG['local_data_dir'])

    # Get the destination sub_folder name, which is in sub_folder
    if time_now is None:
        date_now = datetime.utcnow()
    else:
        date_now = time_now

    current_time = date_now
    print(current_time)

    # Convert Time to Most Current JB2008 File Push
    if int(current_time.minute) < 58:
        current_time = current_time - timedelta(hours=1)
    current_time = str(current_time)
    yr = current_time[0:4]
    mon = current_time[5:7]
    day = current_time[8:10]

    # Build UDL Path to JB2008 Data
    sub_folder = '/SupportingData/SGI/JB2008/' + yr + '/' + mon + '/' + day + '/'
    #print(sub_folder + '\n')



    if no_update is False:
        # Generate a widget to get username and password
        print('Please input your username and password!')
        root = Tk()
        nameVar = StringVar()
        passVar = StringVar()

        def getName():
            root.destroy()

        root.geometry('300x150')
        root.title('Unified Data Library')
        userLabel = Label(root, text="Enter Username")
        username = Entry(root, bd=5, textvariable=nameVar)
        pwLabel = Label(root, text="Enter Password")
        password = Entry(root, bd=5, textvariable=passVar, show='*')
        submit = Button(root, text="Submit", command=getName)

        userLabel.pack()
        username.pack()
        pwLabel.pack()
        password.pack()
        submit.pack(side=BOTTOM)
        root.mainloop()

        username = nameVar.get()
        password = passVar.get()
        # print(username,password)

        # After get the username and password, download the data

        host = CONFIG['remote_data_dir']
        services = CONFIG['services']

        url = host + services + '/list' + sub_folder

        headers = {'Content-type': 'application/json'}

        # Gets File List

        r = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, password))

        if (r.ok):

            d = json.loads(r.text)
            if len(d) == 0:
                return
            for index in [-4, -3, -2, -1]:
                if (d[index]['type'] == 'file'):
                    if 'DST' in str(d[index]['attributes']['name']):
                        dst_file_name = download_file(host + services + '/downloadFile' + d[index].get('id'),
                                      username,password)
                        print(type(dst_file_name))
        else:
            r.raise_for_status()
            dst_file_name = None
    else:
        dst_files = CONFIG['local_data_dir'] + '*DST*'
        if len(glob.glob(dst_files))>0:

            dst_file_name = glob.glob(dst_files)[-1]
            print(dst_file_name)
        else:
            dst_file_name = None


    if type(dst_file_name) is str:

        dst_f = open(dst_file_name, 'r')
    else:
        raise TypeError('dst file not exist!')

    data = dst_f.readlines()

    time_array = []

    dst_array = []

    for i, dst_line in enumerate(data):

        year = int(dst_line[3:5])

        if (year <= 99 and year >= 96):
            year = year + 1900

        if (year >= 00 and year <= 95):
            year = year + 2000

        month = int(dst_line[5:7])

        day = int(dst_line[8:10])

        for h in range(24):
            time_array.append(datetime(year, month, day, hour=h))

            dst_data = int(dst_line[h * 4 + 20:h * 4 + 24])
            dst_array.append(dst_data)

    date_all = np.array(time_array)
    dst_all = np.array(dst_array)
    start_time = datetime.utcnow() - timedelta(days=time_history)
    end_time = datetime.utcnow() + timedelta(hours=2)

    index = np.where((date_all > start_time) & (date_all < end_time))

    dst_frame = pd.DataFrame({'date': date_all[index], 'dst': dst_all[index]})
    dst_frame.set_index('date', inplace=True, drop=True)
    pdframe_to_mat(dst_frame, real_dir=CONFIG['real_data_dir'], res='60m')

    # dst_mean = round(dst_data[0:24].mean())

    # dst_matrix.append(dst_data)

    # =np.append(dst_matrix,dst_data,axis=0)

    # if( abs(dst_data[24] - dst_mean) > 1.0 and (dst_data[24] != 9999)):

    #    print(i,dst_mean,dst_data[24],dst_line)

    return dst_frame




# def load(dst_file,time_history = 30):
#
#
#     dst_f = open(dst_file, 'r')
#
#     data = dst_f.readlines()
#
#     time_array = []
#
#     dst_array = []
#
#     for i, dst_line in enumerate(data):
#
#         year = int(dst_line[3:5])
#
#         if (year <= 99 and year >= 96):
#             year = year + 1900
#
#         if (year >= 00 and year <= 95):
#             year = year + 2000
#
#         month = int(dst_line[5:7])
#
#         day = int(dst_line[8:10])
#
#         for h in range(24):
#
#             time_array.append(datetime(year, month, day,hour=h))
#
#             dst_data =int(dst_line[h * 4 + 20:h * 4 + 24])
#             dst_array.append(dst_data)
#
#
#     date_all = np.array(time_array)
#     dst_all = np.array(dst_array)
#     start_time = datetime.utcnow() - timedelta(days=time_history)
#     end_time = datetime.utcnow() + timedelta(hours=2)
#
#     index = np.where((date_all>start_time) & (date_all < end_time))
#
#
#     dst_frame= pd.DataFrame({'date':date_all[index],'dst':dst_all[index]})
#     dst_frame.set_index('date',inplace = True, drop = True)
#     pdframe_to_mat(dst_frame,real_dir=CONFIG['real_data_dir'],res='60m')
#
#         # dst_mean = round(dst_data[0:24].mean())
#
#         #dst_matrix.append(dst_data)
#
#         # =np.append(dst_matrix,dst_data,axis=0)
#
#         # if( abs(dst_data[24] - dst_mean) > 1.0 and (dst_data[24] != 9999)):
#
#         #    print(i,dst_mean,dst_data[24],dst_line)
#
#     return dst_frame
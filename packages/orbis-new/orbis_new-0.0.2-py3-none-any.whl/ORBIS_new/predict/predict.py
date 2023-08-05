# @Author : Donglai
# @Time   : 7/12/2020 1:57 AM
# @Email  : dma96@atmos.ucla.edu donglaima96@gmail.com



import numpy as np
from scipy.io import loadmat,savemat
import os
from datetime import datetime, timedelta
from scipy.interpolate import interp1d
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import tempfile
from .config import CONFIG
from .. import dst_kyoto
from .. import ae
from .. import ace
from .. import dst

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import pkgutil



def real_load_mat(datatype,res,dir):
    """
    This function should load the real data and history data,
    the file format should be the same like:"omni_flowspeed_1min.mat"
    ACE data need to do a timeshift and calculate the

    @param datatype: The name of index :AE, SYMH, flowspeed, pressure, Bz_gsm
    @param res: resolution of the data,like 1 min
    @param dir: direction
    @return: data
    """
    dir_real = dir
    file_mat = dir_real + 'real_' + datatype + '_' + str(res) + 'm.mat'

    if (os.path.isfile(file_mat)):
        data = loadmat(file_mat)
        return data
    else:
        raise IOError('Real file does not exist:' + file_mat)

    pass


#
# def omni_load_mat(datatype, res, dir):
#     ''' Load OMNI data. '''
#     dir_omni = dir + '//omni//'
#     file_mat = dir_omni + 'omni_' + datatype + '_' + str(res) + 'min.mat'
#
#     if (os.path.isfile(file_mat)):
#         data = loadmat(file_mat)
#         return data
#     else:
#         raise IOError('Omni file does not exist:' + file_mat)

def fill_gap(list_input, max_gap):
    """
    interpolate the gap in the list
    :param list_input: The input list
    :param max_gap: the max gap allowed to be filled
    :return: new list
    """
    # Find where is the gap

    n = np.concatenate(([False], np.isnan(list_input), [False]))
    index = np.where(n[:-1] != n[1:])[0]

    # Find data turning point

    if len(index) > 1:
        for i in range(len(index) - 1):
            if np.isnan(list_input[index[i]]) and (index[i + 1] - index[i]) <= max_gap and (
                    index[i] > 0 and index[i + 1] < len(list_input)):  # fill the gap now

                difference = list_input[index[i + 1]] - list_input[index[i] - 1]
                gap_length = index[i + 1] - index[i]
                for gap_count in range(index[i + 1] - index[i]):
                    list_input[index[i] + gap_count] = (difference / (gap_length + 1)) * (gap_count + 1) + \
                                                       list_input[index[i] - 1]

    return list_input

def datenum_to_datetime(date_num):
    """
    Convert Matlab datenum into Python datetime.
    :param datenum: Date in datenum format
    :return:        Datetime object corresponding to datenum.
    """
    days = date_num % 1
    return datetime.fromordinal(int(date_num)) \
           + timedelta(days=days) \
           - timedelta(days=366)

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

def time_series_init(start_time, end_time, time_res):
    """
    Make a time series in (datetime, datenum)
    :param start_time: datetime of start time
    :param end_time: datetime of end time
    :param time_res: time resolution in min
    :return: time_date, time_datenum
    """
    time_resolution = timedelta(minutes=time_res)
    date_series_np = np.arange(start_time, end_time, time_resolution)
    date_series = date_series_np.astype(datetime)
    datenum_series = np.array([datetime_to_datenum(date_series[i]) for i in range(0, len(date_series))])
    return date_series, datenum_series

# def _extract_from_package(resource):
#     data = pkgutil.get_data('tempocnn', resource)
#     with tempfile.NamedTemporaryFile(prefix='model', suffix='.h5', delete=False) as f:
#         f.write(data)
#         name = f.name
#     return name

class FluxPredict(object):
    def __init__(self,
                 model_dir=CONFIG['model_dir'],
                 data_dir = CONFIG['real_data_dir'],
                 model_name = 'DL_15',
                 start_time=datetime(2017, 2, 1, 8, 0),
                 end_time=datetime(2017, 2, 11, 12, 0),
                 interp_time_res = 1,
                 channel=1,
                 data_type='rbsp',  # Another possible data_type is 'mageis'
                 ##############################
                 real_flag = True,

                 model_description='This is a 15 day history test model for radiation belt',
                 mindex=['ae_Boyel','dst','flowspeed','flow_pressure','bz_gsm'],
                 mres=np.array([15, 60, 1, 1, 1], dtype=np.int),
                 mwindow=np.array([180, 180, 180, 180, 180], dtype=np.int),
                 gap_max=np.array([100, 10, 144, 144, 144], dtype=np.int),
                 mdlag=np.array([180, 180, 180, 180, 180], dtype=np.double),
                 mlag0=np.array([0, 0, 0, 0, 0], dtype=np.double),
                 mlag1=np.array([21600, 21600, 21600, 21600, 21600], dtype=np.double),
                 L_range=[3, 6],
                 L_res=0.25,
                 L_num=12
                 ):
        self.data_dir = data_dir
        self.model_dir = model_dir
        self.start_time = start_time
        self.end_time = end_time
        self.channel = channel
        self.data_type = data_type
        self.model_name = 'DL_15'
        self.interp_time_res = interp_time_res
        self.X_input = None
        self.y_test = None
        self.L_range = L_range
        self.L_res = L_res
        self.L_num = L_num

        # Model information
        # Predict flag ,it true, means the real time data
        self.predict_flag = real_flag




        # model parameters
        self._model_name = model_name
        self._model_description = model_description
        self._mres = mres
        self._mindex = mindex
        self._mwindow = mwindow
        self._gap_max = gap_max
        self._mdlag = mdlag
        self._mlag0 = mlag0
        self._mlag1 = mlag1

        self._mwindow_index = (mwindow / mres).astype(int)
        self._fill_gap_flag = True

    def load_input(self):
        """
        This function is for loading the input from omni data
        @return: The input of model without time
        """
        #################################



        print('Loading input...')
        nindex = np.array([(self._mlag1[i] - self._mlag0[i]) / self._mdlag[i] + 1
                           for i in range(len(self._mdlag))]).astype(np.int)

        idx0 = np.append(0, np.cumsum(nindex)).astype(int)

        # Make a time series based on start_time and end_time
        self.total_tdata, self.total_tdata_datenum = time_series_init(self.start_time, self.end_time,
                                                            self.interp_time_res)


        ndata = len(self.total_tdata_datenum)
        ensem = np.empty([ndata, np.sum(nindex).astype(int)], dtype=np.double)



        for iidx, (index, res, window, gap_max) in enumerate(
                zip(self._mindex, self._mres, self._mwindow_index, self._gap_max)):
            ###########################################
            # if self.predict_flag:
            #     data = real_load_mat(index,res,self.data_dir)
            # else:
            #     data = omni_load_mat(index, res, self.data_dir)
            data = real_load_mat(index, res, self.data_dir)
            lags = np.linspace(self._mlag0[iidx], self._mlag1[iidx], num=nindex[iidx])
            # print(nindex,lags)
            mean_data_raw = data['data'].squeeze()
            time_raw = data['tdata'].squeeze()
            # change the omni time range for time history
            index_new = np.where(time_raw > (self.total_tdata_datenum[0] - 16))
            time_raw = time_raw[index_new]
            mean_data_raw = mean_data_raw[index_new]
            weights = np.ones(window) / window
            if self._fill_gap_flag:
                mean_data_temp = fill_gap(mean_data_raw, gap_max)
                mean_data_raw = mean_data_temp
                print('filling gap ...')

            mean_data = np.convolve(weights, mean_data_raw)[window - 1:-window + 1]

            mean_data_new = np.append(np.repeat(mean_data[0], window - 1), mean_data)
            fint = interp1d(time_raw, mean_data_new)

            for ilag, lag in enumerate(lags):

                ensem[:, ilag + idx0[iidx]] = fint(self.total_tdata_datenum - lag / 1440).flatten()

        self.input_total_data = ensem
        print('Load input success')



        # Now keep the data finite
        # remove the inf and NAN in the input value

        t_temp = np.expand_dims(self.total_tdata_datenum,axis=1)
        print('keeping finite...')
        TOTAL = np.concatenate((t_temp, self.input_total_data), axis=1)
        TOTAL_nan = TOTAL[~(np.isnan(TOTAL).any(axis=1))]
        TOTAL_new = TOTAL_nan[~(np.isinf(TOTAL_nan).any(axis=1))]
        print('keeping finite finished')
        self.total_tdata_datenum_finite = TOTAL_new[:, 0]
        self.X_input = TOTAL_new[:, 1:(self.input_total_data).shape[1] + 1]
        self.total_tdata_finite = np.array([datenum_to_datetime(self.total_tdata_datenum_finite[i])
                                            for i in range(0, len(self.total_tdata_datenum_finite))])

        return self.X_input

    def get_flux(self):
        """
        Use X_input to calculate the flux
        @return: y_output in 12 dimension
        """
        if self.X_input is None:
            raise ValueError('Please first run load_input')
        # Load the machine learning model
        model_name = self.model_dir + self.model_name + '_model.h5'

        orbis_model = tf.keras.models.load_model(model_name)
        print('calculating predict flux...')
        self.y_test = np.array(orbis_model(self.X_input))
        print('Success')
        return self.y_test

    def get_dataframe(self):
        """
        Combine the time and make an matrix
        @return: A panda dataframe
                Time    L_bin_0    L_bin_1 .... L_bin_11
        """
        if self.y_test is None:
            raise ValueError('Please first run load_input then run get_flux')

        # name_list = ['L_bin' + str(i) for i in range(self.L_num)]
        # orbis_dataFrame = pd.DataFrame(data=self.y_test, index=self.total_tdata_finite,columns = name_list)
        # print(orbis_dataFrame)
        print(self.y_test.shape)
        orbis_data = self.y_test.flatten()
        orbis_time = np.repeat(self.total_tdata_finite,self.L_num,axis = 0)
        orbis_L = np.tile(np.arange(self.L_range[0],self.L_range[1],self.L_res),len(self.y_test))
        orbis_dataFrame = pd.DataFrame({'time':orbis_time,'L':orbis_L,'eflux':orbis_data})
        return orbis_dataFrame

    def make_predict_plot(self,save = True):
        """
        Make the predict plot
        @param save: The flag of whether save the flag

        """
        if self.y_test is None:
            raise ValueError('Please first run load_input then run get_flux')
        eflux_data = np.transpose(self.y_test)
        fig,ax = plt.subplots(figsize = (12,8))
        norm = plt.Normalize(0.1, 6.5)
        L_data = np.arange(self.L_range[0],self.L_range[1]+self.L_res,self.L_res)
        time_mesh,L_mesh = np.meshgrid(self.total_tdata_finite, L_data)
        time_now = datetime.utcnow()
        predict_plot = ax.pcolormesh(time_mesh,L_mesh,eflux_data,cmap='jet',norm=norm)
        color_axis_ml = inset_axes(ax, width="1%",  # width = 5% of parent_bbox width
                                   height="100%",
                                   loc='lower left',
                                   bbox_to_anchor=(1.05, 0., 1, 1),
                                   bbox_transform=ax.transAxes,
                                   borderpad=0,
                                   )
        ax.set_ylabel('L_shell')
        Channel_name = 'Channel_' + str(self.channel)
        ax.set_title('ORBIS_Prediction  ' + Channel_name)
        fig.colorbar(predict_plot,cax = color_axis_ml,label = "log(Eflux)")
        # time_plot_range = timedelta(days=1)
        # ax.set_xlim(self.total_tdata_finite[0],time_now + time_plot_range)
        ax.vlines(x = time_now,ymin = 3,ymax = 6,label='utcnow')
        ax.legend()
        fig.autofmt_xdate()

        if save:
            fig_name = self.model_name +'_'+Channel_name + '.png'
            plt.savefig(fig_name)
        fig.show()

    def download_model(self):
        """
        Load the model from ???

        @return:
        """
        # if not os.path.exists(CONFIG['model_dir']):
        #     os.makedirs(CONFIG['model_dir'])
        #   Then download the model
        if os.path.exists(CONFIG['model_dir'] + self.model_name +'model.h5'):
            print(self.model_name +' model exist!')
        else:
            raise ValueError('Model not exist!')

def get_realtime_flux(utcnow = datetime.utcnow(),
                  time_range = 3,
                  model_name = 'DL_15',noupdate = False,dst_version = 'dst',makeplot = True):
    """

    @param utcnow: datetime of utcnow or other datetime specific
    @param time_range: date of the time history
    @param model_name: name of the model
    @param noupdate: if no update is true, will use current files to calculate the
                    flux value.
    @param dst_version: 'dst' or 'dst_kyoto'
    @return: a panda data frame
    """
    time_now = utcnow
    start_time = time_now - timedelta(days=time_range)
    #end_time = time_now
    #orbis = FluxPredict(start_time=start_time, end_time=end_time, model_name=model_name)
    orbis = FluxPredict(start_time=start_time, model_name=model_name)
    orbis.ae_frame = ae.load(time_now=time_now, no_update=noupdate)
    orbis.swepam_frame = ace.load(time_now=time_now, instrument='swepam', no_update=noupdate)
    orbis.mag_frame = ace.load(time_now=time_now, instrument='mag', no_update=noupdate)
    if dst_version is 'dst':
        orbis.dst_frame = dst.load(time_now=time_now, no_update=noupdate)
    else:
        orbis.dst_frame = dst_kyoto.load()

    # get the predict end time
    end_time  = (np.min([orbis.ae_frame.index.values[-1],
          orbis.swepam_frame.index.values[-1],
          orbis.mag_frame.index.values[-1],
          orbis.dst_frame.index.values[-1]]))

    end_time_date = pd.Timestamp(end_time).to_pydatetime()

    orbis = FluxPredict(start_time=start_time, end_time=end_time_date, model_name=model_name)
    orbis.load_input()
    orbis.get_flux()
    orbis.predict_frame = orbis.get_dataframe()
    if makeplot:

        orbis.make_predict_plot()
    return orbis.predict_frame


    #orbis_input_data = orbis.load_input()


    # orbis.ae_frame = ae_frame
    # orbis.dst_frame = dst_frame
    # orbis.swepam_frame = swepam_frame
    # orbis.mag_frame = mag_frame


    #flux = orbis.get_flux()




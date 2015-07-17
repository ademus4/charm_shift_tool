from urllib import request
import re
import json
from pprint import pprint
from scipy.optimize import curve_fit
import numpy as np
from archive.database_call_v0 import lgdb_tools
from datetime import datetime, timedelta
import pandas as pd
import urllib

bpm_url = "https://ps-irrad.web.cern.ch/irrad/bpm.php?bpmid=BPM_0"
tf = '%Y-%m-%d %H:%M:%S'

def fwhm(sigma):
  return round(sigma*2.355,2)

class Timber_detectors(object):
  def fetch_from_timber(self, variable_name, filename, deltahours):
    a = lgdb_tools()
    t1 = (datetime.now()-timedelta(deltahours)).strftime(tf)
    t_now = (datetime.now()).strftime(tf)
    output = a.get_data(variable_name, t1, t_now, filename)
    return output

  def read_timber_data(self, filename, t_target, headers):
      print (filename)
      filename = './data/{}.csv'.format(filename)
      try:
        df = pd.read_csv(filename, delimiter=',', names=headers, index_col=False, skiprows=8)
      except:
        return pd.DataFrame()
      df['Time [local]'] = pd.to_datetime(df['Time [local]'])
      df = df.set_index('Time [local]')
      return df

class BPM:

  def integralMean(self,data):
    weight = 0.0
    weightedSum = 0.0
    for arr in data:
      weight += arr[1]
      weightedSum += arr[1]*arr[0];
    if(weight == 0):
      return (0)
    return round(weightedSum/weight,2)

  def sigma(self, data,mean):
    W = 0.0
    Q = 0.0
    for arr in data:
      W += arr[1]
      Q += arr[1]*(arr[0]-mean)*(arr[0]-mean)
    try:
      s = np.sqrt(Q/W);
      return round(s,2)
    except ZeroDivisionError:
      return 0.0

  # Returns dictionary that contains reference data aswell as the last 
  # 4 time stamped samplings
  def dl_bpm_data(self, url):
    bpm_error = False

    try:
      html = request.urlopen(url).read().decode("utf8")
    except:
      bpm_error = True # error when retrieving bpm data, check the mwpc
    json_table = re.findall(r"startData = (.*);",html)[0]
    try:
      data_dict = json.loads(json_table)
    except ValueError:
      print("Value Error in BPM data_dict!")
      bpm_error = True

    return data_dict, bpm_error

  def extract_xy_data(self, data_dict):
      data_arr = []
      
       # i in data_dict are each a dictionary which contains
       # the data array on index 'data'. The data array is
       # devided into several smaller arrays each containing x and y values like this
       # [[x0,y0], [x1,y1], ..., [xn,yn]]
      for i in data_dict:
        data = {}
        data['title'] = i['title']
        data['mean']  = self.integralMean(i['data'])
        data['sigma'] = self.sigma(i['data'], data['mean'])
        data['fwhm'] = fwhm(data['sigma'])
        int_arr = []
        for j in i['data']:
          int_arr.append(j[1])
        data['intensity'] = max(int_arr)
        # find the index of the highest value to know where above the X-axis it is
        data['centre'] = i['data'][int_arr.index(data['intensity'])][0]
        data_arr.append(data)

      return data_arr
  
  # returns the last samples from all the BPMs
  # both in the Y and X axis
  def get_bpm_data(self):
    xdata = []
    ydata = []
    for i in range(1,5):
      data, bpm_error = self.dl_bpm_data(bpm_url+str(i))
      xdata.append(self.extract_xy_data(data['X']))
      ydata.append(self.extract_xy_data(data['Y']))
    return xdata, ydata, bpm_error
  
class MWPC(Timber_detectors):

  def integralMean(self,x,y):
    weight = 0.0
    weightedSum = 0.0
    for i in range(len(x)):
      weight += y[i]
      weightedSum += y[i]*x[i];
    if(weight == 0):
      return (0)
    return round(weightedSum/weight,2)

  def sigma(self, x, y, mean):
    W = 0.0
    Q = 0.0
    for i in range(len(x)):
      W += y[i]
      Q += y[i]*(x[i]-mean)*(x[i]-mean)
    try:
      s = np.sqrt(Q/W);
      return round(s,2)
    except ZeroDivisionError:
      return 0.0

  def gauss(self, x, A, mu, sigma):
      p = -(x-mu)**2/(2.*sigma**2)
      p = list(p) # need to convert to list in order for np.exp to work
      return A*np.exp(p)

  def gaussian_fit_test(self,x_data,y_data):
      mwpc_error = False
      y_offset = np.min(y_data)
      x = np.array(x_data)
      y = np.array(y_data)-y_offset

      x_fine = np.arange(-100, 100, 0.1)  # x array, with finer resolution
      p = [1.0, 1.0, 75.0]             # initial fit params

      # If the MWPC data is really bad, a curve can't be fit to it
      # Alter the user
      try:
        coeff, pcov = curve_fit(self.gauss, x, y, p) # fit the params, get coeffs
      except RuntimeError:
        mwpc_error = True

      if not mwpc_error:
        y_fit = self.gauss(x_fine, *coeff)+y_offset                      # make a nice gaussian with fine x array

        peak,     centre,     sigma     = coeff
        peak_err, centre_err, sigma_err = np.sqrt(np.diag(pcov))

        fwhm = 2.355*sigma
        err_sigma  = (sigma_err/sigma)*100                    # std/sigma, % error for the FWHM value
      else:
        x_fine = y_fit = fwhm = err_sigma = centre = centre_err = float('nan') 

      return x_fine, y_fit, fwhm, err_sigma, centre, centre_err

  def get_data(self):
    n_spills = 10
    variable_name_h = 'MWPC.ZT8.135:PROFILE_H'
    variable_name_v = 'MWPC.ZT8.135:PROFILE_V'
    filename_v = 'mwpc_v'
    filename_h = 'mwpc_h'
    deltahours = 1
    headers = ['Time [local]']+[i for i in range(32)]

    self.fetch_from_timber(variable_name_v, filename_v, deltahours)
    self.fetch_from_timber(variable_name_h, filename_h, deltahours)

    t_now = (datetime.now()).strftime(tf)
    vdata = self.read_timber_data(filename_v, t_now, headers) 
    hdata = self.read_timber_data(filename_h, t_now, headers) 

    if (vdata.empty or hdata.empty):
        # An error occured in fetching mwpc data
        # returning infinity will cause an alert to be sent
        return float("inf"),float("inf"),float("inf"),float("inf")

    vdata = vdata[:t_now][-n_spills:]
    hdata = hdata[:t_now][-n_spills:]

    vdata_s = vdata.sum()
    vdata_d = vdata.std(axis=0)
    hdata_s = hdata.sum()
    hdata_d = hdata.std(axis=0)

    v_start = str(vdata.index[0]).split('.')[0]
    v_end   = str(vdata.index[-1]).split('.')[0]
    h_start = str(hdata.index[0]).split('.')[0]
    h_end   = str(hdata.index[-1]).split('.')[0]

    spacing = 6.0 # mm
    Lv = spacing*len(vdata_s.T)
    v_y_max = vdata_s.max().max()
    Lh = spacing*len(hdata_s.T)
    h_y_max = hdata_s.max().max()

    vx = ((np.array(vdata_s.index))*spacing)-(Lv/2.0)+(spacing/2)
    vy = vdata_s.values/n_spills
    hx = ((np.array(hdata_s.index))*spacing)-(Lh/2.0)+(spacing/2)
    hy = hdata_s.values/n_spills

    x_f, y_f, fwhm, err_sigma, centre, centre_err = self.gaussian_fit_test(vx, vy)
    fwhm_v = fwhm
    centre_v = centre

    x_f, y_f, fwhm, err_sigma, centre, centre_err = self.gaussian_fit_test(hx, hy)
    fwhm_h = fwhm
    centre_h = centre

    #v_intensity = vdata.ix[-1].max()
    #h_intensity = hdata.ix[-1].max()

    return fwhm_v, fwhm_h, centre_v, centre_h

class SEC(Timber_detectors):

  def __init__(self):
    self.calibration = {
        'SEC1': 2.2E7
    }

  def get_data(self):
    variable_name = 'MSC01.ZT8.107:COUNTS'
    filename = 'sec1_data'
    headers = ['Time [local]','Counts']
    deltahours = 0.25

    self.fetch_from_timber(variable_name, filename, deltahours)
    t_now = (datetime.now()).strftime(tf)
    print (t_now)
    f = open('data/' + filename + '.CSV')
    # Data from the SEC is not stored in timber if there is no beam.
    # we must therefore check that there is actually data in the timber
    # file we downloaded.
    if sum(1 for line in f) > 7:
      data = self.read_timber_data(filename, t_now, headers)
      data['pot/spill'] = data['Counts'].values*self.calibration['SEC1']
    else:
    #This should probably be fixed by using a custom pandas DataFrame
      data = t_now
    return data

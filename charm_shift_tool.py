from data_retriver import BPM, MWPC, SEC
from datetime import datetime, timedelta
from email_tools import alert

deviation = .3
calibration = {
    'SEC1': 2.2E7
}

def roundTime(dt=None, roundTo=60):
    '''
    Round a datetime object to any time laps in seconds
    dt : datetime.datetime object, default now.
    roundTo : Closest number of seconds to round to, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
    '''

    if dt == None: dt = datetime.now()
    seconds = (dt - dt.min).seconds
    # // is a floor division, not a comment on following line:
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return dt + timedelta(0,rounding-seconds,-dt.microsecond)

def bpm_msg(data, axis):
  # BPMs are numbered 1 through 4
  # index 0 contains refrence data,
  # and the last index contains the most recent sampling
  msg = axis 
  for d in data:
    for j in  ('intensity','fwhm'):
      if ((d[-1][j] > (1+deviation)*d[0][j]) or (d[-1][j] < (1-deviation)*d[0][j])):
        msg += 'Large deviation in the ' + j + ' of ' + str(d[-1]['title']) + '\n'
        msg += ' reference ' + j + ' ' + str(d[0][j]) + '\n'
        msg += ' current ' + j + ' ' + str(d[-1][j]) + '\n'
  return msg

def check_BPM():
  b = BPM()
  xdata, ydata = b.get_bpm_data()
  xmsg = bpm_msg(xdata, 'x-axis\n')
  ymsg = bpm_msg(ydata, 'y-axis\n')
  return xmsg, ymsg

def check_MWPC():
  m = MWPC()
  v_intensity, h_intensity, fwhm_v, fwhm_h = m.get_data()
  msg = "Vertical intesity: " + str(v_intensity) + " Horizontal intensity: " + str(h_intensity) + " Vertical FWHM: " + str(fwhm_v) + " Horizontal FWHM: " + str(fwhm_h)
  return msg

def check_SEC():
  s = SEC()
  data = s.get_data()
  reference = 3.5e11
  now = roundTime(datetime.now(), roundTo=60*60)
  try:
    intensity = (data['pot/spill'].mean())
    last_spill = data.index[-1]
    warning = '{} - PROBLEM! NO BEAM SINCE {}!'.format(datetime.now(), last_spill)
  except IndexError:
    return warning
  if ((intensity > (1+deviation)*reference) or (intensity < (1-deviation)*reference)):
    msg =  'SEC1 intesity: ' + str(intensity) + ' reference: ' + str(intensity)
  msg = ''
  return msg

xmsg, ymsg = check_BPM()
print(xmsg)
print(ymsg)
print("\n")
mwpc_msg = check_MWPC()
print(mwpc_msg)
print("\n")
sec_msg = check_SEC()
print(sec_msg)
print("\n")

#alert("Warning", xmsg+ymsg+mwpc_msg+sec_msg, 'charm_shift_tool@cern.ch', 'eino.juhani.oltedal@cern.ch')

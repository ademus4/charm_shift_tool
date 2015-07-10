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
  check_centre = False
  check_fwhm = False
  check_intensity = False
  msg = axis 
  for d in data:
    for j in  ('intensity','fwhm'):
      if ((d[-1][j] > (1+deviation)*d[0][j]) or (d[-1][j] < (1-deviation)*d[0][j])):
        msg += 'Large deviation in the ' + j + ' of ' + str(d[-1]['title']) + '\n'
        msg += ' reference ' + j + ' ' + str(d[0][j]) + '\n'
        msg += ' current ' + j + ' ' + str(d[-1][j]) + '\n'
        if (j == 'fwhm'):
          check_mwpc_fwhm = True
        elif (j == 'intensity'):
          check_sec_intensity  = True
    if  abs(d[-1]['centre'])  >= 4.5:
        msg += 'Off cenre: ' + str(d[-1]['centre']) + " of " + str(d[-1]['title']) + '\n'
        check_mwpc_centre = True #reference with the mwpc
  return msg, check_centre, check_fwhm, check_intensity

def check_BPM():
  b = BPM()
  xdata, ydata = b.get_bpm_data()
  xmsg, xcentre, xfwhm, xintensity = bpm_msg(xdata, 'x-axis\n')
  ymsg, ycentre, yfwhm, yintensity = bpm_msg(ydata, 'y-axis\n')
  return xmsg, ymsg, xcentre, xfwhm, xintensity, ycentre, yfwhm, yintensity

def check_MWPC():
  m = MWPC()
  ref_fv = 67
  ref_fh = 89
  ref_cv = .6
  ref_ch = 6.5
  msg = ""
  v_intensity, h_intensity, fwhm_v, fwhm_h, centre_v, centre_h = m.get_data()
  if abs(centre_v) > (1+deviation)*ref_cv:
    msg += "MWPC vertical center offset: " + str(centre_v) + " mm\n"
  if abs(centre_h) > (1+deviation)*ref_ch:
    msg += "MWPC horizontal center offset: " + str(centre_h) + " mm\n"
  if fwhm_v > (1+deviation)*ref_fv:
    msg += "MWPC vertical FWHM too large: " + str(fwhm_v) + " mm\n"
  if fwhm_h > (1+deviation)*ref_fh:
    msg += "MWPC horizontal FWHM too large: " + str(fwhm_h) + " mm\n"
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

xmsg = ""
ymsg = ""
mwpc_msg = ""
sec_msg = ""
xmsg, ymsg, xcentre, xfwhm, xintensity, ycentre, yfwhm, yintensity = check_BPM()
print(xmsg)
print(ymsg)
print("\n")
# Make sure the centre/fwhm is acutally off by also comparing to the SEC
if (xfwhm or xcentre or ycentre or yfwhm):
  mwpc_msg = check_MWPC()
mwpc_msg = check_MWPC()
print(mwpc_msg)
print("\n")
if (xintensity or yintensity):
# Make sure  the intensity is acutally off by also comparing to the SEC
  sec_msg = check_SEC()
  if sec_msg != '':
    alert("Warning", xmsg+ymsg+mwpc_msg+sec_msg, 'charm_shift_tool@cern.ch', 'eino.juhani.oltedal@cern.ch')
#alert("Warning", xmsg+ymsg+mwpc_msg+sec_msg, 'charm_shift_tool@cern.ch', 'eino.juhani.oltedal@cern.ch')

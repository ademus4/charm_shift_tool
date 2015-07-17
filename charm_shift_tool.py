from data_retriver import BPM, MWPC, SEC
from datetime import datetime, timedelta
from database_ctrl import *
from email_tools import alert
from database_ctrl import db_commands
import time
import urllib

tf = '%Y-%m-%d %H:%M:%S'
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
  db_cmd = db_commands()
  deviation = db_cmd.get_setting('deviation')
  del db_cmd
  check_centre = False
  check_fwhm = False
  msg = axis 
  for d in data:
    j = 'fwhm'
    if ((d[-1][j] > (1+deviation)*d[0][j]) or (d[-1][j] < (1-deviation)*d[0][j])):
      msg += 'Large deviation in the ' + j + ' of ' + str(d[-1]['title']) + '\n'
      msg += ' reference ' + j + ' ' + str(d[0][j]) + '\n'
      msg += ' current ' + j + ' ' + str(d[-1][j]) + '\n'
      if (j == 'fwhm'):
        check_fwhm = True
    if  abs(d[-1]['centre'])  >= 4.5:
        msg += 'Off centre: ' + str(d[-1]['centre']) + " of " + str(d[-1]['title']) + '\n'
        check_centre = True #reference with the mwpc
  return msg, check_centre, check_fwhm

def check_BPM():
  b = BPM()
  xdata, ydata, bpm_error = b.get_bpm_data()
  xmsg, xcentre, xfwhm = bpm_msg(xdata, 'x-axis\n')
  ymsg, ycentre, yfwhm = bpm_msg(ydata, 'y-axis\n')
  return xmsg, ymsg, xcentre, xfwhm, ycentre, yfwhm, bpm_error

def check_MWPC():
  db_cmd = db_commands()
  ref_fv = db_cmd.get_setting('mwpc_V_FWHM')
  ref_fh = db_cmd.get_setting('mwpc_H_FWHM')
  ref_cv = db_cmd.get_setting('mwpc_V_center')
  ref_ch = db_cmd.get_setting('mwpc_H_centre')
  deviation = db_cmd.get_setting('deviation')
  del db_cmd
  m = MWPC()
  msg = ""
  fwhm_v, fwhm_h, centre_v, centre_h = m.get_data()
  print ("MWPC: fwhm v: " + str(fwhm_v) + " fwhm_h: " + str(fwhm_h) + " centre_v: " + str(centre_v) + " centre_h: " + str(centre_h))
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
  db_cmd = db_commands()
  deviation = db_cmd.get_setting('deviation')
  del db_cmd
  s = SEC()
  data = s.get_data()
  reference = 3.5e11
  now = roundTime(datetime.now(), roundTo=60*60)
  msg = ''
  warning = '{} - PROBLEM! NO BEAM!'.format(datetime.now())
  try:
    intensity = (data['pot/spill'].mean())
    last_spill = data.index[-1]
    print ("SEC intensity: " + str(intensity))
  except:
    return warning
  if ((intensity > (1+deviation)*reference) or (intensity < (1-deviation)*reference)):
    msg =  'SEC1 intesity: ' + str(intensity) + ' reference: ' + str(intensity)
  return msg

def running():

  while True:
    xmsg = ""
    ymsg = ""
    mwpc_msg = ""
    sec_msg = ""
    subject = "Warning "
    warn_email = False

    #check only SEC for intensity
    sec_msg = check_SEC()
    print(sec_msg)
    if sec_msg != '':
      warn_email = True
      subject += 'BEAM DOWN! '

    xmsg, ymsg, xcentre, xfwhm, ycentre, yfwhm, bpm_error = check_BPM()
    print(xmsg)
    print(ymsg)
    print("\n")


    # Make sure the centre/fwhm is acutally off by also comparing to the SEC
    if (xfwhm or xcentre or ycentre or yfwhm or bpm_error):
      mwpc_msg = check_MWPC()
      print(mwpc_msg)
      print("\n")
      if mwpc_msg != '':
        warn_email = True
        subject += 'Beam off centre! '

    dbc = db_commands()
    last_msg = dbc.get_last_msg()
    t_now = (datetime.now()).strftime(tf)
    # Only send message if we haven't already
    if last_msg is None:
        if warn_email:
            alert(subject, xmsg+ymsg+mwpc_msg+sec_msg, 'charm_shift_tool@cern.ch', 'eino.juhani.oltedal@cern.ch')
            dbc.insert_msg((t_now, xmsg+ymsg+mwpc_msg+sec_msg, 0))
    else:
      if last_msg[-1] == 1:
        if warn_email:
            alert(subject, xmsg+ymsg+mwpc_msg+sec_msg, 'charm_shift_tool@cern.ch', 'eino.juhani.oltedal@cern.ch')
            dbc.insert_msg((t_now, xmsg+ymsg+mwpc_msg+sec_msg, 0))
      elif last_msg[-1] == 0 and warn_email == False: 
          # Beam is now up again
          alert("Notice CHARM beam is up again", "Beam up again at " + t_now, 'charm_shift_tool@cern.ch', 'eino.juhani.oltedal@cern.ch')
          dbc.insert_msg((t_now, "Beam up again.", 1))
    del dbc
    time.sleep(600)

if __name__ == "__main__":
    running()

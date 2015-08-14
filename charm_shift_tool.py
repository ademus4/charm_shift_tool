from data_retriver import BPM, MWPC, SEC
from datetime import datetime, timedelta
from database_ctrl import *
from email_tools import alert
from database_ctrl import db_commands
from shifter import get_shifter, get_date, get_all_shifters
from shift_tool_constants import whole_msg, new_shifter_msg
import time
import urllib

tf = '%Y-%m-%d %H:%M:%S'
calibration = {
    'SEC1': 2.2E7
}

def bpm_msg(data, axis):
  # BPMs are numbered 1 through 4
  # index 0 contains refrence data,
  # and the last index contains the most recent sampling
  db_cmd = db_commands()
  # divide by 100 because the database stores % not floats between 0 and 1
  deviation = db_cmd.get_setting('deviation')/100.
  del db_cmd
  check_centre = False
  check_fwhm = False
  msg = ""
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
  deviation = db_cmd.get_setting('deviation')/100.
  del db_cmd
  m = MWPC()
  fwhm_msg = ""
  centre_msg = ""
  fwhm_v, fwhm_h, centre_v, centre_h = m.get_data()
  print ("MWPC: fwhm v: " + str(fwhm_v) + " fwhm_h: " + str(fwhm_h) + " centre_v: " + str(centre_v) + " centre_h: " + str(centre_h))
  if abs(centre_v) > (1+deviation)*ref_cv:
    centre_msg += "MWPC vertical center offset: " + str(centre_v) + " mm\n"
  if abs(centre_h) > (1+deviation)*ref_ch:
    centre_msg += "MWPC horizontal center offset: " + str(centre_h) + " mm\n"
  if fwhm_v > (1+deviation)*ref_fv:
    fwhm_msg += "MWPC vertical FWHM too large: " + str(fwhm_v) + " mm\n"
  if fwhm_h > (1+deviation)*ref_fh:
    fwhm_msg += "MWPC horizontal FWHM too large: " + str(fwhm_h) + " mm\n"
  return centre_msg, fwhm_msg

def check_SEC():
  db_cmd = db_commands()
  dv = db_cmd.get_setting('deviation')
  if dv == None:
    #if there is no deviation setting use 30 as default
    dv = 30
  deviation = dv/100.
  del db_cmd
  s = SEC()
  data = s.get_data()
  reference = 3.5e11
  now = datetime.now()
  msg = ''
  warning = '{} - PROBLEM! NO BEAM!'.format(datetime.now())

  if type(data) == bool:
    # No recent sec data in timber
    return warning

  try:
    #check number of samples in last five minutes
    #there should be about 3.4 per minute
    #if it drops below 2.4 per minute, send a warning.
    #Do this because even if there has been no samples 
    #in the last five miutes, the intensity will still be high enough.
    fiveminago  = now - timedelta(minutes=5)
    samplecnt = 0
    timeindex = len(data.index)-1
    while (data.index[timeindex] > fiveminago):
      samplecnt += 1
      timeindex -= 1
    if (samplecnt < 10):
      return warning

    # Enough samples in the last 5 minutes, return intensity
    intensity = (data['pot/spill'].mean())
    last_spill = data.index[-1]
    print ("SEC intensity: " + str(intensity))
  except:
    return warning
  if ((intensity > (1+deviation)*reference) or (intensity < (1-deviation)*reference)):
    msg =  'SEC1 intesity: ' + str(intensity) + ' reference: ' + str(intensity)
  return msg

def phone2email(number):
  sms_address = '004175411{}@mail2sms.cern.ch'
  number = str(number)
  if number == '':
    sms_address = number
  elif len(number) == 4:
    sms_address = sms_address.format(7164)
  else:
    number = number.replace('+','00')
    sms_address = '{}@mail2sms.cern.ch'.format(number)
  return sms_address

def running():

  # If the shifter changes we want to send an email to the new shifter.
  prev_shifter = ''
  while True:
    xmsg = ""
    ymsg = ""
    centre_msg = ""
    fwhm_msg = ""
    sec_msg = ""
    beam_status = 1
    centre_status = 1
    fwhm_status = 1
    subject = "Warning "
    warn_email = False
    warn_centre_email = False
    warn_fwhm_email = False

    dbc = db_commands()

    last_msg = dbc.get_last_msg()
    response = dbc.get_response()

    # In order for the user and administrator intefaces to see all the shifters, they need to be stored in the database
    # To make sure that all shifters are stored in the data base we call get_all_shifters on both the database and the google sheet
    # Then we add all the shifters to the database that are in the google sheet but not yet in the database
    database_shifters = dbc.get_all_shifters()
    sheet_shifters = get_all_shifters()
    for name in sheet_shifters:
      if name not in database_shifters:
        dbc.insert_shifter({'name':name, 'email':'', 'phone':0, 'current':0, 'alert':0})


    shifter = get_shifter()
    alertees = dbc.get_alerts()
    recipients = []
    if shifter not in alertees:
      shifter_info = dbc.get_shifter_info(shifter)
      recipients.append(shifter_info['email'])
      sms = phone2email(shifter_info['phone'])
      recipients.append(sms)
    for name in alertees:
      shifter_info = dbc.get_shifter_info(name)
      recipients.append(shifter_info['email'])
      sms = phone2email(shifter_info['phone'])
      recipients.append(sms)

    # Send email if there is a new shifter
    if prev_shifter != shifter:
      prev_shifter = shifter
      dbc.set_current_shifter(shifter)
      shifttime=1400
      date,tomorrow = get_date(shifttime)
      shifter_msg = new_shifter_msg.format(shifter=shifter, date=date, tomorrow=tomorrow, shifttime=shifttime)
      print(shifter_msg)
      alert('New CHARM shifter {:s}'.format(shifter), shifter_msg, 'charm_shift_tool@cern.ch', recipients)
    
    #check only SEC for intensity
    sec_msg = check_SEC()
    if sec_msg != '':
      warn_email = True
      beam_status = 0
      centre_status = 0
      fwhm_status = 0
      subject += 'BEAM DOWN! '
    
    xmsg, ymsg, xcentre, xfwhm, ycentre, yfwhm, bpm_error = check_BPM()

    # Make sure the centre/fwhm is acutally off by also comparing to the SEC
    if (xfwhm or xcentre or ycentre or yfwhm or bpm_error):
      centre_msg, fwhm_msg = check_MWPC()
      if centre_msg != '':
        warn_centre_email = True
        subject += 'Beam off centre! '
      if fwhm_msg != '':
        warn_fwhm_email = True
        subject += 'Beam fwhm too wide '

    t_now = (datetime.now()).strftime(tf)

    # Only send message if we haven't already
    alert_msg = whole_msg.format(sec=sec_msg, x=xmsg, y=ymsg, centre=centre_msg, fwhm=fwhm_msg)    
    if last_msg is None:
        if warn_email or warn_fwhm_email or warn_centre_email:
            alert(subject, alert_msg, 'charm_shift_tool@cern.ch', recipients)
            dbc.insert_msg((t_now, alert_msg, 1*warn_email, 1*warn_fwhm_email, 1*warn_centre_email))
            dbc.respond(0)
    
    # Send the alerts if there is something wrong or if th ebeam is up again.
    else:
      if last_msg[-3] == 1 and warn_email:
        print(1)
        # If there is a warn_email, everything is down
        alert(subject, alert_msg, 'charm_shift_tool@cern.ch', recipients)
        dbc.insert_msg((t_now, alert_msg, 0, 0, 0))
        dbc.respond(0)
      elif last_msg[-3] == 0 and warn_email == False:
        print(2)
        # Beam is now up again
        alert("Notice CHARM beam is up again", "Beam up again at " + t_now, 'charm_shift_tool@cern.ch', recipients)
        dbc.insert_msg((t_now, "Beam up again.", 1,1*warn_fwhm_email,1*warn_centre_email))
        dbc.respond(1)
      elif (warn_fwhm_email == False and last_msg[-2] == 0) and (warn_centre_email == False and last_msg[-1] == 0):
        print(3)
        alert('Notic Beam Centered and FWHM Normal', alert_msg, 'charm_shift_tool@cern.ch', recipients)
        dbc.insert_msg((t_now, alert_msg, 1, 1, 1))
        dbc.respond(1)
      elif last_msg[-2] == 1 or last_msg[-1] == 1:
        print(4)
        # FWHM too large or Centre off
        if (warn_fwhm_email and last_msg[-2] == 1) or (warn_centre_email and last_msg[-1] == 1):
          alert(subject, alert_msg, 'charm_shift_tool@cern.ch', recipients)
          dbc.insert_msg((t_now, alert_msg, 1, 1*(not warn_fwhm_email), 1*(not warn_centre_email)))
          dbc.respond(0)
          # FWHM and Centre back to normal
        elif ((last_msg[-3] == 0 or last_msg[-2] == 0 or last_msg[-1] == 0) and response == (0,)):
          print(5)
          #Keep sending messages until user responds
          alert('Resending ' + subject, alert_msg, 'charm_shift_tool@cern.ch', recipients)
      elif ((last_msg[-3] == 0 or last_msg[-2] == 0 or last_msg[-1] == 0) and response == (0,)):
        print(5)
        #Keep sending messages until user responds
        alert('Resending ' + subject, alert_msg, 'charm_shift_tool@cern.ch', recipients)

    del dbc
    print(alert_msg)
    time.sleep(600)

if __name__ == "__main__":
    running()

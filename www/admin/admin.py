from database_ctrl import db_commands
import cgi
import cgitb

cgitb.enable()
db_cmd = db_commands()
shifters = db_cmd.get_all_shifters()
alertees = db_cmd.get_alerts()

ref_lables =['downtime','deviation', 'sec_ref','mwpc_V_FWHM',  'mwpc_V_center', 'mwpc_H_FWHM', 'mwpc_H_centre'] 
ref_tags = {'downtime':'Down time before users are alerted [min]','deviation':'Deviation before users are alerted [%]', 'sec_ref':'SEC reference [e10]','mwpc_V_FWHM':'MWPC vertical FWHM reference [mm]',  'mwpc_V_center':'MWPC vertical centre reference [e-1mm]', 'mwpc_H_FWHM':'MWPC horizontal FWHM reference [mm]', 'mwpc_H_centre':'MWPC horizontal centre reference [e-1mm]'}
ref_vals = {'downtime':10,'deviation':30, 'sec_ref':35,'mwpc_V_FWHM':67, 'mwpc_V_center':16, 'mwpc_H_FWHM':89, 'mwpc_H_centre':65}

print('Content-type:text/html\r\n\r\n')
print('<html>')
print('<header>')
print('<h1>Administrator Interface</h1>')
print('<title> Administrator Interface </title>')
print('<link rel=stylesheet href="adminstyle.css" type="text/css" media=all>')
print('</header>')
print('<body>')
f = open('admin/ref-form.html','r')
print('<form class="pure-form" action="./submit.py" method="POST">')

print('<fieldset>')
print('<legend>Reference values</legend>')
for label in ref_lables:
  setting = db_cmd.get_setting(label)
  print('<label for="{:s}">'.format(label))
  print('  {:s}'.format(ref_tags[label]))
  print('<input id="{x:s}" type="text" name="{x:s}" placeholder="{y:d}" value="{z:d}">'.format(x=label, y=ref_vals[label], z=setting))
  print('</label>')
  print('<br />')
print('</fieldset>')

print('<fieldset>')
print('<legend>Shifter Info</legend>')
print('<ul class="alert"> <li>Alert</li> </ul> <ul class="username"> <li>User Name</li> </ul> <ul class="emailphone"> <li>Email</li> <li>Phone Number</li></ul>')
print('<br />')
for user in shifters:
  shifter_info = db_cmd.get_shifter_info(user)
  checked = ""
  if user in alertees:
    checked = "checked"
  if len(shifter_info) == 0:
    email = ""
    phone = ""
  else:
    email = shifter_info['email']
    phone = str(shifter_info['phone'])
  print('<label for="email_{:s}">'.format(user))
  print(user)
  print('  <input id="alert_{i:s}" type="checkbox" name="alert{i:s}" {c:s}>'.format(i=user,p=phone,c=checked))
  print('  <input id="email_{i:s}" type="email" name="email{i:s}" value="{e:s}">'.format(i=user,e=email))
  print('  <input id="phone_{i:s}" type="text" name="phone{i:s}" value="{p:s}">'.format(i=user,p=phone))
  print('</label>')
  print('<br />')
print('</fieldset>')

print('<input type="submit" value="Submit Values">')
print('</form>')
print('</body>')
print('</html>')

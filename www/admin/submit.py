import cgi
import cgitb
from database_ctrl import db_commands

cgitb.enable()
form = cgi.FieldStorage()

db_cmd = db_commands()
print("Content-type:text/html\r\n\r\n")
print('<html>')
print('<head>')
print('<title>CHARM Shift Tool</title>')
print('<link rel=stylesheet href="adminstyle.css" type="text/css" media=all>')
print('</head>')
print('<body>')
print('Sending Response... Please Wait')
shifters = db_cmd.get_all_shifters()
# Html forms do not send checkboxes if they are not checked
# therefore we must collect all users who had the alert box checked
# set their alert variable to 1 in the database and the rest to 0
alertees = []
for key in form.keys():
  if 'alert' in key:
    alertees.append(key.replace('alert',''))
  if 'phone' in key:
    db_cmd.set_shifter_phone((key.replace('phone',''),form[key].value))
  elif 'email' in key:  
    db_cmd.set_shifter_email((key.replace('email',''),form[key].value))
  else:
    db_cmd.insert_setting((key,form[key].value))

for user in shifters:
  if user in alertees:
    db_cmd.set_alert((user,1))
  else:
    db_cmd.set_alert((user,0))

print('<script>')
print('window.location = "https://test-charmshifttool.web.cern.ch/test-charmshifttool/admin/admin.py";')
print('</script>')
print('</body>')
print('</html>')

from database_ctrl import db_commands
#from shifter import get_shifter
import cgi
import cgitb

cgitb.enable()
form = cgi.FieldStorage()
#if "name" not in form:
#    print "<H1>Error</H1>"
#    print "Please fill in the name and addr fields."
#    return
db_cmd = db_commands()
msgs = db_cmd.get_last_x_msgs(5)
status = db_cmd.get_beam_status()
response = db_cmd.get_response()
shifter = db_cmd.get_current_shifter()
print("Content-type:text/html\r\n\r\n")
print('<html>')
print('<head>')
print('<title>CHARM Shift Tool</title>')
print('<style type="text/css">body{margin:40px auto;max-width:650px;line-height:1.6;font-size:18px;color:#444;padding:0 10px}h1,h2,h3{line-height:1.2}b{padding:12px}</style>')
print('</head>')
print('<body>')

if status[0]:
  print('<b>Beam status: <font color=#009000>OK</font></b>')
else:
  print('<b>Beam status: <font color=#FF0000>DOWN</b></font>')

if status[1]:
  print('<b>Beam FWHM: <font color=#009000>OK</font></b>')
else:
  print('<b>Beam FWHM: <font color=#FF0000>DOWN</b></font>')

if status[2]:
  print('<b>Beam Centre: <font color=#009000>OK</font></b>')
else:
  print('<b>Beam Centre: <font color=#FF0000>DOWN</b></font>')
print('<p>')
if response == (1,):
  print('<button type="button" disabled="disabled"> Respond</button>')
else:
  print('<form name="input" action="/test-charmShiftTool/cgi-bin/respond.py" method="get">')
  print('<input type="submit" value="Respond">')
print('</p>')
print('<b>Current Shifter: ' + str(shifter) + '</b>')
print('<h2>Last Five Status Message</h2>')
for msg in msgs:
  print('<h4>'+msg[1]+'</h4>')
  print(msg[2].replace('\n','<br>'))
print('</body>')
print('</html>')


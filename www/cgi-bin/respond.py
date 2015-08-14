import cgi
import cgitb
from database_ctrl import db_commands

cgitb.enable()

db_cmd = db_commands()
db_cmd.respond(1)
print("Content-type:text/html\r\n\r\n")
print('<html>')
print('<head>')
print('<title>CHARM Shift Tool</title>')
print('<style type="text/css">body{margin:40px auto;max-width:650px;line-height:1.6;font-size:18px;color:#444;padding:0 10px}h1,h2,h3{line-height:1.2}</style>')
print('</head>')
print('<body>')
print('Sending Response... Please Wait')
print('<script>')
print('window.location = "https://test-charmshifttool.web.cern.ch/test-charmshifttool/cgi-bin/tool.py";')
print('</script>')
print('</body>')
print('</html>')

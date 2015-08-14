from database_ctrl import *
from datetime import datetime

tf = '%Y-%m-%d %H:%M:%S'

class Tester():

  def __init__(self):
    self.tests = 0
    self.errors = 0

  def testIfAsExpected(self, test, value, expected):
    if self.tests == 0:
      print()
      print("==================================================================================================================================================")
      print("== Starting testing.")
      print("==================================================================================================================================================")
    self.tests += 1
    if value == expected:
      msg = str(value)+", "
      result = "OK"
    else:
      self.errors += 1
      msg = "Actual value " + str(value) + ", expected value: " + str(expected)
      result = "FAIL"
    print("== Testing {t:<15} {m:<110} {r:s}".format(t=test+":",m=msg,r=result))

  def print_stats(self):
    print()
    print("==================================================================================================================================================")
    print("== Test Results.")
    print("==================================================================================================================================================")
    print("== Ran " + str(self.tests) + " test(s).")
    print("== Failed " + str(self.errors) + " test(s).")
    print("== " + str(100-self.errors/self.tests*100) + "% of the tests executed correctly.")

dbc = db_commands()
t = Tester()

def test_shifter_functions(self):
# test shifter functions
  shifter = {'name':'Eino', 'email':'eino.juhani.oltedal@cern.ch','phone':4741760950,'current':0,'alert':1}
  dbc.insert_shifter(shifter)
  print(dbc.get_shifter_info('Eino').values())
  t.testIfAsExpected('Insert Shifter', dbc.get_shifter_info('Eino'), shifter)
  shifter = {'name':'Maris', 'email':'maris.tali@cern.ch','phone':9999999999,'current':1,'alert':0}
  dbc.insert_shifter(shifter)
  t.testIfAsExpected('Insert Shifter', dbc.get_shifter_info('Maris'), shifter)

  t.testIfAsExpected('Set Shifter', dbc.get_current_shifter(), 'Maris')
  dbc.set_current_shifter('Eino')
  t.testIfAsExpected('Change Shifter', dbc.get_current_shifter(), 'Eino')

  t.testIfAsExpected('Get Alertees', dbc.get_alerts(), ['Eino'])
  dbc.set_alert(('Maris',1))
  t.testIfAsExpected('Get Alertees', dbc.get_alerts(), ['Eino','Maris'])

print(dbc.get_all_shifters())


t.print_stats()

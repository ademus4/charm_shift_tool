import sys
#from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from cst import Ui_MainWindow
from database_ctrl import db_commands

class GUI(QMainWindow, Ui_MainWindow):
  def __init__(self, parent = None):

    QMainWindow.__init__(self, parent)

    self.setupUi(self)

  def update_msg(self):
    db_cmd = db_commands()
    msg = db_cmd.get_last_msg()
    msg = msg[2]
    _translate = QCoreApplication.translate
    self.plainTextEdit.setPlainText(_translate("MainWindow", msg))

  def update_spinbox_vals(self):
    db_cmd = db_commands()
    self.downTimeBox.setValue(db_cmd.get_setting('downtime'))
    self.deviationBox.setValue(db_cmd.get_setting('deviation'))
    self.secRefBox.setValue(db_cmd.get_setting('sec_ref'))
    self.mwpcVFwhmRefBox.setValue(db_cmd.get_setting('mwpc_V_FWHM'))
    self.mwpcHFwhmRefBox.setValue(db_cmd.get_setting('mwpc_H_FWHM'))
    self.mwpcVCentreRefBox.setValue(db_cmd.get_setting('mwpc_V_center'))
    self.mwpcHCentreRefBox.setValue(db_cmd.get_setting('mwpc_H_centre'))

if __name__ == '__main__':
  cst = QApplication(sys.argv)
  window = GUI()

  window.show()
  window.update_msg()
  window.update_spinbox_vals()

  sys.exit(cst.exec_())


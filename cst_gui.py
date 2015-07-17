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

  def update_msg(self, msg):
    _translate = QCoreApplication.translate
    self.plainTextEdit.setPlainText(_translate("MainWindow", msg))

if __name__ == '__main__':
  cst = QApplication(sys.argv)
  window = GUI()

  window.show()
  db_cmd = db_commands()
  msg = db_cmd.get_last_msg()
  print(msg)
  window.update_msg(msg[2])
  #appLabel = QQuickView()
  #appLabel.setSource(QUrl('cst.qml'))

  #appLabel.show()

  #cst.exec_()
  sys.exit(cst.exec_())


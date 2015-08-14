

# Form implementation generated from reading ui file 'cst.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from database_ctrl import db_commands
from shifter import get_all_shifters

class Ui_MainWindow(object):

    def __init__(self):
      self.db_cmd = db_commands()

    def downtime_changed(self, value):
        self.db_cmd.insert_setting(("downtime", value))

    def deviation_changed(self, value):
        self.db_cmd.insert_setting(("deviation", value))

    def sec_ref_changed(self, value):
        self.db_cmd.insert_setting(("sec_ref", value))

    def mwpc_V_FWHM_changed(self, value):
        self.db_cmd.insert_setting(("mwpc_V_FWHM", value))

    def mwpc_V_centre_changed(self, value):
        self.db_cmd.insert_setting(("mwpc_V_center", value))
    
    def mwpc_H_FWHM_changed(self, value):
        self.db_cmd.insert_setting(("mwpc_H_FWHM", value))
    
    def mwpc_H_centre_changed(self, value):
        self.db_cmd.insert_setting(("mwpc_H_centre", value))

    def load_defaults(self):
        self.db_cmd.insert_setting(("downtime", 10))
        self.db_cmd.insert_setting(("deviation", 30))
        self.db_cmd.insert_setting(("sec_ref", 35))
        self.db_cmd.insert_setting(("mwpc_V_FWHM", 67))
        self.db_cmd.insert_setting(("mwpc_V_center", 16))
        self.db_cmd.insert_setting(("mwpc_H_FWHM", 89))
        self.db_cmd.insert_setting(("mwpc_H_centre", 65))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 908)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(590, 0, 431, 541))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy)
        self.plainTextEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 591, 541))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.mwpcVCentreRefBox = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.mwpcVCentreRefBox.setMaximum(999)
        self.mwpcVCentreRefBox.setObjectName("mwpcVCentreRefBox")
        self.gridLayout.addWidget(self.mwpcVCentreRefBox, 4, 1, 1, 1)
        self.mwpcVFwhmRefBox = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.mwpcVFwhmRefBox.setMaximum(999)
        self.mwpcVFwhmRefBox.setObjectName("mwpcVFwhmRefBox")
        self.gridLayout.addWidget(self.mwpcVFwhmRefBox, 3, 1, 1, 1)
        self.mwpcHCentreRefBox = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.mwpcHCentreRefBox.setMaximum(999)
        self.mwpcHCentreRefBox.setObjectName("mwpcHCentreRefBox")
        self.gridLayout.addWidget(self.mwpcHCentreRefBox, 6, 1, 1, 1)
        self.secRefBox = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.secRefBox.setMaximum(999)
        self.secRefBox.setObjectName("secRefBox")
        self.gridLayout.addWidget(self.secRefBox, 2, 1, 1, 1)
        self.downTimeBox = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.downTimeBox.setMaximum(120)
        self.downTimeBox.setObjectName("downTimeBox")
        self.gridLayout.addWidget(self.downTimeBox, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.mwpcHFwhmRefBox = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.mwpcHFwhmRefBox.setMaximum(999)
        self.mwpcHFwhmRefBox.setObjectName("mwpcHFwhmRefBox")
        self.gridLayout.addWidget(self.mwpcHFwhmRefBox, 5, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.deviationBox = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.deviationBox.setMaximum(999)
        self.deviationBox.setObjectName("deviationBox")
        self.gridLayout.addWidget(self.deviationBox, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 7, 0, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 540, 1021, 281))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 0, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout_4.addWidget(self.label_13, 0, 3, 1, 1)

        self.all_user_boxes = []
        self.emailEdits = []
        self.phoneEdits = []
        self.usernames = []
        self.alert_checkboxes = []
        num_shifters = len(get_all_shifters())
        for i in range(num_shifters):
          myLabel = QtWidgets.QLabel(self.gridLayoutWidget_2) 
          myLabel.setObjectName("user_label_"+str(i))
          self.all_user_boxes.append(myLabel)
          self.usernames.append(myLabel)
          for j in range(2):
            myLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
            myLineEdit.setObjectName("lineEdit_"+str(i+j))
            self.all_user_boxes.append(myLineEdit)
            if j == 0:
              self.emailEdits.append(myLineEdit)
            else:
              self.phoneEdits.append(myLineEdit)
          checkBox = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
          checkBox.setText("")
          checkBox.setObjectName("checkBox_"+str(i))
          self.all_user_boxes.append(checkBox)
          self.alert_checkboxes.append(checkBox)

        i = 0
        for j in range(2,num_shifters+2):
          for k in range(0,4):
            self.gridLayout_4.addWidget(self.all_user_boxes[i], j, k, 1, 1)
            i += 1

        self.label_10 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 0, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_9.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_4.addWidget(self.label_9, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 38))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.deviationBox.valueChanged['int'].connect(MainWindow.deviation_changed)
        self.pushButton.clicked.connect(MainWindow.load_defaults)
        self.mwpcVCentreRefBox.valueChanged['int'].connect(MainWindow.mwpc_V_centre_changed)
        self.mwpcVFwhmRefBox.valueChanged['int'].connect(MainWindow.mwpc_V_FWHM_changed)
        self.secRefBox.valueChanged['int'].connect(MainWindow.sec_ref_changed)
        self.mwpcHFwhmRefBox.valueChanged['int'].connect(MainWindow.mwpc_H_FWHM_changed)
        self.downTimeBox.valueChanged['int'].connect(MainWindow.downtime_changed)
        self.mwpcHCentreRefBox.valueChanged['int'].connect(MainWindow.mwpc_H_centre_changed)
        self.pushButton.clicked.connect(self.mwpcHCentreRefBox.update)
        self.pushButton.clicked.connect(self.mwpcHFwhmRefBox.update)
        for line in self.emailEdits:
          line.editingFinished.connect(self.user_email_changed)
        for line in self.phoneEdits:
          line.editingFinished.connect(self.user_phone_changed)
        for box in self.alert_checkboxes:
          box.clicked['bool'].connect(self.alert_checked)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def alert_checked(self, state):
      sender = self.sender()
      try:
        idx = int(sender.objectName().split('_')[-1])
      except ValuError:
        print('Error! not a string')
        idx = 0
        return
      name = self.usernames[idx].text()
      #email = self.emailEdits[idx].text()
      #phone = self.phoneEdits[idx].text()
      alert = state*1 # convert True, False to 1, 0
      db_cmd = db_commands()
      db_cmd.set_alert((name,alert))

    def user_phone_changed(self):
      sender = self.sender()
      # Since the QLineEdits and user labels are labled 1,2,3...n
      # We can use the senders name to find the user name stored in the user label
      # This is very hacky, but I have spent too long trying to find
      # the correct way to do it...
      # Using split(_) because the name and number is devided by _ as in user_label_10
      try:
        idx = int(sender.objectName().split('_')[-1])-1
      except ValuError:
        print('Error! not a string')
        idx = 0
        return
      name = self.usernames[idx].text()
      phone = sender.text()
      db_cmd = db_commands()
      db_cmd.set_shifter_phone((name,phone))
    
    def user_email_changed(self):
      sender = self.sender()
      # Since the QLineEdits and user labels are labled 0,1,2...n
      # We can use the senders name to find the user name stored in the user label
      # This is very hacky, but I have spent too long trying to find
      # the correct way to do it...
      # Using split(_) because the name and number is devided by _ as in user_label_10
      try:
        idx = int(sender.objectName().split('_')[-1])
      except ValuError:
        print('Error! not a string')
        idx = 0
        return
      name = self.usernames[idx].text()
      email = sender.text()
      db_cmd = db_commands()
      db_cmd.set_shifter_email((name,email))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Deviation before users are alerted [%]"))
        self.label_3.setText(_translate("MainWindow", "SEC reference [e10]"))
        self.label_4.setText(_translate("MainWindow", "MWPC vertical FWHM refrence"))
        self.label_5.setText(_translate("MainWindow", "MWPC vertical Centre reference [e-1 mm]"))
        self.label_6.setText(_translate("MainWindow", "MWPC horizontal FWHM reference"))
        self.label.setText(_translate("MainWindow", "Down time before users are alerted [min]"))
        self.label_7.setText(_translate("MainWindow", "MWPC horizontal Centre  reference [e-1 mm]"))
        self.pushButton.setText(_translate("MainWindow", "Load Defaults"))
        self.label_8.setText(_translate("MainWindow", "User Name"))
        self.label_10.setText(_translate("MainWindow", "Phone number"))
        self.label_9.setText(_translate("MainWindow", "Email"))
        self.label_13.setText(_translate("MainWindow", "Alert"))

        shifters = get_all_shifters()
        shifters = sorted(shifters, key=str.lower)
        num_shifters = len(shifters)
        n = 0
        e = 1
        p = 2
        for name in shifters:
          shifter_info = self.db_cmd.get_shifter_info(name)
          if len(shifter_info) == 0:
            email = ""
            phone = ""
          else:
            email = shifter_info['email']
            phone = str(shifter_info['phone'])
          self.all_user_boxes[n].setText(_translate("MainWindow", name))
          self.all_user_boxes[e].setText(_translate("MainWindow", email))
          self.all_user_boxes[p].setText(_translate("MainWindow", phone))
          n += 4
          e += 4
          p += 4



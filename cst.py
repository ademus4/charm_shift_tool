# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cst.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from database_ctrl import db_commands

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
        MainWindow.resize(894, 757)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.downTimeBox = QtWidgets.QSpinBox(self.centralwidget)
        self.downTimeBox.setGeometry(QtCore.QRect(320, 10, 181, 31))
        self.downTimeBox.setMaximum(120)
        self.downTimeBox.setObjectName("downTimeBox")
        self.deviationBox = QtWidgets.QSpinBox(self.centralwidget)
        self.deviationBox.setGeometry(QtCore.QRect(320, 60, 181, 31))
        self.deviationBox.setMaximum(999)
        self.deviationBox.setObjectName("deviationBox")
        self.secRefBox = QtWidgets.QSpinBox(self.centralwidget)
        self.secRefBox.setGeometry(QtCore.QRect(320, 110, 181, 31))
        self.secRefBox.setMaximum(999)
        self.secRefBox.setObjectName("secRefBox")
        self.mwpcVFwhmRefBox = QtWidgets.QSpinBox(self.centralwidget)
        self.mwpcVFwhmRefBox.setGeometry(QtCore.QRect(320, 160, 181, 31))
        self.mwpcVFwhmRefBox.setMaximum(999)
        self.mwpcVFwhmRefBox.setObjectName("mwpcVFwhmRefBox")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 15, 301, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 301, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 301, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 160, 281, 31))
        self.label_4.setObjectName("label_4")
        self.mwpcVCentreRefBox = QtWidgets.QSpinBox(self.centralwidget)
        self.mwpcVCentreRefBox.setGeometry(QtCore.QRect(320, 210, 181, 31))
        self.mwpcVCentreRefBox.setMaximum(999)
        self.mwpcVCentreRefBox.setObjectName("mwpcVCentreRefBox")
        self.mwpcHFwhmRefBox = QtWidgets.QSpinBox(self.centralwidget)
        self.mwpcHFwhmRefBox.setGeometry(QtCore.QRect(320, 260, 181, 31))
        self.mwpcHFwhmRefBox.setMaximum(999)
        self.mwpcHFwhmRefBox.setObjectName("mwpcHFwhmRefBox")
        self.mwpcHCentreRefBox = QtWidgets.QSpinBox(self.centralwidget)
        self.mwpcHCentreRefBox.setGeometry(QtCore.QRect(320, 310, 181, 31))
        self.mwpcHCentreRefBox.setMaximum(999)
        self.mwpcHCentreRefBox.setObjectName("mwpcHCentreRefBox")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 210, 291, 21))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 260, 281, 31))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(10, 310, 281, 31))
        self.label_7.setObjectName("label_7")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(523, 10, 361, 701))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy)
        self.plainTextEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 350, 101, 31))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 894, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.downTimeBox.valueChanged['int'].connect(MainWindow.downtime_changed)
        self.secRefBox.valueChanged['int'].connect(MainWindow.sec_ref_changed)
        self.mwpcVFwhmRefBox.valueChanged['int'].connect(MainWindow.mwpc_V_FWHM_changed)
        self.mwpcVCentreRefBox.valueChanged['int'].connect(MainWindow.mwpc_V_centre_changed)
        self.mwpcHFwhmRefBox.valueChanged['int'].connect(MainWindow.mwpc_H_FWHM_changed)
        self.mwpcHCentreRefBox.valueChanged['int'].connect(MainWindow.mwpc_H_centre_changed)
        self.deviationBox.valueChanged['int'].connect(MainWindow.deviation_changed)
        self.pushButton.clicked.connect(MainWindow.load_defaults)
        self.pushButton.clicked.connect(self.mwpcHCentreRefBox.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Down time before users are alerted [min]"))
        self.label_2.setText(_translate("MainWindow", "Deviation before users are alerted [%]"))
        self.label_3.setText(_translate("MainWindow", "SEC reference [e10]"))
        self.label_4.setText(_translate("MainWindow", "MWPC vertical FWHM refrence"))
        self.label_5.setText(_translate("MainWindow", "MWPC vertical Centre reference [e-1 mm]"))
        self.label_6.setText(_translate("MainWindow", "MWPC horizontal FWHM reference"))
        self.label_7.setText(_translate("MainWindow", "MWPC horizontal Centre  reference [e-1 mm]"))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus. Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec consectetur ante hendrerit. Donec et mollis dolor. Praesent et diam eget libero egestas mattis sit amet vitae augue. Nam tincidunt congue enim, ut porta lorem lacinia consectetur. Donec ut libero sed arcu vehicula ultricies a non tortor. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean ut gravida lorem. Ut turpis felis, pulvinar a semper sed, adipiscing id dolor. Pellentesque auctor nisi id magna consequat sagittis. Curabitur dapibus enim sit amet elit pharetra tincidunt feugiat nisl imperdiet. Ut convallis libero in urna ultrices accumsan. Donec sed odio eros. Donec viverra mi quis quam pulvinar at malesuada arcu rhoncus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. In rutrum accumsan ultricies. Mauris vitae nisi at sem facilisis semper ac in est.\n"
"\n"
"Vivamus fermentum semper porta. Nunc diam velit, adipiscing ut tristique vitae, sagittis vel odio. Maecenas convallis ullamcorper ultricies. Curabitur ornare, ligula semper consectetur sagittis, nisi diam iaculis velit, id fringilla sem nunc vel mi. Nam dictum, odio nec pretium volutpat, arcu ante placerat erat, non tristique elit urna et turpis. Quisque mi metus, ornare sit amet fermentum et, tincidunt et orci. Fusce eget orci a orci congue vestibulum. Ut dolor diam, elementum et vestibulum eu, porttitor vel elit. Curabitur venenatis pulvinar tellus gravida ornare. Sed et erat faucibus nunc euismod ultricies ut id justo. Nullam cursus suscipit nisi, et ultrices justo sodales nec. Fusce venenatis facilisis lectus ac semper. Aliquam at massa ipsum. Quisque bibendum purus convallis nulla ultrices ultricies. Nullam aliquam, mi eu aliquam tincidunt, purus velit laoreet tortor, viverra pretium nisi quam vitae mi. Fusce vel volutpat elit. Nam sagittis nisi dui.\n"
"\n"
"Suspendisse lectus leo, consectetur in tempor sit amet, placerat quis neque. Etiam luctus porttitor lorem, sed suscipit est rutrum non. Curabitur lobortis nisl a enim congue semper. Aenean commodo ultrices imperdiet. Vestibulum ut justo vel sapien venenatis tincidunt. Phasellus eget dolor sit amet ipsum dapibus condimentum vitae quis lectus. Aliquam ut massa in turpis dapibus convallis. Praesent elit lacus, vestibulum at malesuada et, ornare et est. Ut augue nunc, sodales ut euismod non, adipiscing vitae orci. Mauris ut placerat justo. Mauris in ultricies enim. Quisque nec est eleifend nulla ultrices egestas quis ut quam. Donec sollicitudin lectus a mauris pulvinar id aliquam urna cursus. Cras quis ligula sem, vel elementum mi. Phasellus non ullamcorper urna.\n"
"\n"
"Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. In euismod ultrices facilisis. Vestibulum porta sapien adipiscing augue congue id pretium lectus molestie. Proin quis dictum nisl. Morbi id quam sapien, sed vestibulum sem. Duis elementum rutrum mauris sed convallis. Proin vestibulum magna mi. Aenean tristique hendrerit magna, ac facilisis nulla hendrerit ut. Sed non tortor sodales quam auctor elementum. Donec hendrerit nunc eget elit pharetra pulvinar. Suspendisse id tempus tortor. Aenean luctus, elit commodo laoreet commodo, justo nisi consequat massa, sed vulputate quam urna quis eros. Donec vel. "))
        self.pushButton.setText(_translate("MainWindow", "Load Defaults"))


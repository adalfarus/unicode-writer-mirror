# made by memoryview
from PyQt5 import QtCore, QtGui, QtWidgets

class UI_SettingsWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 250)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)  # Define grid layout

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1)  # Added to layout

        self.fontComboBox = QtWidgets.QFontComboBox(self.centralwidget)
        self.fontComboBox.setObjectName("fontComboBox")
        self.gridLayout.addWidget(self.fontComboBox, 0, 2)  # Added to layout

        self.commandLinkButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.gridLayout.addWidget(self.commandLinkButton, 5, 0)  # Moved one down

        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 3, 0)  # Added to layout

        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 4, 0)  # Added to layout

        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setEnabled(False)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout.addWidget(self.toolButton, 4, 3)  # Moved one to the right

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 3, 2)  # Added to layout

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 1)  # Added to layout

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 4, 2)  # Moved one to the right

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton_2, 6, 0)  # Added to layout

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton_3, 6, 1)  # Added to layout

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 6, 2)  # Added to layout

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 351, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Change Font"))
        self.commandLinkButton.setText(_translate("MainWindow", "Check for Updates"))
        self.checkBox.setText(_translate("MainWindow", "Auto Start"))
        self.checkBox_2.setText(_translate("MainWindow", "Auto Restart"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.comboBox.setItemText(0, _translate("MainWindow", "Icon"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Icon2"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Icon3"))
        self.comboBox.setItemText(3, _translate("MainWindow", "Icon4"))
        self.comboBox.setItemText(4, _translate("MainWindow", "Icon5"))
        self.comboBox.setItemText(5, _translate("MainWindow", "Icon6"))
        self.comboBox.setItemText(6, _translate("MainWindow", "Custom"))
        self.label_2.setText(_translate("MainWindow", "Icon File"))
        self.pushButton_2.setText(_translate("MainWindow", "Save Settings"))
        self.pushButton_3.setText(_translate("MainWindow", "Revert Settings"))
        self.pushButton.setText(_translate("MainWindow", "Uninstall"))

# made by memoryview
from PySide6 import QtWidgets, QtGui, QtCore
from dancer import config


class UI_AboutWindow(QtWidgets.QDialog):
    def __init__(self, parent):
        super(UI_AboutWindow, self).__init__(parent)
        self.setModal(True)
        self.result = None
        self.setWindowTitle('About')
        self.setWindowIcon(QtGui.QIcon('media/icon.png'))

        logo_label = QtWidgets.QLabel(self)
        logo_label.setPixmap(QtGui.QPixmap('media/rc.png'))
        logo_label.setAlignment(QtCore.Qt.AlignCenter)
        logo_label.setScaledContents(True)
        logo_label.setFixedSize(200, 250)#268)

        app_name = config.PROGRAM_NAME
        version = config.get_version_str()
        self.app_label = QtWidgets.QLabel(self)
        self.app_label.setText(f"{app_name} {version}")
        self.app_label.setAlignment(QtCore.Qt.AlignCenter)
        self.app_label.setStyleSheet("padding-left: 4px; padding-right: 4px; color: #358cf8; text-decoration: underline;")
        self.app_label.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.app_label.mousePressEvent = self.call_link

        copy_label = QtWidgets.QLabel(self)
        copy_label.setText("Copyright (C) 2025 Cariel Becker")
        copy_label.setAlignment(QtCore.Qt.AlignCenter)

        rights_label = QtWidgets.QLabel(self)
        rights_label.setText("All rights reserved")
        rights_label.setAlignment(QtCore.Qt.AlignCenter)

        # mech_label = QtWidgets.QLabel(self)
        # mech_label.setText("GitHub Repository")
        # mech_label.setAlignment(QtCore.Qt.AlignCenter)
        # #mech_label.setFont(QtGui.QFont('Arial', 10, QtGui.QFont.bold | QtGui.QFont.underline))
        # mech_label.setStyleSheet("color: blue")
        # mech_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # mech_label.mousePressEvent = self.call_link

        ok_button = QtWidgets.QPushButton('OK', self)
        ok_button.clicked.connect(self.accept)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(logo_label)
        layout.addWidget(self.app_label)
        layout.addWidget(copy_label)
        layout.addWidget(rights_label)
        # layout.addWidget(mech_label)
        layout.addWidget(ok_button)
        self.setLayout(layout)

    def call_link(self, event):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/adalfarus/unicode-writer"))
        self.app_label.setStyleSheet("color: #464cb1; text-decoration: underline;")

# Example usage
if not 1 == 1:
    app = QtWidgets.QApplication([])
    window = UI_AboutWindow(None)
    window.show()
    app.exec_()

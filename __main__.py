from UnicodeWriterSettingsWindow import UI_SettingsWindow
from UnicodeWriterAboutWindow import UI_AboutWindow
from PyQt5.QtWidgets import QMessageBox, QPushButton, QApplication, QSystemTrayIcon, QMenu, QAction, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import requests
import logging
import sqlite3
import sys
import os

__author__ = 'Cariel Becker'
__copyright__ = 'Copyright (C) 2023, Cariel Becker'
__credits__ = ['Cariel Becker']
__license__ = 'The MIT License (MIT)'
__version__ = '0.0.0'
__maintainer__ = 'Cariel Becker'
__email__ = 'naido@streber24.de'
__status__ = 'Beta'

_AppName_ = 'Unicode Writer'

class DataBase():
    def __init__(self, database_location: str):
        # Check if the settings database exists
        if not os.path.exists(database_location):
            # Open a DB conn
            self.open_conn(database_location)
            # If it doesn't exist, initialize it with default settings
            self.initialize_settings(1, 'Default', 0, 0, 'Icon', '')
        else:
            self.open_conn(database_location)
        
    def initialize_settings(self, db_id, font, auto_start, auto_restart, icon, custom_icon_file):
        # Create settings table
        self.c.execute("""CREATE TABLE Settings (
                    id INTEGER PRIMARY KEY,
                    font TEXT,
                    auto_start INTEGER,
                    auto_restart INTEGER,
                    icon TEXT,
                    custom_icon_file TEXT)""")

        # Initialize settings with default values
        self.c.execute("INSERT INTO Settings VALUES (?, ?, ?, ?, ?, ?)",
                  (db_id, font, auto_start, auto_restart, icon, custom_icon_file))

        self.conn.commit()
        
    def save_settings(self, db_id, font, auto_start, auto_restart, icon, custom_icon_file):
        # Create table if it doesn't exist
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS Settings (
                id INTEGER PRIMARY KEY,
                font TEXT,
                auto_start INTEGER,
                auto_restart INTEGER,
                icon TEXT,
                custom_icon_file TEXT
            )
        ''')

        # Save settings
        self.c.execute('''
            INSERT OR REPLACE INTO Settings
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (db_id, font, auto_start, auto_restart, icon, custom_icon_file))

        self.conn.commit()
        
    def load_settings(self):
        # Fetch settings
        self.c.execute("SELECT * FROM Settings WHERE id = 1")
        row = self.c.fetchone()
        if row is not None:
            _, font, auto_start, auto_restart, icon, custom_icon_file = row
            return _, font, auto_start, auto_restart, icon, custom_icon_file
            
    def open_conn(self, database_location):
        self.conn = sqlite3.connect(database_location)
        self.c = self.conn.cursor()
            
    def close_conn(self):
        self.conn.close()

class QMessageBoxCustom(QMessageBox):
    def __init__(self, title, message, button_labels):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(message)
        self.setStandardButtons(QMessageBox.NoButton)

        for label in button_labels:
            button = QPushButton(label)
            self.addButton(button, QMessageBox.AcceptRole)

        self.buttonClicked.connect(self.on_button_click)
        self.button_click_result = None

    def on_button_click(self, button):
        self.button_click_result = button.text()
        self.close()

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = UI_SettingsWindow()
        self.ui.setupUi(self)
        
        # Connect signals to slots
        self.ui.fontComboBox.currentFontChanged.connect(self.change_font)
        self.ui.commandLinkButton.clicked.connect(self.check_for_updates)
        self.ui.checkBox.stateChanged.connect(self.toggle_auto_start)
        self.ui.checkBox_2.stateChanged.connect(self.toggle_auto_restart)
        self.ui.comboBox.currentTextChanged.connect(self.select_icon)
        self.ui.toolButton.clicked.connect(self.select_icon_file)
        self.ui.pushButton.clicked.connect(self.uninstall)

    def change_font(self, font):
        # Change the font of all text
        self.setFont(font)

    def check_for_updates(self):
        # Check for updates
        response = requests.get("https://api.github.com/repos/adalfarus/unicode-writer/releases/latest")
        print(response.json()["name"].split("v"))
        repo_version = ''.join([x if sum(c.isnumeric() for c in x) >= 3 else "" for x in response.json()["name"].split("v")])
        if int(repo_version.replace(".", "")) > int(__version__.replace(".", "")):
            messagebox = QMessageBoxCustom("Info", "New Version available.\nDo you want to update?", ["Yes", "No"])
            messagebox.exec_()
            if messagebox.button_click_result == "Yes":
                location = "./update/"
                version = repo_version
                ui_toggle = 0
                cmd_toggle = 0
                if not cmd_toggle:
                    subprocess.run(["python", "scripts/update.py", str(location), str(version), str(ui_toggle)])
                else:
                    subprocess.run(["pythonw", "scripts/update.py", str(location), str(version), str(ui_toggle)])
            elif messagebox.button_click_result == "No":
                pass
        else:
            messagebox = QMessageBoxCustom("Info", "No new version available.", ["Okay"])
            messagebox.exec_()

    def toggle_auto_start(self, state):
        # Toggle auto start
        if state == Qt.Checked:
            # Enable auto start
            pass  # You need to implement this
        else:
            # Disable auto start
            pass  # You need to implement this

    def toggle_auto_restart(self, state):
        # Toggle auto restart
        if state == Qt.Checked:
            # Enable auto restart
            pass  # You need to implement this
        else:
            # Disable auto restart
            pass  # You need to implement this

    def select_icon(self, text):
        # Select icon
        if text == "Custom":
            self.ui.lineEdit.setEnabled(True)
            self.ui.toolButton.setEnabled(True)
        else:
            self.ui.lineEdit.setEnabled(False)
            self.ui.toolButton.setEnabled(False)
            # Set icon
            pass  # You need to implement this

    def select_icon_file(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Select Icon File', '', 'Icon Files (*.ico *.png *.jpg *.jpeg *.bmp)')
        if file:
            self.ui.lineEdit.setText(file)
            # Set icon
            pass  # You need to implement this

    def uninstall(self):
        # Uninstall
        pass  # You need to implement this
        
    def closeEvent(self, event):
        # Perform actions when the user closes the window
        # Add your code here

        # Example: Display a message box and ask for confirmation
        reply = QMessageBox.question(
            self, "Confirmation",
            "Are you sure you want to close the window?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # User confirmed, proceed with closing the window
            event.accept()
        else:
            # User cancelled, ignore the close event
            event.ignore()

def main(var, database_file):
    def open_settings():
        global settings_window
        settings_window = SettingsWindow()
        settings_window.show()
        #settings_window.setScaledContents(True)
        
        # Set the UI elements to the loaded settings
        index = settings_window.ui.fontComboBox.findText(font)
        if index != -1:
            settings_window.ui.fontComboBox.setCurrentIndex(index)

        settings_window.ui.checkBox.setChecked(bool(auto_start))
        settings_window.ui.checkBox_2.setChecked(bool(auto_restart))

        index = settings_window.ui.comboBox.findText(icon)
        if index != -1:
            settings_window.ui.comboBox.setCurrentIndex(index)

        settings_window.ui.lineEdit.setText(custom_icon_file)

    def open_about_window():
        global about_window
        about_window = UI_AboutWindow(None)
        about_window.show()

    # Create db object and initialize
    db = DataBase('settings.db')
    # Load the settings from the database
    db_id, font, auto_start, auto_restart, icon, custom_icon_file = db.load_settings()

    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)  # Keep the application running even when all windows are closed

    # Create a system tray icon
    tray = QSystemTrayIcon()
    tray.setIcon(QIcon("media/icon.png"))  # Set your icon file
    tray.setVisible(True)
    tray.setIcon(QIcon("media/icon2.png"))  # Set your icon file

    # Create a menu for the tray
    menu = QMenu()

    # Create an action for the menu
    settings_action = QAction("Settings")
    settings_action.triggered.connect(open_settings)
    menu.addAction(settings_action)

    # Quit action
    quit_action = QAction("Quit")
    quit_action.triggered.connect(app.quit)
    quit_action.triggered.connect(db.close_conn)
    menu.addAction(quit_action)
    
    # About action
    about_action = QAction("About")
    about_action.triggered.connect(open_about_window)
    menu.addAction(about_action)

    # Add the menu to the tray
    tray.setContextMenu(menu)

    app.exec_()
    
def handle_exception(database_file):
    def check_database(database_file, complex_output=False):
        if os.path.exists(database_file):
            try:
                conn = sqlite3.connect(database_file)
                cursor = conn.cursor()
                cursor.execute("PRAGMA integrity_check")
                result = cursor.fetchone()
                conn.close()

                if complex_output:
                    if result[0] == "ok":
                        print("Database", database_file, "exists and is not corrupted.")
                    else:
                        print("Database", database_file, "exists but is corrupted.")
                else:
                    if result[0] == "ok":
                        print("Database", database_file, "is not corrupted.")
                    else:
                        print("Database", database_file, "is corrupted.")
            except sqlite3.Error as e:
                print("SQLite3 Error:", e)
        else:
            if complex_output:
                print("Database", database_file, "does not exist.")
            else:
                return False

        return ""
    if check_database(database_file) == False:
        os.remove(database_file)
    if 1 != 1:
        start_application()
    else:
        main('ff', database_file)
    
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)
    
def start_application():
    try:
        if len(sys.argv) >= 2:
            name = int(sys.argv[0]) # Super script name
            var = int(sys.argv[1]) # Variable
        else:
            print("Not enough arguments provided. Please input them manually.")
            var = input("Variable: ")
        main(var, 'settings.db')
    except Exception as e:
        logging.exception(f"An error accured: {e}")
        handle_exception('settings.db')

start_application()

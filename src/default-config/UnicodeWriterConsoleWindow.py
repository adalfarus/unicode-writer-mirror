from PySide6.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout
from PySide6.QtGui import QTextCursor, QFont, QIcon

class UI_ConsoleWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Console Output")
        # self.setWindowIcon(QIcon("media/icon.png"))
        self.resize(880, 505)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.console = QPlainTextEdit(self)
        self.console.setReadOnly(True)

        # Style like a terminal
        font = QFont("DejaVu Sans Mono", 10)
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setWeight(QFont.Weight.Bold)
        self.console.setFont(font)
        self.console.setStyleSheet("""
            QPlainTextEdit {
                background-color: #111;
                color: #a3a3a3;
                border: none;
                padding: 8px;
            }
        """)

        layout.addWidget(self.console)

    def write(self, message: str):
        self.console.moveCursor(QTextCursor.MoveOperation.End)
        self.console.insertPlainText(message)
        self.console.moveCursor(QTextCursor.MoveOperation.End)
        self.console.ensureCursorVisible()

    def flush(self): pass

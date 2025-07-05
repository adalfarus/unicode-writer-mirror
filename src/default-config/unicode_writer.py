"""Unicode writer"""
from dancer import config
from dancer.qt import BasicAppGUIQt

from argparse import Namespace
import threading
import logging
import base64
import json
import re
import os

# Third party
from pynput.keyboard import Key, Controller, Listener, KeyCode
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction, QCursor
from PySide6.QtCore import QTimer

# Local imports
from UnicodeWriterAboutWindow import UI_AboutWindow
from UnicodeWriterConsoleWindow import UI_ConsoleWindow

import typing as _ty


KEY_NAME_MAP: dict[str, KeyCode] = {
    "Alt": Key.alt,
    "AltGr": Key.alt_gr,
    "Ctrl": Key.ctrl,
    "CtrlL": Key.ctrl_l,
    "CtrlR": Key.ctrl_r,
    "Shift": Key.shift,
    "ShiftL": Key.shift_l,
    "ShiftR": Key.shift_r,
    "CapsLock": Key.caps_lock,
    "ScrollLock": Key.scroll_lock,
    "Insert": Key.insert,
    "Pause": Key.pause,
    "Menu": Key.menu,
    "Esc": Key.esc,
    "Enter": Key.enter,
    "Tab": Key.tab,
    "Backspace": Key.backspace,
    "Space": Key.space,
    "Delete": Key.delete,
    "Home": Key.home,
    "End": Key.end,
    "PageUp": Key.page_up,
    "PageDown": Key.page_down,
    "Up": Key.up,
    "Down": Key.down,
    "Left": Key.left,
    "Right": Key.right,
    "NumLock": Key.num_lock,
    "F1": Key.f1,
    "F2": Key.f2,
    "F3": Key.f3,
    "F4": Key.f4,
    "F5": Key.f5,
    "F6": Key.f6,
    "F7": Key.f7,
    "F8": Key.f8,
    "F9": Key.f9,
    "F10": Key.f10,
    "F11": Key.f11,
    "F12": Key.f12
}


def parse_key_combo(combo_str: str) -> set[Key | KeyCode]:
    """
    Parses a key combo string like "Alt+Ctrl+K" into a set of Key/KeyCode objects.

    Returns a set of Key or KeyCode instances. Invalid entries are ignored.
    """
    combo: set[Key | KeyCode] = set()
    parts = re.split(r"\s*\+\s*", combo_str.strip())

    for part in parts:
        key_name = part.strip()

        if key_name in KEY_NAME_MAP:
            combo.add(KEY_NAME_MAP[key_name])
        elif len(key_name) == 1:
            combo.add(KeyCode.from_char(key_name.lower()))
        else:
            print(f"⚠️ Unknown key: '{part}' — skipped")
    return combo


class QtConsoleHandler(logging.Handler):
    def __init__(self, widget: UI_ConsoleWindow):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        self.widget.console.appendPlainText(msg)


class UnicodeWriterApp(BasicAppGUIQt):
    def __init__(self, args: Namespace, logging_mode: int) -> None:
        super().__init__(os.path.abspath("./logs"), args, logging_mode)
        self.qapp: QApplication
        self.about_window: UI_AboutWindow
        self.console_window: UI_ConsoleWindow
        self.tray: QSystemTrayIcon

        self.controller: Controller = Controller()
        self.config_path: str = os.path.abspath("./config/settings.json")
        self.config: dict[str, _ty.Any] = self.load_settings()
        self.config_lock: threading.Lock = threading.Lock()

        self.enabled: bool = self.config.get("enabled", True)
        self.icon_filename: str = self.config.get("icon", "")
        self.mode_str: str = self.ensure_mode(self.config.get("mode", "numpad"))

        self.shortcut_keys: set[KeyCode]
        self.modifier_key_combo: str = self.ensure_modifier_key_combo(self.config.get("modifier_key_combo", "AltGr"))

        self.icons: list[str] = self.scan_icons()
        self.icon_index: int = self.get_initial_icon_index()

        self.save_settings()  # So we ensure checked settings while running

        self.modes: dict[str, str] = {
            "numpad": "🔢 Numpad/Numbers Mode",
            "letter": "🔡 Letter Mode",
            "hex": "🔣 Hex Mode",
            "base64": "🔣 Base64 Mode"
        }

        self.current_keys: set[KeyCode] = set()
        self.number_string: str = ""
        self.concurrent_key_presses: int = 0
        self.max_concurrent_key_presses: int = 5

        self.listener_thread: threading.Thread | None = None
        self.listener_stop_event: threading.Event = threading.Event()
        if self.enabled:
            self.start_listener()

    def scan_icons(self) -> list[str]:
        """Scan all image files in the media folder"""
        media_dir: str = os.path.abspath("./media")
        return [
            f for f in os.listdir(media_dir)
            if f.lower().endswith((".png", ".ico", ".jpg", ".jpeg", ".bmp", ".webp")) and f.lower().startswith("icon")
        ]

    def get_initial_icon_index(self) -> int:
        """Gets the initial icon index if the configs icon name is in the detected icons, otherwise 0"""
        if self.icon_filename in self.icons:
            return self.icons.index(self.icon_filename)
        return 0

    def ensure_mode(self, mode_str: str) -> str:
        """Ensures the mode_str is correct"""
        if mode_str not in ("numpad", "letter", "hex", "base64"):
            return "numpad"
        return mode_str

    def ensure_modifier_key_combo(self, modifier_key_combo_str: str) -> str:
        """Ensures a valid modifier key combo"""
        try:
            self.shortcut_keys = parse_key_combo(modifier_key_combo_str)
        except Exception:
            self.shortcut_keys = {Key.alt_gr}
            return "AltGr"
        reverse_map = {v: k for k, v in KEY_NAME_MAP.items()}
        return "+".join(reverse_map[key] for key in self.shortcut_keys if key in reverse_map)

    def load_settings(self) -> dict[str, _ty.Any]:
        """Loads json from a set path and returns it as a dict"""
        if not os.path.exists(self.config_path):
            return {}
        with open(self.config_path, "r") as f:
            return json.load(f)

    def save_settings(self) -> None:
        """Saves set dict to a set path as json"""
        with self.config_lock:
            self.config["enabled"] = self.enabled
            self.config["mode"] = self.mode_str
            self.config["icon"] = self.icons[self.icon_index]
            self.config["modifier_key_combo"] = self.modifier_key_combo
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)
        return None

    def update_tray_menu(self) -> None:
        """Updates the text of the actions within self.tray with the current config data"""
        menu = self.tray.contextMenu()
        actions = menu.actions()

        # Skip title and separator (first two actions)
        toggle_action = actions[2]
        mode_action = actions[3]
        icon_action = actions[4]

        toggle_action.setText("🟢 Enabled" if self.enabled else "🔴 Disabled")
        toggle_action.triggered.disconnect()
        toggle_action.triggered.connect(self.toggle_enabled)

        mode_action.setText(self.modes[self.mode_str])
        mode_action.triggered.disconnect()
        mode_action.triggered.connect(self.cycle_mode)

        icon_label = f"🖼 Icon: {self.icons[self.icon_index]} ({self.icon_index + 1} of {len(self.icons)})"
        icon_action.setText(icon_label)
        icon_action.triggered.disconnect()
        icon_action.triggered.connect(self.cycle_icon)

        # Reopen menu at previous cursor position
        global_cursor_pos = QCursor.pos()
        menu_pos = menu.pos()
        relative_cursor_pos = global_cursor_pos - menu_pos
        new_menu_pos = global_cursor_pos - relative_cursor_pos

        QTimer.singleShot(0, lambda: menu.popup(new_menu_pos))
        return None

    def toggle_enabled(self) -> None:
        """Toggles the app on/off by using self.start_listener() and self.stop_listener() --> Maybe use flag / event thread safe instead?"""
        self.enabled = not self.enabled
        self.save_settings()
        self.update_tray_menu()
        if self.enabled:
            self.ensure_resumed_listener()
        else:
            self.ensure_stalled_listener()
        return None

    def cycle_mode(self) -> None:
        """Toggles hex/numbers mode"""
        mode_strs = list(self.modes.keys())
        mode_index = (mode_strs.index(self.mode_str) + 1) % len(mode_strs)
        self.mode_str = mode_strs[mode_index]

        if self.mode_str != "numpad" and self.shortcut_keys == {Key.alt_gr}:
            self.io_manager.warning(
                prompt_title="Modifier Key May Interfere with Input",
                log_message=(
                    f"The current modifier is set to `{self.modifier_key_combo}`, but the selected mode "
                    f" may not work reliably. The `AltGr` key can alter typed input, especially "  # `{self.mode_str}` removed this so do not show again works properly
                    "on non-US keyboard layouts.\n\n"
                    "💡 To improve compatibility, consider changing the modifier in your settings file:\n"
                    f"  {config.base_app_dir}/config/settings.json\n\n"
                    'Example:\n'
                    '    "modifier_key_combo": "CtrlR+Insert"\n\n'
                    "Accepted format: combinations like `Alt+Ctrl+K` (case-insensitive, `+`-delimited)."
                ),
                show_prompt=True
            )

        self.save_settings()
        self.update_tray_menu()

    def change_icon(self, icon_path: str) -> None:
        """Changes the icon on all windows and the tray icon"""
        new_icon: QIcon = QIcon(icon_path)
        self.tray.setIcon(new_icon)
        self.about_window.setWindowIcon(new_icon)
        self.console_window.setWindowIcon(new_icon)

    def cycle_icon(self) -> None:
        """Cycles icons with the icon index"""
        self.icon_index = (self.icon_index + 1) % len(self.icons)
        self.save_settings()
        self.change_icon(os.path.join("media", self.icons[self.icon_index]))
        self.update_tray_menu()

    def open_console(self) -> None:
        """Shows the console window"""
        self.console_window.show()

    def show_about(self) -> None:
        """Shows the about window"""
        self.about_window.show()

    def exec(self) -> int:
        self.qapp.setQuitOnLastWindowClosed(False)
        self.io_manager.info("Starting GUI ...")

        icon_path: str = os.path.join("media", self.icons[self.icon_index])

        self.console_window = UI_ConsoleWindow(None)
        self.handler = QtConsoleHandler(self.console_window)
        formatter = logging.Formatter(
            '[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.handler.setFormatter(formatter)
        self.io_manager.add_handler(self.handler)

        self.about_window = UI_AboutWindow(None)

        self.tray = QSystemTrayIcon()  # , self.qapp
        self.tray.setVisible(True)
        self.tray.setToolTip(config.PROGRAM_NAME)

        self.change_icon(icon_path)

        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                color: #000000; 
                background-color: #ffffff; 
                border-radius: 5px;
            }
            QMenu::item {
                padding: 2px 10px; 
                margin: 2px 2px; 
                font-weight: bold;
            }
            QMenu::item:selected {
                background-color: #f2f2f2;
            }
        """)
        title_action = QAction(f"🔧 {config.PROGRAM_NAME} Menu")
        title_action.setEnabled(False)  # Make it non-clickable
        menu.addAction(title_action)
        menu.addSeparator()

        toggle_action = QAction("🟢 Enabled" if self.enabled else "🔴 Disabled")
        toggle_action.triggered.connect(self.toggle_enabled)
        menu.addAction(toggle_action)

        mode_action = QAction(self.modes[self.mode_str])
        mode_action.triggered.connect(self.cycle_mode)
        menu.addAction(mode_action)

        icon_label = f"🖼 Icon: {self.icons[self.icon_index]} ({self.icon_index + 1} of {len(self.icons)})"
        icon_action = QAction(icon_label)
        icon_action.triggered.connect(self.cycle_icon)
        menu.addAction(icon_action)

        console_action = QAction("💻 Console")
        console_action.triggered.connect(self.open_console)
        menu.addAction(console_action)

        about_action = QAction("ℹ️ About")
        about_action.triggered.connect(self.show_about)
        menu.addAction(about_action)

        quit_action = QAction("❌ Quit")
        quit_action.triggered.connect(self.qapp.quit)
        menu.addAction(quit_action)

        for action in menu.actions():
            action.setIconVisibleInMenu(False)

        self.tray.setContextMenu(menu)
        self.parent = self.tray.parent()  # Better parent?
        self.io_manager.info("Entering application loop ...")
        return super().exec()

    def start_listener(self) -> None:
        """Starts the global keyboard input listener based on thread-safe config values and regex checks."""

        mode_patterns = {
            "hex": re.compile(r"[0-9a-f]", re.IGNORECASE),
            "letter": re.compile(r"[a-z]", re.IGNORECASE),
            "numpad": re.compile(r"[0-9]"),
            "base64": re.compile(r"[A-Za-z0-9+/]"),
        }

        def _get_mode_pattern() -> re.Pattern:
            with self.config_lock:
                mode = self.config["mode"]
            return mode_patterns[mode]

        def _on_press(key: Key | KeyCode) -> None:
            with self.config_lock:
                if not self.config["enabled"]:
                    return None
            if key in self.shortcut_keys:
                self.current_keys.add(key)
                return None

            if self.current_keys == self.shortcut_keys:
                char: str | None = None
                try:
                    if isinstance(key, Key):
                        self.concurrent_key_presses += 1
                        if self.concurrent_key_presses >= self.max_concurrent_key_presses:
                            self.io_manager.info(prompt_title="",
                                                 log_message="We didn't get KeyCodes in a while, maybe you have numlock enabled?",
                                                 show_prompt=True)
                            # self.concurrent_key_presses = 0
                        return None
                    elif isinstance(key, KeyCode) and key.char:
                        char = key.char
                    elif 96 <= getattr(key, "vk", -1) <= 105:
                        char = str(key.vk - 96)
                    self.concurrent_key_presses = 0
                except AttributeError:
                    pass  # Not a character key

                if char:
                    pattern = _get_mode_pattern()
                    if pattern.fullmatch(char):
                        self.number_string += char
            return None

        def _on_release(key: Key | KeyCode) -> None:
            if key in self.shortcut_keys:
                self.current_keys.discard(key)

                if not self.current_keys and self.number_string:
                    with self.config_lock:
                        mode = self.config["mode"]

                    output = None
                    try:
                        if mode == "base64":
                            decoded = base64.b64decode(self.number_string.encode("utf-8"))
                            output = decoded.decode("utf-8")
                        elif mode == "hex":
                            value = int(self.number_string, 16)
                            if 0 <= value <= 0x10FFFF:
                                output = chr(value)
                        elif mode == "letter":
                            value = int(self.number_string, 36)  # a-z + 0-9 as base36
                            if 0 <= value <= 0x10FFFF:
                                output = chr(value)
                        elif mode == "numpad":
                            value = int(self.number_string, 10)
                            if 0 <= value <= 0x10FFFF:
                                output = chr(value)
                    except Exception as e:
                        print(f"❌ Failed to convert input '{self.number_string}': {e}")

                    if output:
                        self.controller.type(output)

                    self.number_string = ""
            return None

        def _listen(stop_event: threading.Event) -> None:
            listener = Listener(on_press=_on_press, on_release=_on_release)
            listener.start()

            while not stop_event.is_set():
                stop_event.wait(0.1)  # Wait briefly to avoid tight loop

            listener.stop()
            listener.join()

        self.listener_thread = threading.Thread(target=_listen, args=(self.listener_stop_event,), daemon=True)
        self.listener_thread.start()

    def ensure_resumed_listener(self) -> None:
        """Ensures the configs enable flag is true"""
        with self.config_lock:
            self.config["enabled"] = True

    def ensure_stalled_listener(self) -> None:
        """Ensures the configs enable flag is false"""
        with self.config_lock:
            self.config["enabled"] = False
            self.current_keys.clear()
            self.number_string = ""

    def close(self) -> None:
        super().close()
        if hasattr(self, "listener_thread") and self.listener_thread is not None and self.listener_thread.is_alive():
            self.listener_stop_event.set()
            self.listener_thread.join()

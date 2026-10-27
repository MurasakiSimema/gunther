import sys
import os
import ctypes
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from gunther.pet_window import PetWindow
from gunther.utils import get_resource_path

def set_app_user_model_id():
    try:
        app_id = "gunther.desktop.companion.1.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception:
        pass

def main():
    set_app_user_model_id()

    app = QApplication(sys.argv)
    app.setApplicationName("Gunther Desktop Companion")
    app.setQuitOnLastWindowClosed(False)

    icon_path = get_resource_path(os.path.join("assets", "icon.png"))
    app_icon = QIcon(icon_path) if os.path.exists(icon_path) else QIcon()
    app.setWindowIcon(app_icon)

    pet = PetWindow()
    pet.show()

    # System Tray Icon
    if QSystemTrayIcon.isSystemTrayAvailable():
        tray_icon = QSystemTrayIcon(app_icon, app)
        tray_icon.setToolTip("Gunther il Criceto 🐹❤️")

        tray_menu = QMenu()
        tray_menu.setStyleSheet("""
            QMenu {
                background-color: #FFFDF8;
                border: 1px solid #D6C7B8;
                border-radius: 8px;
                padding: 6px;
                font-family: 'Segoe UI';
                font-size: 10pt;
                color: #382C24;
            }
            QMenu::item {
                padding: 6px 20px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #F8E2CD;
                color: #261B14;
            }
        """)

        bring_act = tray_menu.addAction("🐹 Riporta Gunther qui")
        bring_act.triggered.connect(pet.move_to_initial_floor)

        feed_act = tray_menu.addAction("🌻 Dai un semino")
        feed_act.triggered.connect(pet.feed_hamster)

        thought_act = tray_menu.addAction("💭 Cosa stai pensando?")
        thought_act.triggered.connect(pet.trigger_random_thought)

        tray_menu.addSeparator()

        quit_act = tray_menu.addAction("👋 Saluta Gunther ed esci")
        quit_act.triggered.connect(app.quit)

        tray_icon.setContextMenu(tray_menu)
        tray_icon.activated.connect(lambda reason: pet.move_to_initial_floor() if reason == QSystemTrayIcon.ActivationReason.DoubleClick else None)
        tray_icon.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

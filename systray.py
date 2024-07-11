import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PyQt6.QtGui import QIcon, QAction

def show_message():
    tray_icon.showMessage(
        "Hello",
        "This is a message from the system tray icon",
        QSystemTrayIcon.MessageIcon.Information,
        2000
    )

def exit_app():
    QApplication.quit()

app = QApplication(sys.argv)

# Create the system tray icon
tray_icon = QSystemTrayIcon(QIcon("icon.png"), parent=app)
tray_icon.setToolTip("System Tray Icon Example")

# Create the context menu
menu = QMenu()

show_message_action = QAction("Show Message")
show_message_action.triggered.connect(show_message)
menu.addAction(show_message_action)

exit_action = QAction("Exit")
exit_action.triggered.connect(exit_app)
menu.addAction(exit_action)

tray_icon.setContextMenu(menu)

# Show the tray icon
tray_icon.show()

# Ensure the application keeps running
sys.exit(app.exec())
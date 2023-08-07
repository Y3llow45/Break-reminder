from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QSystemTrayIcon, QMenu, QAction, QHBoxLayout, QCheckBox, QSpinBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys
import time
import datetime
from win10toast import ToastNotifier

class BreakNotifierApp(QWidget):
    def __init__(self):
        super().__init__()

        self.break_intervals = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
        self.break_durations = [5, 10, 15, 20, 25, 30]

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Break Notifier")
        self.setGeometry(100, 100, 300, 200)  # Increased height to accommodate the new checkbox

        layout = QVBoxLayout()

        interval_label = QLabel("Select Break Interval:")
        self.custom_interval_checkbox = QCheckBox("Custom")
        self.custom_interval_checkbox.stateChanged.connect(self.toggle_custom_inputs)
        
        self.interval_input = QComboBox()
        self.interval_input.addItems([str(interval) + " mins" for interval in self.break_intervals])

        duration_label = QLabel("Select Break Duration:")
        self.duration_input = QComboBox()
        self.duration_input.addItems([str(duration) + " mins" for duration in self.break_durations])

        self.custom_interval_input = QSpinBox()
        self.custom_interval_input.setRange(1, 500)
        self.custom_interval_input.hide()  # Initially hidden

        self.custom_duration_input = QSpinBox()
        self.custom_duration_input.setRange(1, 500)
        self.custom_duration_input.hide()  # Initially hidden

        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start_notifications)

        layout.addWidget(self.custom_interval_checkbox)
        layout.addWidget(interval_label)
        layout.addWidget(self.interval_input)
        layout.addWidget(self.custom_interval_input)

        layout.addSpacing(10)  # Add spacing between interval and duration inputs

        layout.addWidget(duration_label)
        layout.addWidget(self.duration_input)
        layout.addWidget(self.custom_duration_input)
        
        layout.addSpacing(20)  # Add spacing between duration input and Start button

        layout.addWidget(start_button)

        self.setLayout(layout)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("path_to_your_icon"))  # Set your own icon file path
        show_action = QAction("Open", self)
        quit_action = QAction("Quit", self)
        show_action.triggered.connect(self.restore_from_tray)
        quit_action.triggered.connect(self.quit_application)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)

    def toggle_custom_inputs(self, state):
        if state == Qt.Checked:
            self.interval_input.hide()
            self.duration_input.hide()
            #self.custom_interval_checkbox.setText("Standard")
            self.custom_interval_input.show()
            self.custom_duration_input.show()
            #self.custom_break_input.show()
        else:
            self.custom_duration_input.hide()
            self.custom_interval_input.hide()
            self.interval_input.show()
            self.duration_input.show()
            #self.custom_interval_checkbox.setText("Custom")
            

    def start_notifications(self):
        interval = int(self.interval_combo.currentText().split()[0])
        duration = int(self.duration_combo.currentText().split()[0])

        self.hide()

        current_time = datetime.datetime.now()
        next_notification_time = current_time + datetime.timedelta(minutes=interval)

        while True:
            time.sleep((next_notification_time - current_time).total_seconds())
            self.show_notification()
            
            current_time = datetime.datetime.now()
            next_notification_time = current_time + datetime.timedelta(minutes=interval)
            
            time.sleep((duration - 4) * 60)  # Sleep for break duration minus notification duration

    def show_notification(self):
        toast = ToastNotifier()
        toast.show_toast("TAKE A BREAK", "5 min break", duration=4)

    def restore_from_tray(self):
        self.showNormal()

    def quit_application(self):
        self.tray_icon.hide()
        QApplication.quit()

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.restore_from_tray()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = BreakNotifierApp()
    main_window.show()
    sys.exit(app.exec_())

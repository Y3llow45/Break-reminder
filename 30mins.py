from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QSystemTrayIcon, QMenu, QAction, QCheckBox, QSpinBox
from PyQt5.QtCore import Qt
import sys
import time
from win10toast import ToastNotifier

class BreakNotifierApp(QWidget):
    def __init__(self):
        super().__init__()

        self.break_intervals = [20, 25, 30, 35, 40, 45]
        self.break_durations = [5, 10, 15, 20, 25, 30]

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Break Notifier")
        self.setGeometry(100, 100, 400, 300)

        self.setStyleSheet("background-color: #222; color: white;")

        layout = QVBoxLayout()

        interval_label = QLabel("Select Break Interval")
        interval_label.setStyleSheet("font-family: 'Franklin Gothic'; font-size: 16px; font-weight: bold;")
        self.custom_interval_checkbox = QCheckBox("Custom")
        self.custom_interval_checkbox.setStyleSheet("font-family: 'Franklin Gothic'; font-size: 14px;")
        self.custom_interval_checkbox.stateChanged.connect(self.toggle_custom_inputs)
        
        self.interval_input = QComboBox()
        self.interval_input.addItems([str(interval) + " mins" for interval in self.break_intervals])
        self.interval_input.setStyleSheet("font-family: 'Franklin Gothic'; font-size: 16px;")

        duration_label = QLabel("Select Break Duration")
        duration_label.setStyleSheet("font-family: 'Franklin Gothic'; font-size: 16px; font-weight: bold;")

        self.duration_input = QComboBox()
        self.duration_input.addItems([str(duration) + " mins" for duration in self.break_durations])
        self.duration_input.setStyleSheet("font-family: 'Franklin Gothic'; font-size: 16px;")

        self.custom_interval_input = QSpinBox()
        self.custom_interval_input.setRange(1, 500)
        self.custom_interval_input.setStyleSheet("font-family: 'Franklin Gothic'; font-size: 16px;")
        self.custom_interval_input.hide()

        self.custom_duration_input = QSpinBox()
        self.custom_duration_input.setRange(1, 500)
        self.custom_duration_input.setStyleSheet("font-family: 'Franklin Gothic'; font-size: 16px;")
        self.custom_duration_input.hide()

        start_button = QPushButton("Start")
        start_button.clicked.connect(self.get_values)
        start_button.setStyleSheet("font-family: 'Franklin Gothic'; font-size: 16px; background-color: #007acc; color: white; font-weight: bold;")

        layout.addWidget(self.custom_interval_checkbox)
        layout.addWidget(interval_label)
        layout.addWidget(self.interval_input)
        layout.addWidget(self.custom_interval_input)

        layout.addSpacing(10) 

        layout.addWidget(duration_label)
        layout.addWidget(self.duration_input)
        layout.addWidget(self.custom_duration_input)
        
        layout.addSpacing(20)

        layout.addWidget(start_button)

        self.setLayout(layout)

        show_action = QAction("Open", self)
        quit_action = QAction("Quit", self)
        show_action.triggered.connect(self.restore_from_tray)
        quit_action.triggered.connect(self.quit_application)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)

    def get_values(self):
        self.hide()
        if self.custom_interval_checkbox.isChecked():
            interval_value = self.custom_interval_input.value()
            #print(f"Custom Interval Selected: {interval_value} minutes")
            duration_value = self.custom_duration_input.value()
            #print(f"Custom Duration Selected: {duration_value} minutes")
            self.start(interval_value, duration_value)
        else:
            interval_index = self.interval_input.currentIndex()
            interval_value = self.break_intervals[interval_index]
            #print(f"Standard Interval Selected: {interval_value} minutes")
            duration_index = self.duration_input.currentIndex()
            duration_value = self.break_durations[duration_index]
            #print(f"Standard Duration Selected: {duration_value} minutes")
            self.start(interval_value, duration_value)

    def start(self, interval_value, duration_value):
        while True:
            time.sleep((interval_value*60)-4)
            self.show_notification("TAKE A BREAK", "break", duration_value)
            time.sleep((duration_value*60)-4)
            self.show_notification("GET BACK TO WORK", "work", interval_value)

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
            
    def show_notification(self, text, stext, duration):
        toast = ToastNotifier()
        toast.show_toast(text, f"{duration} min {stext}", duration=4)

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
    app.setStyle("Windows")
    sys.exit(app.exec_())

import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSlider, QPushButton


class SettingsWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
        self.load_current_theme()

    def setup_ui(self):
        self.setWindowTitle("Настройки")
        self.setGeometry(300, 300, 300, 150)
        layout = QVBoxLayout()
        header_label = QLabel("Настройки темы")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header_label)
        theme_layout = QHBoxLayout()
        self.theme_slider = QSlider(Qt.Orientation.Horizontal)
        self.theme_slider.setMinimum(0)
        self.theme_slider.setMaximum(1)
        self.theme_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.theme_slider.setTickInterval(1)
        light_label = QLabel("Светлая")
        dark_label = QLabel("Темная")
        theme_layout.addWidget(light_label)
        theme_layout.addWidget(self.theme_slider)
        theme_layout.addWidget(dark_label)
        layout.addLayout(theme_layout)
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)
        self.theme_slider.valueChanged.connect(self.change_theme)

    def load_current_theme(self):
        if os.path.exists('settings.txt'):
            try:
                with open('settings.txt', 'r') as f:
                    theme = f.read().strip()
                    if theme == 'dark':
                        self.theme_slider.setValue(1)
                    else:
                        self.theme_slider.setValue(0)
                    self.apply_theme(theme)
            except:
                self.theme_slider.setValue(0)
                self.apply_theme('white')
        else:
            self.theme_slider.setValue(0)
            self.apply_theme('white')

    def change_theme(self, value):
        theme = 'dark' if value == 1 else 'white'
        with open('settings.txt', 'w') as f:
            f.write(theme)
        self.apply_theme(theme)
        if self.main_window:
            self.main_window.set_theme(theme)

    def apply_theme(self, theme):
        if theme == 'dark':
            self.setStyleSheet("QWidget { background-color: #2b2b2b; color: white; }")
        else:
            self.setStyleSheet("QWidget { background-color: white; color: black; }")


def load_current_theme(self):
    import os
    if os.path.exists('settings.txt'):
        try:
            with open('settings.txt', 'r') as f:
                theme = f.read().strip()
                if theme == 'dark':
                    self.setStyleSheet("QWidget { background-color: #2b2b2b; color: white; }")
                else:
                    self.setStyleSheet("QWidget { background-color: white; color: black; }")
        except:
            self.setStyleSheet("QWidget { background-color: white; color: black; }")
    else:
        self.setStyleSheet("QWidget { background-color: white; color: black; }")

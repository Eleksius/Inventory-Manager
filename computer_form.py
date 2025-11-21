from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox

from settings import load_current_theme
import sqlite3


class ComputerForm(QWidget):
    def __init__(self, computer_data=None):
        super().__init__()
        self.computer_data = computer_data
        self.setup_ui()
        load_current_theme(self)
        if computer_data:
            self.fill_form()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название компьютера")
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("IP адрес")
        self.mac_input = QLineEdit()
        self.mac_input.setPlaceholderText("MAC адрес")
        self.cpu_input = QLineEdit()
        self.cpu_input.setPlaceholderText("Процессор")
        self.ram_input = QLineEdit()
        self.ram_input.setPlaceholderText("ОЗУ (ГБ)")
        self.os_input = QLineEdit()
        self.os_input.setPlaceholderText("Операционная система")
        self.status_combo = QComboBox()
        self.load_statuses()
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Заметки")
        self.notes_input.setMaximumHeight(100)
        layout.addWidget(QLabel("Название:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("IP адрес:"))
        layout.addWidget(self.ip_input)
        layout.addWidget(QLabel("MAC адрес:"))
        layout.addWidget(self.mac_input)
        layout.addWidget(QLabel("Процессор:"))
        layout.addWidget(self.cpu_input)
        layout.addWidget(QLabel("ОЗУ (ГБ):"))
        layout.addWidget(self.ram_input)
        layout.addWidget(QLabel("ОС:"))
        layout.addWidget(self.os_input)
        layout.addWidget(QLabel("Статус:"))
        layout.addWidget(self.status_combo)
        layout.addWidget(QLabel("Заметки:"))
        layout.addWidget(self.notes_input)
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.cancel_button = QPushButton("Отмена")
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
        self.setWindowTitle("Форма компьютера")
        self.setGeometry(200, 200, 400, 500)

    def load_statuses(self):
        try:
            conn = sqlite3.connect('computers.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM statuses ORDER BY id")
            statuses = cursor.fetchall()
            conn.close()
            for status in statuses:
                self.status_combo.addItem(status[1], status[0])
        except:
            self.status_combo.addItem("В работе", 1)
            self.status_combo.addItem("На ремонте", 2)
            self.status_combo.addItem("Списан", 3)
            self.status_combo.addItem("Резерв", 4)

    def fill_form(self):
        self.name_input.setText(self.computer_data['name'])
        self.ip_input.setText(self.computer_data['ip_address'])
        self.mac_input.setText(self.computer_data['mac_address'])
        self.cpu_input.setText(self.computer_data['cpu'])
        self.ram_input.setText(self.computer_data['ram'])
        self.os_input.setText(self.computer_data['os'])
        self.notes_input.setPlainText(self.computer_data['notes'])
        if 'status' in self.computer_data and self.computer_data['status']:
            index = self.status_combo.findText(self.computer_data['status'])
            if index >= 0:
                self.status_combo.setCurrentIndex(index)

    def get_data(self):
        return {
            'name': self.name_input.text(),
            'ip_address': self.ip_input.text(),
            'mac_address': self.mac_input.text(),
            'cpu': self.cpu_input.text(),
            'ram': self.ram_input.text(),
            'os': self.os_input.text(),
            'notes': self.notes_input.toPlainText(),
            'status_id': self.status_combo.currentData() if self.status_combo.currentData() else 1
        }

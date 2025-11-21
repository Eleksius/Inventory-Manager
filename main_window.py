from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, \
    QMessageBox, QFrame

from computer_card import ComputerCard
from computer_form import ComputerForm
from db_manager import init_database, select_all_computers_db, add_computer_db, edit_computer_db, \
    delete_computer_db, get_statistics_db
from settings import SettingsWindow
from settings import load_current_theme
from PyQt6.QtGui import QPixmap
import sqlite3, sys, os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        init_database(self)
        self.setup_ui()
        load_current_theme(self)
        self.load_computers()

    def setup_ui(self):
        self.setWindowTitle("Инвентаризация компьютеров")
        self.setGeometry(100, 100, 1000, 700)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        header_layout = QHBoxLayout()
        logo_label = QLabel()
        image_path = resource_path('images/computer.png')
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setFixedSize(32, 32)
        header_label = QLabel("Инвентаризация компьютеров")
        header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.add_button = QPushButton("Добавить компьютер")
        self.add_button.setStyleSheet("background-color: #66cc66; padding: 10px;")
        self.settings_button = QPushButton("Настройки")
        self.settings_button.setStyleSheet("padding: 10px;")
        self.exit_button = QPushButton("Выйти")
        self.exit_button.setStyleSheet("background-color: #ff6666; padding: 10px;")
        header_layout.addWidget(logo_label)
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        header_layout.addWidget(self.settings_button)
        header_layout.addWidget(self.add_button)
        header_layout.addWidget(self.exit_button)
        main_layout.addLayout(header_layout)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.scroll_widget)
        main_layout.addWidget(self.scroll_area)
        self.stats_frame = QFrame()
        self.stats_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        self.stats_layout = QHBoxLayout(self.stats_frame)
        self.total_label = QLabel("Всего компьютеров: 0")
        self.status_labels = []
        self.stats_layout.addWidget(self.total_label)
        self.stats_layout.addStretch()
        main_layout.addWidget(self.stats_frame)
        self.add_button.clicked.connect(self.add_computer)
        self.settings_button.clicked.connect(self.open_settings)
        self.exit_button.clicked.connect(self.close)

    def load_computers(self):
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)
        conn = sqlite3.connect('computers.db')
        computers = select_all_computers_db(self)
        total_count, status_counts = get_statistics_db(self)
        conn.close()
        self.total_label.setText(f"Всего компьютеров: {total_count}")
        for label in self.status_labels:
            self.stats_layout.removeWidget(label)
            label.deleteLater()
        self.status_labels.clear()
        for status_name, count in status_counts:
            label = QLabel(f"{status_name}: {count}")
            self.stats_layout.addWidget(label)
            self.status_labels.append(label)
        for computer in computers:
            computer_data = {
                'id': computer[0],
                'name': computer[1],
                'ip_address': computer[2],
                'mac_address': computer[3],
                'cpu': computer[4],
                'ram': computer[5],
                'os': computer[6],
                'notes': computer[7],
                'status': computer[8] if computer[8] else 'Не указан'
            }
            card = ComputerCard(computer_data)
            card.edit_button.clicked.connect(lambda checked, c=computer_data: self.edit_computer(c))
            card.delete_button.clicked.connect(lambda checked, id=computer[0]: self.delete_computer(id))
            self.scroll_layout.addWidget(card)

    def add_computer(self):
        self.form = ComputerForm()
        self.form.save_button.clicked.connect(self.save_new_computer)
        self.form.cancel_button.clicked.connect(self.form.close)
        self.form.setWindowTitle("Добавить компьютер")
        self.form.setGeometry(200, 200, 400, 500)
        self.form.show()

    def save_new_computer(self):
        data = self.form.get_data()
        if not data['name']:
            QMessageBox.warning(self,
                                "Ошибка", "Пожалуйста, введите название компьютера")
            return
        try:
            conn = sqlite3.connect('computers.db')
            add_computer_db(self, data)
            conn.close()
            self.form.close()
            self.load_computers()
            QMessageBox.information(self,
                                    "Успех", "Компьютер успешно добавлен")
        except Exception as e:
            QMessageBox.critical(self,
                                 "Ошибка", f"Ошибка при добавлении компьютера: {str(e)}")

    def edit_computer(self, computer_data):
        self.form = ComputerForm(computer_data)
        self.form.save_button.clicked.connect(lambda: self.save_edited_computer(computer_data['id']))
        self.form.cancel_button.clicked.connect(self.form.close)
        self.form.setWindowTitle("Редактировать компьютер")
        self.form.setGeometry(200, 200, 400, 500)
        self.form.show()

    def save_edited_computer(self, computer_id):
        data = self.form.get_data()
        if not data['name']:
            QMessageBox.warning(self,
                                "Ошибка", "Пожалуйста, введите название компьютера")
            return
        try:
            conn = sqlite3.connect('computers.db')
            edit_computer_db(self, data, computer_id)
            conn.close()
            self.form.close()
            self.load_computers()
            QMessageBox.information(self,
                                    "Успех", "Информация о компьютере успешно обновлена")
        except Exception as e:
            QMessageBox.critical(self,
                                 "Ошибка", f"Ошибка при обновлении информации: {str(e)}")

    def delete_computer(self, computer_id):
        reply = QMessageBox.question(self, "Подтверждение",
                                     "Вы уверены, что хотите удалить этот компьютер?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = sqlite3.connect('computers.db')
                delete_computer_db(self, computer_id)
                conn.close()
                self.load_computers()
                QMessageBox.information(self,
                                        "Успех", "Компьютер успешно удален")
            except Exception as e:
                QMessageBox.critical(self,
                                     "Ошибка", f"Ошибка при удалении компьютера: {str(e)}")

    def open_settings(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()

    def set_theme(self, theme):
        if theme == 'dark':
            self.setStyleSheet("QWidget { background-color: #2b2b2b; color: white; }")
            self.stats_frame.setStyleSheet("QFrame { background-color: #3c3c3c; }")
        else:
            self.setStyleSheet("QWidget { background-color: white; color: black; }")
            self.stats_frame.setStyleSheet("QFrame { background-color: #f0f0f0; }")

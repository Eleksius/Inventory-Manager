from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QGridLayout, QTextEdit, QHBoxLayout, QPushButton


class ComputerCard(QFrame):
    def __init__(self, computer_data, parent=None):
        super().__init__(parent)
        self.computer_data = computer_data
        self.setup_ui()

    def setup_ui(self):
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setLineWidth(1)
        layout = QVBoxLayout()
        name_label = QLabel(f"<b>{self.computer_data['name']}</b>")
        name_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(name_label)
        info_layout = QGridLayout()
        info_layout.addWidget(QLabel("IP адрес:"), 0, 0)
        info_layout.addWidget(QLabel(self.computer_data['ip_address']), 0, 1)
        info_layout.addWidget(QLabel("MAC адрес:"), 1, 0)
        info_layout.addWidget(QLabel(self.computer_data['mac_address']), 1, 1)
        info_layout.addWidget(QLabel("Процессор:"), 2, 0)
        info_layout.addWidget(QLabel(self.computer_data['cpu']), 2, 1)
        info_layout.addWidget(QLabel("ОЗУ:"), 3, 0)
        info_layout.addWidget(QLabel(self.computer_data['ram']), 3, 1)
        info_layout.addWidget(QLabel("ОС:"), 4, 0)
        info_layout.addWidget(QLabel(self.computer_data['os']), 4, 1)
        info_layout.addWidget(QLabel("Статус:"), 5, 0)
        info_layout.addWidget(QLabel(self.computer_data.get('status', 'Не указан')), 5, 1)
        layout.addLayout(info_layout)
        if self.computer_data['notes']:
            notes_label = QLabel("<b>Заметки:</b>")
            layout.addWidget(notes_label)
            notes_text = QTextEdit()
            notes_text.setPlainText(self.computer_data['notes'])
            notes_text.setMaximumHeight(100)
            notes_text.setReadOnly(True)
            layout.addWidget(notes_text)
        buttons_layout = QHBoxLayout()
        self.edit_button = QPushButton("Редактировать")
        self.edit_button.setStyleSheet("background-color: #4794ff;")
        self.delete_button = QPushButton("Удалить")
        self.delete_button.setStyleSheet("background-color: #ff6666;")
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

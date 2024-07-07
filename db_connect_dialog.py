from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox

class DbConnectDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Подключение к базе данных")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QFormLayout()

        self.dbname_input = QLineEdit("coursework")
        self.user_input = QLineEdit()
        self.layout.addRow("Имя пользователя:", self.user_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addRow("Пароль:", self.password_input)

        self.host_input = QLineEdit("localhost")
        self.port_input = QLineEdit("5432")

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    def get_connection_data(self):
        return {
            "dbname": self.dbname_input.text(),
            "user": self.user_input.text(),
            "password": self.password_input.text(),
            "host": self.host_input.text(),
            "port": self.port_input.text(),
        }

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QDateEdit
from PyQt5.QtCore import QDate

class QueryWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Запросы")
        self.setGeometry(150, 150, 600, 400)

        layout = QVBoxLayout()

        self.query1_button = QPushButton("Запрос 1: Все данные")
        self.query1_button.clicked.connect(self.main_window.query_all_data)
        layout.addWidget(self.query1_button)

        self.query2_layout = QFormLayout()
        self.query2_button = QPushButton("Запрос 2: Публикации за период")
        self.query2_start_date = QDateEdit()
        self.query2_start_date.setCalendarPopup(True)
        self.query2_start_date.setDate(QDate.currentDate().addYears(-1))
        self.query2_end_date = QDateEdit()
        self.query2_end_date.setCalendarPopup(True)
        self.query2_end_date.setDate(QDate.currentDate())
        self.query2_button.clicked.connect(self.query_publications_by_date)
        self.query2_layout.addRow("Дата начала:", self.query2_start_date)
        self.query2_layout.addRow("Дата окончания:", self.query2_end_date)
        self.query2_layout.addWidget(self.query2_button)
        layout.addLayout(self.query2_layout)

        self.query3_layout = QFormLayout()
        self.query3_button = QPushButton("Запрос 3: Поиск по ключевому слову в тексте публикации")
        self.query3_keyword = QLineEdit()
        self.query3_button.clicked.connect(self.query_search_by_keyword)
        self.query3_layout.addRow("Ключевое слово:", self.query3_keyword)
        self.query3_layout.addWidget(self.query3_button)
        layout.addLayout(self.query3_layout)

        self.query4_layout = QFormLayout()
        self.query4_button = QPushButton("Запрос 4: Участники по роли")
        self.query4_role = QLineEdit("Журналист")
        self.query4_button.clicked.connect(self.query_participants_by_role)
        self.query4_layout.addRow("Роль:", self.query4_role)
        self.query4_layout.addWidget(self.query4_button)
        layout.addLayout(self.query4_layout)

        self.query5_layout = QFormLayout()
        self.query5_button = QPushButton("Запрос 5: Поиск публикаций по ключевому слову в заголовке")
        self.query5_keyword = QLineEdit()
        self.query5_button.clicked.connect(self.query_publications_with_keyword_in_title)
        self.query5_layout.addRow("Ключевое слово:", self.query5_keyword)
        self.query5_layout.addWidget(self.query5_button)
        layout.addLayout(self.query5_layout)

        self.setLayout(layout)

    def query_publications_by_date(self):
        start_date = self.query2_start_date.date().toString("yyyy-MM-dd")
        end_date = self.query2_end_date.date().toString("yyyy-MM-dd")
        self.main_window.query_publications_by_date(start_date, end_date)

    def query_search_by_keyword(self):
        keyword = self.query3_keyword.text()
        self.main_window.query_search_by_keyword(keyword)

    def query_participants_by_role(self):
        role = self.query4_role.text()
        self.main_window.query_participants_by_role(role)

    def query_publications_with_keyword_in_title(self):
        keyword = self.query5_keyword.text()
        self.main_window.query_publications_with_keyword_in_title(keyword)

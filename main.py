import sys
import psycopg2
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget,
                             QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem, QDialog, QFormLayout,
                             QDialogButtonBox, QMessageBox, QLabel, QDateEdit, QRadioButton, QButtonGroup,
                             QComboBox)
from PyQt5.QtCore import QDate

class DbConnectDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Подключение к базе данных")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QFormLayout()

        self.dbname_input = QLineEdit("coursework")
        #self.layout.addRow("Название базы данных:", self.dbname_input)

        self.user_input = QLineEdit()
        self.layout.addRow("Имя пользователя:", self.user_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addRow("Пароль:", self.password_input)

        self.host_input = QLineEdit("localhost")
        #self.layout.addRow("Хост:", self.host_input)

        self.port_input = QLineEdit("5432")
        #self.layout.addRow("Порт:", self.port_input)

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

class DataManagementDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Управление данными")
        self.setGeometry(150, 150, 800, 600)

        layout = QVBoxLayout()

        self.table_selection_group = QButtonGroup(self)
        table_selection_layout = QHBoxLayout()

        self.smi_radio = QRadioButton("smi")
        self.smi_radio.setChecked(True)
        self.table_selection_group.addButton(self.smi_radio)
        table_selection_layout.addWidget(self.smi_radio)

        self.publications_radio = QRadioButton("publications")
        self.table_selection_group.addButton(self.publications_radio)
        table_selection_layout.addWidget(self.publications_radio)

        self.participants_radio = QRadioButton("participants")
        self.table_selection_group.addButton(self.participants_radio)
        table_selection_layout.addWidget(self.participants_radio)

        self.relationship_radio = QRadioButton("participantAndPublicatonsRelationship")
        self.table_selection_group.addButton(self.relationship_radio)
        table_selection_layout.addWidget(self.relationship_radio)

        layout.addLayout(table_selection_layout)

        self.data_table = QTableWidget()
        layout.addWidget(self.data_table)

        buttons_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_record)
        buttons_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Редактировать")
        self.edit_button.clicked.connect(self.edit_record)
        buttons_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_record)
        buttons_layout.addWidget(self.delete_button)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.back_to_main)
        buttons_layout.addWidget(self.back_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.table_selection_group.buttonClicked.connect(self.load_table_data)
        self.load_table_data()

    def load_table_data(self):
        selected_button = self.table_selection_group.checkedButton()
        table_name = selected_button.text()

        if table_name == "publications":
            query = """
            SELECT
                publications.id_publication,
                smi.name AS smi_name,
                publications.category,
                publications.title,
                publications.summary,
                publications.publication_date,
                publications.last_edited
            FROM
                publications
            JOIN
                smi ON publications.id_smi = smi.id_smi;
            """
        elif table_name == "participants":
            query = """
            SELECT
                id_participant,
                surname,
                name,
                role,
                contact_info
            FROM
                participants;
            """
        elif table_name == "smi":
            query = """
            SELECT
                id_smi,
                name,
                type,
                contact_info
            FROM
                smi;
            """
        elif table_name == "participantAndPublicatonsRelationship":
            query = """
            SELECT
                participantAndPublicatonsRelationship.id_relationship,
                publications.title AS publication_title,
                participants.surname AS participant_surname,
                participants.name AS participant_name,
                participantAndPublicatonsRelationship.price
            FROM
                participantAndPublicatonsRelationship
            JOIN
                publications ON participantAndPublicatonsRelationship.id_publication = publications.id_publication
            JOIN
                participants ON participantAndPublicatonsRelationship.id_participant = participants.id_participant;
            """
        self.main_window.run_query_for_table(query, self.data_table)

    def add_record(self):
        selected_table = self.table_selection_group.checkedButton().text()
        dialog = DataEntryDialog(self.main_window, f"add_{selected_table}")
        if dialog.exec_() == QDialog.Accepted:
            self.load_table_data()

    def edit_record(self):
        selected_table = self.table_selection_group.checkedButton().text()
        selected_row = self.data_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите строку для редактирования.")
            return

        data = {}
        for col in range(self.data_table.columnCount()):
            header = self.data_table.horizontalHeaderItem(col).text()
            data[header] = self.data_table.item(selected_row, col).text()

        dialog = DataEntryDialog(self.main_window, f"update_{selected_table}", data)
        if dialog.exec_() == QDialog.Accepted:
            self.load_table_data()

    def delete_record(self):
        selected_table = self.table_selection_group.checkedButton().text()
        selected_row = self.data_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите строку для удаления.")
            return

        data = {}
        for col in range(self.data_table.columnCount()):
            header = self.data_table.horizontalHeaderItem(col).text()
            data[header] = self.data_table.item(selected_row, col).text()

        dialog = DataEntryDialog(self.main_window, f"delete_{selected_table}", data)
        if dialog.exec_() == QDialog.Accepted:
            self.load_table_data()

    def back_to_main(self):
        self.accept()

class DataEntryDialog(QDialog):
    def __init__(self, main_window, operation, data=None):
        super().__init__()
        self.main_window = main_window
        self.operation = operation
        self.setWindowTitle(f"Операция: {operation}")

        self.layout = QFormLayout()
        self.fields = {}
        self.hidden_fields = {}
        self.id_mapping = {}

        if operation in ["add_smi", "update_smi"]:
            self.fields["name"] = QLineEdit()
            self.fields["type"] = QLineEdit()
            self.fields["contact_info"] = QLineEdit()
            self.layout.addRow("Название:", self.fields["name"])
            self.layout.addRow("Тип:", self.fields["type"])
            self.layout.addRow("Контактная информация:", self.fields["contact_info"])
            if operation == "update_smi" and data:
                self.hidden_fields["id_smi"] = data["id_smi"]
                self.fields["name"].setText(data["name"])
                self.fields["type"].setText(data["type"])
                self.fields["contact_info"].setText(data["contact_info"])

        elif operation == "delete_smi":
            self.hidden_fields["id_smi"] = data["id_smi"] if data else None

        elif operation in ["add_publications", "update_publications"]:
            self.fields["id_smi"] = QComboBox()
            self.main_window.populate_combobox(self.fields["id_smi"], "smi", "id_smi", "name", self.id_mapping)
            self.fields["category"] = QLineEdit()
            self.fields["title"] = QLineEdit()
            self.fields["summary"] = QLineEdit()
            self.fields["publication_date"] = QDateEdit()
            self.fields["publication_date"].setCalendarPopup(True)
            self.fields["publication_date"].setDisplayFormat("yyyy-MM-dd")

            self.layout.addRow("СМИ:", self.fields["id_smi"])
            self.layout.addRow("Категория:", self.fields["category"])
            self.layout.addRow("Заголовок:", self.fields["title"])
            self.layout.addRow("Описание:", self.fields["summary"])
            self.layout.addRow("Дата публикации (YYYY-MM-DD):", self.fields["publication_date"])

            if operation == "update_publications" and data:
                self.hidden_fields["id_publication"] = data["id_publication"]
                self.fields["category"].setText(data["category"])
                self.fields["title"].setText(data["title"])
                self.fields["summary"].setText(data["summary"])
                publication_date = QDate.fromString(data["publication_date"], "yyyy-MM-dd")
                self.fields["publication_date"].setDate(publication_date)

        elif operation == "delete_publications":
            self.hidden_fields["id_publication"] = data["id_publication"] if data else None

        elif operation in ["add_participants", "update_participants"]:
            self.fields["surname"] = QLineEdit()
            self.fields["name"] = QLineEdit()
            self.fields["role"] = QLineEdit()
            self.fields["contact_info"] = QLineEdit()
            self.layout.addRow("Фамилия:", self.fields["surname"])
            self.layout.addRow("Имя:", self.fields["name"])
            self.layout.addRow("Роль:", self.fields["role"])
            self.layout.addRow("Контактная информация:", self.fields["contact_info"])
            if operation == "update_participants" and data:
                self.hidden_fields["id_participant"] = data["id_participant"]
                self.fields["surname"].setText(data["surname"])
                self.fields["name"].setText(data["name"])
                self.fields["role"].setText(data["role"])
                self.fields["contact_info"].setText(data["contact_info"])

        elif operation == "delete_participants":
            self.hidden_fields["id_participant"] = data["id_participant"] if data else None

        elif operation in ["add_participantAndPublicatonsRelationship", "update_participantAndPublicatonsRelationship"]:
            self.fields["pub_id"] = QComboBox()
            self.main_window.populate_combobox(self.fields["pub_id"], "publications", "id_publication", "title", self.id_mapping)
            self.fields["part_id"] = QComboBox()
            self.main_window.populate_combobox(self.fields["part_id"], "participants", "id_participant", "surname || ' ' || name", self.id_mapping)
            self.fields["price"] = QLineEdit()
            self.layout.addRow("Публикация:", self.fields["pub_id"])
            self.layout.addRow("Участник:", self.fields["part_id"])
            self.layout.addRow("Цена:", self.fields["price"])
            if operation == "update_participantAndPublicatonsRelationship" and data:
                self.hidden_fields["id_relationship"] = data.get("id_relationship", "")
                self.fields["price"].setText(data["price"])

        elif operation == "delete_participantAndPublicatonsRelationship":
            self.hidden_fields["id_relationship"] = data["id_relationship"] if data else None

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    def accept(self):
        data = {key: self.id_mapping.get(field.currentText(), field.currentText()) if isinstance(field, QComboBox) else field.text() for key, field in self.fields.items()}
        data.update(self.hidden_fields)
        if self.operation.startswith("add_"):
            self.main_window.add_record(self.operation, data)
        elif self.operation.startswith("update_"):
            self.main_window.update_record(self.operation, data)
        elif self.operation.startswith("delete_"):
            self.main_window.delete_record(self.operation, data)
        super().accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Управление базой данных")
        self.setGeometry(100, 100, 1200, 800)

        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)

        self.connect_button = QPushButton("Подключиться к базе данных")
        self.connect_button.clicked.connect(self.open_db_connect_dialog)
        left_layout.addWidget(self.connect_button)

        self.task2_button = QPushButton("Задание 2")
        self.task2_button.clicked.connect(self.open_query_widget)
        self.task2_button.setEnabled(False)
        left_layout.addWidget(self.task2_button)

        self.manage_data_button = QPushButton("Управление данными")
        self.manage_data_button.clicked.connect(self.open_data_management_dialog)
        self.manage_data_button.setEnabled(False)
        left_layout.addWidget(self.manage_data_button)

        self.query_button = QPushButton("Выполнить запрос")
        self.query_button.clicked.connect(self.execute_query)
        left_layout.addWidget(self.query_button)

        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.clicked.connect(self.query_all_data)
        left_layout.addWidget(self.refresh_button)

        self.query_label = QLabel("Введите запрос:")
        left_layout.addWidget(self.query_label)

        self.query_input = QTextEdit()
        left_layout.addWidget(self.query_input)

        left_widget.setLayout(left_layout)

        right_layout = QVBoxLayout()
        self.result_table = QTableWidget()
        right_layout.addWidget(self.result_table)

        top_layout.addWidget(left_widget, 1)
        top_layout.addLayout(right_layout, 3)

        main_layout.addLayout(top_layout)

        self.container = QWidget()
        self.container.setLayout(main_layout)
        self.setCentralWidget(self.container)

    def open_db_connect_dialog(self):
        dialog = DbConnectDialog()
        if dialog.exec_() == QDialog.Accepted:
            connection_data = dialog.get_connection_data()
            self.connect_to_db(connection_data)

    def connect_to_db(self, connection_data):
        try:
            self.conn = psycopg2.connect(
                dbname=connection_data["dbname"],
                user=connection_data["user"],
                password=connection_data["password"],
                host=connection_data["host"],
                port=connection_data["port"]
            )
            self.cursor = self.conn.cursor()
            self.show_message("Успех", "Подключение к базе данных успешно выполнено.")
            self.task2_button.setEnabled(True)
            self.manage_data_button.setEnabled(True)
        except Exception as e:
            self.show_message("Ошибка", f"Не удалось подключиться.")

    def open_query_widget(self):
        self.query_widget = QueryWidget(self)
        self.query_widget.show()

    def open_data_management_dialog(self):
        dialog = DataManagementDialog(self)
        dialog.exec_()

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def execute_query(self):
        query = self.query_input.toPlainText()
        self.run_query(query)

    def run_query_for_table(self, query, table_widget):
        try:
            self.cursor.execute(query)
            self.conn.commit()
            if query.lower().strip().startswith("select"):
                records = self.cursor.fetchall()
                headers = [desc[0] for desc in self.cursor.description]
                table_widget.setRowCount(len(records))
                table_widget.setColumnCount(len(headers))
                table_widget.setHorizontalHeaderLabels(headers)
                for i, row in enumerate(records):
                    for j, col in enumerate(row):
                        table_widget.setItem(i, j, QTableWidgetItem(str(col)))
                self.hide_key_columns(table_widget, headers)
        except Exception as e:
            try:
                self.conn.rollback()
                self.show_message("Ошибка", f"Не удалось выполнить запрос.")
            except Exception as e:
                print('')

    def hide_key_columns(self, table_widget, headers):
        key_columns = [index for index, header in enumerate(headers) if "id_" in header]
        for col in key_columns:
            table_widget.setColumnHidden(col, True)

    def run_query(self, query):
        try:
            self.cursor.execute(query)
            self.conn.commit()
            if query.lower().strip().startswith("select"):
                records = self.cursor.fetchall()
                headers = [desc[0] for desc in self.cursor.description]
                self.result_table.setRowCount(len(records))
                self.result_table.setColumnCount(len(headers))
                self.result_table.setHorizontalHeaderLabels(headers)
                for i, row in enumerate(records):
                    for j, col in enumerate(row):
                        self.result_table.setItem(i, j, QTableWidgetItem(str(col)))
                self.hide_key_columns(self.result_table, headers)
            self.show_message("Успех", "Запрос успешно выполнен.")
        except Exception as e:
            try:
                self.conn.rollback()
                self.show_message("Ошибка", f"Не удалось выполнить запрос.")
            except Exception as e:
                print('')

    def populate_combobox(self, combobox, table_name, id_field, display_field, id_mapping):
        try:
            query = f"SELECT {id_field}, {display_field} FROM {table_name};"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            combobox.clear()
            for record in records:
                id_mapping[record[1]] = record[0]
                combobox.addItem(record[1])
        except Exception as e:
            self.conn.rollback()
            self.show_message("Ошибка", f"Не удалось загрузить данные для выпадающего списка.")

    def query_all_data(self):
        query = """
        SELECT
            smi.name AS "Название СМИ",
            smi.type AS "Тип СМИ",
            smi.contact_info AS "Контакты СМИ",
            publications.category AS "Категория публикации",
            publications.title AS "Заголовок публикации",
            publications.summary AS "Текст публикации",
            publications.publication_date AS "Дата публикации",
            publications.last_edited AS "Дата последнего редактирования",
            participants.surname AS "Фамилия участника",
            participants.name AS "Имя участника",
            participants.role AS "Роль участника",
            participants.contact_info AS "Контакты участника",
            participantAndPublicatonsRelationship.price AS "Цена участия"
        FROM
            participantAndPublicatonsRelationship
        JOIN
            publications ON participantAndPublicatonsRelationship.id_publication = publications.id_publication
        JOIN
            smi ON publications.id_smi = smi.id_smi
        JOIN
            participants ON participantAndPublicatonsRelationship.id_participant = participants.id_participant
        ORDER BY
            publications.publication_date DESC, smi.name, participants.surname;
        """
        self.run_query(query)

    def query_publications_by_date(self, start_date, end_date):
        query = f"""
        SELECT title, summary, publication_date, last_edited FROM publications
        WHERE publication_date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY publication_date DESC;
        """
        self.run_query(query)

    def query_search_by_keyword(self, keyword):
        query = f"""
        SELECT title, summary, publication_date, last_edited FROM publications
        WHERE summary LIKE '%{keyword}%'
        ORDER BY publication_date DESC;
        """
        self.run_query(query)

    def query_participants_by_role(self, role):
        query = f"""
        SELECT name, surname, role, contact_info FROM participants
        WHERE role = '{role}';
        """
        self.run_query(query)

    def query_publications_with_keyword_in_title(self, keyword):
        query = f"""
        SELECT p.title, p.summary, part.name, part.surname
        FROM publications p
        JOIN participantAndPublicatonsRelationship pr ON p.id_publication = pr.id_publication
        JOIN participants part ON pr.id_participant = part.id_participant
        WHERE p.title LIKE '%{keyword}%';
        """
        self.run_query(query)

    def add_record(self, operation, data):
        try:
            if operation == "add_smi":
                query = f"SELECT add_smi('{data['name']}', '{data['type']}', '{data['contact_info']}');"
            elif operation == "add_publications":
                query = f"SELECT add_publication({data['id_smi']}, '{data['category']}', '{data['title']}', '{data['summary']}', '{data['publication_date']}');"
            elif operation == "add_participants":
                query = f"SELECT add_participant('{data['surname']}', '{data['name']}', '{data['role']}', '{data['contact_info']}');"
            elif operation == "add_participantAndPublicatonsRelationship":
                query = f"SELECT add_relationship({data['pub_id']}, {data['part_id']}, {data['price']});"
            self.cursor.execute(query)
            self.conn.commit()
            self.show_message("Успех", "Запись успешно добавлена.")
        except Exception as e:
            self.conn.rollback()
            self.show_message("Ошибка", f"Не удалось добавить запись.")

    def update_record(self, operation, data):
        try:
            if operation == "update_smi":
                query = f"SELECT update_smi({data['id_smi']}, '{data['name']}', '{data['type']}', '{data['contact_info']}');"
            elif operation == "update_publications":
                query = f"SELECT update_publication({data['id_publication']}, {data['id_smi']}, '{data['category']}', '{data['title']}', '{data['summary']}', '{data['publication_date']}');"
            elif operation == "update_participants":
                query = f"SELECT update_participant({data['id_participant']}, '{data['surname']}', '{data['name']}', '{data['role']}', '{data['contact_info']}');"
            elif operation == "update_participantAndPublicatonsRelationship":
                query = f"SELECT update_relationship({data['id_relationship']}, {data['pub_id']}, {data['part_id']}, {data['price']});"
            self.cursor.execute(query)
            self.conn.commit()
            self.show_message("Успех", "Запись успешно обновлена.")
        except Exception as e:
            self.conn.rollback()
            self.show_message("Ошибка", f"Не удалось обновить запись.")

    def delete_record(self, operation, data):
        try:
            if operation == "delete_smi":
                query = f"SELECT delete_smi({data['id_smi']});"
            elif operation == "delete_publications":
                query = f"SELECT delete_publication({data['id_publication']});"
            elif operation == "delete_participants":
                query = f"SELECT delete_participant({data['id_participant']});"
            elif operation == "delete_participantAndPublicatonsRelationship":
                query = f"SELECT delete_relationship({data['id_relationship']});"
            self.cursor.execute(query)
            self.conn.commit()
            self.show_message("Успех", "Запись успешно удалена.")
        except Exception as e:
            self.conn.rollback()
            self.show_message("Ошибка", "Не удалось удалить запись.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

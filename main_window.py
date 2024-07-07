import psycopg2
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QTextEdit, QTableWidget, QTableWidgetItem, QMessageBox, QLabel, QDialog
from db_connect_dialog import DbConnectDialog
from query_widget import QueryWidget
from data_management_dialog import DataManagementDialog

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

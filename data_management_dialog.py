from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QButtonGroup, QRadioButton, QTableWidget, QPushButton, QMessageBox
from data_entry_dialog import DataEntryDialog

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

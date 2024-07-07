from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDateEdit, QComboBox, QDialogButtonBox
from PyQt5.QtCore import QDate

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

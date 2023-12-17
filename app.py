import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QDialog, QLabel, QLineEdit, QFormLayout, QDateEdit
from PyQt5.QtCore import Qt
import psycopg2

class DatabaseViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PostgreSQL Database Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        info_label = QLabel("Малёнкин Яков Олегович, 4 курс 4 группа 2023 год")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(info_label)

        self.table_combobox = QComboBox()
        self.layout.addWidget(self.table_combobox)

        button_layout = QHBoxLayout()

        self.show_button = QPushButton("Show Table")
        self.edit_button = QPushButton("Edit")
        self.apply_button = QPushButton("Apply Changes")
        self.cancel_button = QPushButton("Cancel Changes")
        self.add_button = QPushButton("Add Row")
        self.delete_button = QPushButton("Delete Row")
        self.apply_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        self.delete_button.setEnabled(False)

        button_layout.addWidget(self.show_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)

        self.layout.addLayout(button_layout)

        self.table_view = QTableWidget()
        self.layout.addWidget(self.table_view)

        self.central_widget.setLayout(self.layout)

        self.db_connection = psycopg2.connect(
            dbname="HRM",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )

        self.edit_mode = False
        self.original_data = None

        self.load_tables()

        self.table_view.setSortingEnabled(True)

        self.show_button.clicked.connect(self.show_table)
        self.edit_button.clicked.connect(self.enable_editing)
        self.apply_button.clicked.connect(self.apply_changes)
        self.cancel_button.clicked.connect(self.cancel_changes)
        self.add_button.clicked.connect(self.add_row_dialog)
        self.delete_button.clicked.connect(self.delete_row)

    def load_tables(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = [row[0] for row in cursor.fetchall()]
        self.table_combobox.addItems(tables)
        cursor.close()

    def show_table(self):
        selected_table = self.table_combobox.currentText()

        cursor = self.db_connection.cursor()
        cursor.execute(f"SELECT * FROM {selected_table}")
        rows = cursor.fetchall()

        self.table_view.setRowCount(len(rows))
        if len(rows) > 0:
            column_names = [desc[0] for desc in cursor.description]
            self.table_view.setColumnCount(len(column_names))
            self.table_view.setHorizontalHeaderLabels(column_names)
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.table_view.setItem(i, j, item)
                    if j in [0, 2]:
                        item.setData(Qt.UserRole, value)

        cursor.close()

        self.delete_button.setEnabled(False)

    def enable_editing(self):
        self.edit_mode = True
        self.apply_button.setEnabled(True)
        self.cancel_button.setEnabled(True)
        self.original_data = []

        for i in range(self.table_view.rowCount()):
            row_data = []
            for j in range(self.table_view.columnCount()):
                item = self.table_view.item(i, j)
                row_data.append(item.text())
            self.original_data.append(row_data)

        self.delete_button.setEnabled(True)

    def apply_changes(self):
        if self.edit_mode:
            selected_table = self.table_combobox.currentText()
            cursor = self.db_connection.cursor()

            for i in range(self.table_view.rowCount()):
                row_data = []
                for j in range(self.table_view.columnCount()):
                    item = self.table_view.item(i, j)
                    row_data.append(item.text())

                record_id = self.table_view.item(i, 0).text()

                update_query = f"UPDATE {selected_table} SET "
                for j, column_name in enumerate(self.table_view.horizontalHeaderItem(j).text() for j in range(1, self.table_view.columnCount())):
                    update_query += f"{column_name} = %s"
                    if j < self.table_view.columnCount() - 2:
                        update_query += ", "

                update_query += f" WHERE {self.table_view.horizontalHeaderItem(0).text()} = %s"
                values = row_data[1:] + [record_id]

                cursor.execute(update_query, values)
                self.db_connection.commit()

            cursor.close()
            self.edit_mode = False
            self.apply_button.setEnabled(False)
            self.cancel_button.setEnabled(False)

    def cancel_changes(self):
        if self.edit_mode and self.original_data:
            for i in range(self.table_view.rowCount()):
                for j in range(self.table_view.columnCount()):
                    item = self.table_view.item(i, j)
                    item.setText(self.original_data[i][j])

        self.edit_mode = False
        self.apply_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def add_row_dialog(self):
        selected_table = self.table_combobox.currentText()
        column_names = [self.table_view.horizontalHeaderItem(j).text() for j in range(self.table_view.columnCount())]
        
        add_dialog = AddRowDialog(column_names, self.db_connection)
        if add_dialog.exec_():
            new_row_values = add_dialog.get_row_values()
            
            if new_row_values:
                cursor = self.db_connection.cursor()
                insert_query = f"INSERT INTO {selected_table} ({', '.join(column_names[1:])}) VALUES ({', '.join(['%s'] * (len(column_names) - 1))})"
                cursor.execute(insert_query, new_row_values)
                self.db_connection.commit()
                cursor.close()
                self.show_table()

    def delete_row(self):
        if self.edit_mode:
            self.cancel_changes()
        
        selected_row = self.table_view.currentRow()

        if selected_row >= 0:
            selected_table = self.table_combobox.currentText()
            item = self.table_view.item(selected_row, 0)
            record_id = item.text()

            cursor = self.db_connection.cursor()

            update_query = f"UPDATE departments SET is_active = false WHERE departmentid = %s"
            cursor.execute(update_query, (record_id,))
            self.db_connection.commit()
            cursor.close()

            self.load_tables()

class AddRowDialog(QDialog):
    def __init__(self, column_names, db_connection):
        super().__init__()
        self.setWindowTitle("Add New Row")
        self.db_connection = psycopg2.connect(
            dbname="HRM",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        self.layout = QFormLayout()
        self.row_values = {}

        for column_name in column_names[1:]:
            label = QLabel(column_name)
            if column_name == 'creationdate':
                date_edit = QDateEdit()
                date_edit.setCalendarPopup(True)
                self.layout.addRow(label, date_edit)
                self.row_values[column_name] = date_edit
            elif column_name == 'departmentid':
                department_combobox = QComboBox()
                department_combobox.addItems(self.get_department_names(self.db_connection))
                self.layout.addRow(label, department_combobox)
                self.row_values[column_name] = department_combobox
            elif column_name == 'birthdate':
                date_edit = QDateEdit()
                date_edit.setCalendarPopup(True)
                self.layout.addRow(label, date_edit)
                self.row_values[column_name] = date_edit
            else:
                line_edit = QLineEdit()
                self.layout.addRow(label, line_edit)
                self.row_values[column_name] = line_edit

        add_button = QPushButton("Add")
        add_button.clicked.connect(self.accept)
        self.layout.addWidget(add_button)
        self.setLayout(self.layout)

    def get_row_values(self):
        values = []
        for column_name, widget in self.row_values.items():
            if column_name == 'creationdate':
                values.append(widget.date().toString("yyyy-MM-dd"))
            elif column_name == 'departmentid':
                values.append(self.get_department_id(widget.currentText()))
            else:
                values.append(widget.text())
        return values

    def get_department_names(self, db_connection):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT departmentname FROM departments WHERE is_active = true")
        department_names = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return department_names

    def get_department_id(self, department_name):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT departmentid FROM departments WHERE departmentname = %s", (department_name,))
        department_id = cursor.fetchone()[0]
        cursor.close()
        return department_id

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseViewer()
    window.show()
    sys.exit(app.exec())

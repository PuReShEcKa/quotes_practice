from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from database import QuotesDB
from ui_design import Ui_CollectionOfQuotes


class MainWindow(QMainWindow, Ui_CollectionOfQuotes):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.db = QuotesDB()
        self.current_image_path = ""

        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['Текст', 'Автор', 'Категория', 'Дата', 'Избранное'])
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        self.categoryComboBox.addItems(['Мотивация', 'Жизнь', 'Любовь', 'Философия', 'Юмор', 'Другое'])

        self.addBtn.clicked.connect(self.add_quote)
        self.deleteBtn.clicked.connect(self.delete_quote)
        self.copyBtn.clicked.connect(self.copy_to_clipboard)
        self.loadImageBtn.clicked.connect(self.load_image)

        self.load_quotes()

    def add_quote(self):
        text = self.textEdit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Ошибка", "Введите текст цитаты!")
            return

        author = self.authorLineEdit.text().strip()
        category = self.categoryComboBox.currentText()
        date = self.dateEdit.date().toString("yyyy-MM-dd")
        favorite = 1 if self.favoriteCheckBox.isChecked() else 0

        self.db.add_quote(text, author, category, date, favorite, self.current_image_path)
        self.load_quotes()
        self.clear_fields()
        QMessageBox.information(self, "Успех", "Цитата добавлена!")

    def delete_quote(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите цитату!")
            return

        quote_id = self.tableWidget.item(row, 0).data(Qt.UserRole)
        reply = QMessageBox.question(self, "Удаление", "Удалить цитату?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.delete_quote(quote_id)
            self.load_quotes()

    def load_quotes(self):
        quotes = self.db.get_all_quotes()
        self.tableWidget.setRowCount(0)

        for row, q in enumerate(quotes):
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(q[1]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(q[2] or ""))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(q[3] or ""))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(q[4] or ""))
            self.tableWidget.setItem(row, 4, QTableWidgetItem("Избранное" if q[5] else ""))

            self.tableWidget.item(row, 0).setData(Qt.UserRole, q[0])

    def copy_to_clipboard(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите цитату!")
            return

        text = self.tableWidget.item(row, 0).text()
        author = self.tableWidget.item(row, 1).text()

        clipboard = QApplication.clipboard()
        if author:
            clipboard.setText(f'"{text}" — {author}')
        else:
            clipboard.setText(text)

        QMessageBox.information(self, "Успех", "Цитата скопирована!")

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "",
                                              "Images (*.png *.jpg *.jpeg *.bmp)")
        if path:
            self.current_image_path = path
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                self.imageLabel.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.imageLabel.setText("")

    def clear_fields(self):
        self.textEdit.clear()
        self.authorLineEdit.clear()
        self.favoriteCheckBox.setChecked(False)
        self.dateEdit.setDate(QDate.currentDate())
        self.imageLabel.setText("Нет изображения")
        self.imageLabel.setPixmap(QPixmap())
        self.current_image_path = ""

    def closeEvent(self, event):
        self.db.close()
        event.accept()
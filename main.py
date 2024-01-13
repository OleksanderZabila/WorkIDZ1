import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QFileDialog
from bs4 import BeautifulSoup
import requests

class ParserApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.text_edit = QTextEdit(self)
        self.parse_button = QPushButton('Parse', self)
        self.parse_button.clicked.connect(self.parse_content)
        self.open_file_button = QPushButton('Open File', self)
        self.open_file_button.clicked.connect(self.open_file)
        self.url_button = QPushButton('Parse URL', self)
        self.url_button.clicked.connect(self.parse_url)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.parse_button)
        layout.addWidget(self.open_file_button)
        layout.addWidget(self.url_button)

        self.setLayout(layout)

        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle('Parser App')
        self.show()

    def parse_content(self):
        content = self.text_edit.toPlainText()
        parsed_data = self.parse_data(content)
        # Далее можно обработать parsed_data по вашим потребностям
        print(parsed_data)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Text File', '', 'Text Files (*.txt);;All Files (*)')
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_edit.setPlainText(content)

    def parse_url(self):
        url, ok = QFileDialog.getOpenFileName(self, 'Open URL', '')
        if ok:
            response = requests.get(url)
            content = response.text
            self.text_edit.setPlainText(content)

    def parse_data(self, data):
        # Ваш код для парсинга данных (используя BeautifulSoup, например)
        # Здесь просто возвращается сам введенный текст, так как это пример
        return data


if __name__ == '__main__':
    app = QApplication(sys.argv)
    parser_app = ParserApp()
    sys.exit(app.exec_())

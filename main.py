import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QFileDialog, QInputDialog, QDialog, QLabel
from docx import Document
from nltk import FreqDist, word_tokenize, download
import spacy

class ResultWindow(QDialog):
    def __init__(self, stats):
        super().__init__()

        self.setWindowTitle('Статистика')
        self.setGeometry(400, 400, 400, 300)

        self.label = QLabel(self)
        result_text = "\n".join([f"{key}: {value}" for key, value in stats.items()])
        self.label.setText(result_text)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

class TextParserApp(QWidget):
    def __init__(self):
        super().__init__()

        self.stop_words = set(spacy.lang.uk.stop_words.STOP_WORDS)  # Використовуємо стоп-слова з spaCy
        self.init_ui()

    def init_ui(self):
        self.text_edit = QTextEdit(self)
        self.parse_button = QPushButton('Аналізувати', self)
        self.parse_button.clicked.connect(self.parse_content)
        self.open_file_button = QPushButton('Відкрити файл', self)
        self.open_file_button.clicked.connect(self.open_file)
        self.set_stop_words_button = QPushButton('Встановити зупинні слова', self)
        self.set_stop_words_button.clicked.connect(self.set_stop_words)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.parse_button)
        layout.addWidget(self.open_file_button)
        layout.addWidget(self.set_stop_words_button)

        self.setLayout(layout)

        self.setGeometry(300, 300, 700, 600)
        self.setWindowTitle('Аналізатор тексту')
        self.show()

    def parse_content(self):
        content = self.text_edit.toPlainText()
        words = self.tokenize_text(content)
        # Видаляємо зупинні слова
        words = [word for word in words if word.lower() not in self.stop_words]
        stats = self.calculate_statistics(words)
        result_window = ResultWindow(stats)
        result_window.exec_()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Відкрити текстовий файл', '', 'Текстові файли (*.txt);;Документи Word (*.docx);;Всі файли (*)')
        if file_path:
            if file_path.endswith(".txt"):
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_edit.setPlainText(content)
                    self.parse_content()
            elif file_path.endswith(".docx"):
                document = Document(file_path)
                content = "\n".join([paragraph.text for paragraph in document.paragraphs])
                self.text_edit.setPlainText(content)
                self.parse_content()

    def set_stop_words(self):
        user_input, ok_pressed = QInputDialog.getText(self, "Встановити зупинні слова", "Введіть зупинні слова (розділені комою):")
        if ok_pressed and user_input:
            self.stop_words = set(user_input.lower().split(','))

    def tokenize_text(self, text):
        return word_tokenize(text)

    def calculate_statistics(self, words):
        freq_dist = FreqDist(words)
        total_characters_with_spaces = sum(len(word) for word in words)
        total_characters_without_spaces = len(''.join(words))
        total_letters = sum(c.isalpha() for c in ''.join(words))
        foreign_words = sum(c.isalpha() and not c.isascii() for c in ''.join(words))
        total_punctuation = sum(c in ',.!?' for c in ''.join(words))
        # Додайте інші статистики за необхідності

        return {
            'Загальна кількість слів': len(words),
            'Загальна кількість символів із пробілами': total_characters_with_spaces,
            'Загальна кількість символів без пробілів': total_characters_without_spaces,
            'Загальна кількість літер': total_letters,
            'Кількість іноземних слів': foreign_words,
            'Загальна кількість знаків пунктуації': total_punctuation,
            # Додайте інші статистики
        }

if __name__ == '__main__':
    app = QApplication(sys.argv)
    parser_app = TextParserApp()
    app.exec_()

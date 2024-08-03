import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QCheckBox, QMessageBox, QDialog, QDialogButtonBox, QScrollArea, QLineEdit
)
from PyQt5.QtCore import Qt, QTimer
from html import unescape  # For cleaning HTML entities

class TriviaApp(QMainWindow):
    CATEGORIES = {
        "General Knowledge": 9,
        "Entertainment: Books": 10,
        "Entertainment: Film": 11,
        "Entertainment: Music": 12,
        "Science: Computers": 18,
        "Entertainment: Games": 15,
        "Science: Gadgets": 17,
        "Entertainment: Japanese Anime & Manga": 31,
        "Entertainment: Video Games": 16,
        "Entertainment: Board Games": 29,
        "Science: Nature": 17,
        "Science: Technology": 18,
        "Entertainment: Comics": 29,
        "Entertainment: Music Albums": 12,
        "Science: Astronomy": 17,
        "Science: Mythology": 20,
        "Science: Biology": 17,
        "Science: Chemistry": 17,
        "Science: Physics": 17,
        "Science: Geology": 17,
        "Science: Mathematics": 17,
        "Entertainment: Television": 14,
        "Entertainment: Art": 25,
        "Entertainment: Celebrity": 26,
        "Entertainment: History": 23,
        "Entertainment: Politics": 24,
        "Entertainment: Geography": 22,
        "Entertainment: Literature": 10,
        "Entertainment: Music Theory": 12,
        "Entertainment: Theatre": 15,
        "Entertainment: Movies": 11,
        "Entertainment: Books and Literature": 10,
        "Entertainment: Music (Pop)": 12,
        "Entertainment: Music (Rock)": 12,
        "Entertainment: Music (Jazz)": 12,
        "Entertainment: Music (Classical)": 12,
        "Entertainment: Music (Country)": 12,
        "Entertainment: Music (Electronic)": 12,
        "Entertainment: Music (Rap)": 12,
        "Entertainment: Music (Reggae)": 12,
        "Entertainment: Music (Blues)": 12,
        "Entertainment: Music (Soul)": 12,
        "Entertainment: Music (R&B)": 12,
        "Entertainment: Music (Folk)": 12,
        "Entertainment: Music (Alternative)": 12,
        "Entertainment: Music (Indie)": 12,
        "Entertainment: Music (Metal)": 12,
        "Entertainment: Music (Punk)": 12,
        "Entertainment: Music (Latin)": 12,
        "Entertainment: Music (World)": 12,
        "Entertainment: Music (Opera)": 12,
        "Entertainment: Music (Gospel)": 12,
        "Entertainment: Music (Other)": 12,
        "Entertainment: Music (Musicals)": 12,
        "Entertainment: Music (Experimental)": 12,
        "Entertainment: Music (Traditional)": 12,
        "Entertainment: Music (Show Tunes)": 12
    }

    def __init__(self):
        super().__init__()

        self.selected_categories = []
        self.current_question = ""
        self.current_answer = ""

        self.setWindowTitle("Trivia App")
        self.setGeometry(100, 100, 600, 400)  # Adjusted resolution

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch_trivia)  # Fetch trivia periodically
        self.timer.start(60000)  # Example: Fetch trivia every 60 seconds

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.select_categories_button = QPushButton("Choose Categories", self)
        self.select_categories_button.setStyleSheet(self.button_style())
        self.select_categories_button.clicked.connect(self.open_category_selection)

        self.fetch_button = QPushButton("Get Trivia", self)
        self.fetch_button.setStyleSheet(self.button_style())
        self.fetch_button.clicked.connect(self.fetch_trivia)
        
        self.restart_button = QPushButton("Restart", self)
        self.restart_button.setStyleSheet(self.button_style())
        self.restart_button.clicked.connect(self.restart_app)

        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setStyleSheet(self.button_style())
        self.exit_button.clicked.connect(self.close_app)

        self.trivia_label = QLabel("Trivia will be displayed here.", self)
        self.trivia_label.setStyleSheet("font-size: 18px;")

        self.reveal_button = QPushButton("Reveal Answer", self)
        self.reveal_button.setStyleSheet(self.button_style())
        self.reveal_button.clicked.connect(self.reveal_answer)
        self.reveal_button.setEnabled(False)  # Disabled initially

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.select_categories_button)
        self.layout.addWidget(self.fetch_button)
        self.layout.addWidget(self.restart_button)
        self.layout.addWidget(self.exit_button)
        self.layout.addWidget(self.trivia_label)
        self.layout.addWidget(self.reveal_button)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        self.setStyleSheet("background-color: #e6f0ff;")  # Light blue color

    def create_layout(self):
        # Layout is handled in create_widgets
        pass

    def button_style(self):
        return (
            "font-size: 16px; padding: 12px; border-radius: 8px;"
            "background: linear-gradient(to bottom, #a1c4fd, #c2e9fb);"
            "border: 2px solid #6fa3ef;"
            "box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"
            "color: #0033cc;"
        )

    def open_category_selection(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Categories")

        dialog_layout = QVBoxLayout()

        # Scroll area setup
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: #f0f8ff;")  # Very light blue

        container_widget = QWidget()
        container_layout = QVBoxLayout()
        self.category_checkboxes = []

        for category in self.CATEGORIES:
            checkbox = QCheckBox(category, container_widget)
            checkbox.setChecked(self.CATEGORIES[category] in self.selected_categories)
            checkbox.stateChanged.connect(self.on_category_changed)
            container_layout.addWidget(checkbox)
            self.category_checkboxes.append(checkbox)

        container_widget.setLayout(container_layout)
        scroll_area.setWidget(container_widget)

        # Back button
        back_button = QPushButton("Back", self)
        back_button.setStyleSheet("font-size: 12px; padding: 5px;")
        back_button.clicked.connect(dialog.reject)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok, Qt.Horizontal, dialog)
        button_box.accepted.connect(dialog.accept)

        dialog_layout.addWidget(back_button)
        dialog_layout.addWidget(scroll_area)
        dialog_layout.addWidget(button_box)
        dialog.setLayout(dialog_layout)
        dialog.exec_()

    def on_category_changed(self, state):
        source = self.sender()
        category = source.text()
        if state == Qt.Checked:  # Checked
            if self.CATEGORIES[category] not in self.selected_categories:
                self.selected_categories.append(self.CATEGORIES[category])
        else:  # Unchecked
            if self.CATEGORIES[category] in self.selected_categories:
                self.selected_categories.remove(self.CATEGORIES[category])

    def fetch_trivia(self):
        if not self.selected_categories:
            self.trivia_label.setText("Please select at least one category.")
            self.reveal_button.setEnabled(False)
            return
        
        category_ids = ','.join(map(str, self.selected_categories))
        url = f"https://opentdb.com/api.php?amount=1&category={category_ids}&type=multiple"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()

            # Debugging: Print the full response
            print("API Response:", data)

            if 'results' in data and data['results']:
                question = unescape(data['results'][0]['question'])  # Clean HTML entities
                answer = unescape(data['results'][0]['correct_answer'])  # Clean HTML entities
                self.current_question = question
                self.current_answer = answer
                self.trivia_label.setText(f"Trivia: {question}")
                self.reveal_button.setEnabled(True)
            else:
                self.trivia_label.setText("No trivia available for the selected categories.")
                self.reveal_button.setEnabled(False)
        except requests.RequestException as e:
            self.trivia_label.setText("An error occurred while fetching trivia.")
            print(f"Error: {e}")

    def reveal_answer(self):
        if self.current_answer:
            self.trivia_label.setText(f"Trivia: {self.current_question}<br>Answer: {self.current_answer}")

    def restart_app(self):
        self.selected_categories = []
        self.current_question = ""
        self.current_answer = ""
        self.trivia_label.setText("Trivia will be displayed here.")
        self.reveal_button.setEnabled(False)

    def close_app(self):
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TriviaApp()
    window.show()
    sys.exit(app.exec_())

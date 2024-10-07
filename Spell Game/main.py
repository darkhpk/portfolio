import sys
import random
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, 
    QMessageBox, QMainWindow, QStackedWidget, QInputDialog, QListWidget, QListWidgetItem, QSplitter
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MainMenu(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        # Create buttons
        self.play_button = QPushButton('Play', self)
        self.settings_button = QPushButton('Settings', self)
        self.score_button = QPushButton('Score', self)

        # Connect buttons to their functions
        self.play_button.clicked.connect(self.start_game)
        self.settings_button.clicked.connect(self.open_settings)
        self.score_button.clicked.connect(self.view_score)

        # Layout
        self.top_scores_label = QLabel('Top 10 Scores:', self)
        self.update_top_scores()

        layout = QVBoxLayout()
        layout.addWidget(self.top_scores_label)
        layout.addWidget(self.play_button)
        layout.addWidget(self.settings_button)
        layout.addWidget(self.score_button)

        self.setLayout(layout)
        self.setWindowTitle('Main Menu')

    def start_game(self):
        self.stacked_widget.setCurrentIndex(1)  # Switch to game screen

    def open_settings(self):
        self.stacked_widget.setCurrentIndex(3)  # Switch to settings screen

    def view_score(self):
        self.stacked_widget.setCurrentIndex(2)  # Switch to score screen

    def update_top_scores(self):
        try:
            with open('score_data.json', 'r') as file:
                score_data = json.load(file)
            sorted_scores = sorted(score_data, key=lambda x: x['hits'], reverse=True)[:10]
            scores_text = 'Top 10 Scores:\n'
            for entry in sorted_scores:
                scores_text += f"{entry['name']}: Hits = {entry['hits']}, Misses = {entry['misses']}\n"
            self.top_scores_label.setText(scores_text)
        except Exception as e:
            self.top_scores_label.setText(f'No scores found: {e}')

class SpellingGame(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        # Load the image dictionary from a JSON file
        self.image_dict = self.load_image_dict('image_data.json')
        self.words = list(self.image_dict.keys())
        random.shuffle(self.words)
        self.current_word_index = 0
        self.current_word = self.words[self.current_word_index]
        
        self.hits = 0
        self.misses = 0

        # Set up the GUI components
        self.initUI()

    def load_image_dict(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
            return data
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load image data: {e}')
            sys.exit(1)

    def initUI(self):
        # Image display
        self.image_label = QLabel(self)
        self.update_image()

        # Input field
        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText('Type the name here')
        self.input_line.returnPressed.connect(self.check_answer)  # Connect Enter key to submit action

        # Submit button
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.check_answer)

        # Score display
        self.hit_label = QLabel(f'Hits: {self.hits}', self)
        self.miss_label = QLabel(f'Misses: {self.misses}', self)

        # Layout
        score_layout = QHBoxLayout()
        score_layout.addWidget(self.hit_label)
        score_layout.addWidget(self.miss_label)

        layout = QVBoxLayout()
        layout.addLayout(score_layout)
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.input_line)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
        self.setWindowTitle('Spelling Game')

    def update_image(self):
        pixmap = QPixmap(self.image_dict[self.current_word])
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        
    def check_answer(self):
        user_input = self.input_line.text().strip().lower()

        if user_input == self.current_word:
            self.hits += 1
            self.hit_label.setText(f'Hits: {self.hits}')
            QMessageBox.information(self, 'Correct!', 'You spelled it correctly!')
        else:
            self.misses += 1
            self.miss_label.setText(f'Misses: {self.misses}')
            QMessageBox.warning(self, 'Incorrect', 'Try again!')

        self.current_word_index += 1

        if self.current_word_index < len(self.words):
            self.current_word = self.words[self.current_word_index]
            self.update_image()
            self.input_line.clear()
        else:
            self.get_player_name_and_save_score()
            QMessageBox.information(self, 'Well Done!', 'You completed the game!')
            self.stacked_widget.setCurrentIndex(0)  # Return to main menu
            self.stacked_widget.widget(0).update_top_scores()  # Update top scores on the main menu

    def get_player_name_and_save_score(self):
        name, ok = QInputDialog.getText(self, 'Player Name', 'Enter your name:')
        if ok and name:
            self.save_score(name)

    def save_score(self, player_name):
        new_score = {'name': player_name, 'hits': self.hits, 'misses': self.misses}
        try:
            with open('score_data.json', 'r') as file:
                score_data = json.load(file)
        except FileNotFoundError:
            score_data = []

        score_data.append(new_score)

        try:
            with open('score_data.json', 'w') as file:
                json.dump(score_data, file)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save score data: {e}')

class ScoreScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        self.score_label = QLabel('Scores will be displayed here.', self)
        self.back_button = QPushButton('Back to Menu', self)
        self.back_button.clicked.connect(self.back_to_menu)

        layout = QVBoxLayout()
        layout.addWidget(self.score_label)
        layout.addWidget(self.back_button)
        self.setLayout(layout)
        self.setWindowTitle('Score')

        self.load_scores()

    def load_scores(self):
        try:
            with open('score_data.json', 'r') as file:
                score_data = json.load(file)
            sorted_scores = sorted(score_data, key=lambda x: x['hits'], reverse=True)
            scores_text = ''
            for entry in sorted_scores:
                scores_text += f"{entry['name']}: Hits = {entry['hits']}, Misses = {entry['misses']}\n"
            self.score_label.setText(scores_text)
        except Exception as e:
            self.score_label.setText(f'No scores found: {e}')

    def back_to_menu(self):
        self.stacked_widget.setCurrentIndex(0)  # Return to main menu

class SettingsScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create the navigation list
        self.nav_list = QListWidget(self)
        self.nav_list.setFixedWidth(200)
        self.nav_list.addItem(QListWidgetItem("Graphics"))
        self.nav_list.addItem(QListWidgetItem("Sound"))
        self.nav_list.addItem(QListWidgetItem("Update/Version"))
        self.nav_list.addItem(QListWidgetItem("About"))

        # Create the stacked widget for different setting pages
        self.settings_pages = QStackedWidget(self)
        
        # Graphics settings page
        self.graphics_page = QLabel("Graphics Settings", self)
        self.settings_pages.addWidget(self.graphics_page)
        
        # Sound settings page
        self.sound_page = QLabel("Sound Settings", self)
        self.settings_pages.addWidget(self.sound_page)
        
        # Update/Version settings page
        self.update_page = QLabel("Update/Version Information", self)
        self.settings_pages.addWidget(self.update_page)
        
        # About settings page
        self.about_page = QLabel("About this Application", self)
        self.settings_pages.addWidget(self.about_page)

        # Connect the navigation list to change the settings page
        self.nav_list.currentRowChanged.connect(self.settings_pages.setCurrentIndex)

        # Layout the components
        layout = QHBoxLayout()
        layout.addWidget(self.nav_list, 1)
        layout.addWidget(self.settings_pages, 3)

        self.setLayout(layout)
        self.setWindowTitle('Settings')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Spelling Game')
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.main_menu = MainMenu(self.stacked_widget)
        self.spelling_game = SpellingGame(self.stacked_widget)
        self.score_screen = ScoreScreen(self.stacked_widget)
        self.settings_screen = SettingsScreen()
        
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.spelling_game)
        self.stacked_widget.addWidget(self.score_screen)
        self.stacked_widget.addWidget(self.settings_screen)
        
        self.stacked_widget.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

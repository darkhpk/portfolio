import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, \
QPushButton, QGridLayout

class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle("Calculator")
        self.setGeometry(100, 100, 300, 400)

        # Create a QVBoxLayout to arrange widgets vertically
        self.layout = QVBoxLayout()

        # Create the display where expressions and results will be shown
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFixedHeight(50)
        self.layout.addWidget(self.display)

        # Create the layout for the buttons
        self.buttons_layout = QGridLayout()

        # Define the buttons labels in a grid layout
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', 'C', '=', '+'
        ]

        # Add buttons to the grid layout
        row = 0
        col = 0
        for button_text in buttons:
            button = QPushButton(button_text)
            button.setFixedHeight(50)
            button.clicked.connect(lambda checked, text=button_text: self.on_button_clicked(text))
            self.buttons_layout.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Add the grid layout of buttons to the main layout
        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)
    
    def on_button_clicked(self, button_text):
        current_text = self.display.text()

        if button_text == 'C':
            # Clear the display
            self.display.clear()
        elif button_text == '=':
            try:
                result = eval(current_text)
                self.display.setText(str(result))
            except Exception:
                self.display.setText("Error")
        else:
            # Append the clicked button text to the current expression
            self.display.setText(current_text + button_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())
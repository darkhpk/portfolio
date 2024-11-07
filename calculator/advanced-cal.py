import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Advance Calculator")
        self.setGeometry(100, 100, 400, 500)

        # Create a QVBoxLayout to arrange widgets vertically
        self.layout = QVBoxLayout()

        # Create the display where expressions and resuts will be shown
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFixedHeight(50)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setStyleSheet("font-size: 24px;")
        self.layout.addWidget(self.display)

        # Create a grid layout for the buttons
        self.buttons_layout = QGridLayout()
        self.buttons_layout.setSpacing(5)

        buttons = {
            '7': (0, 0), '8': (0, 1), '9': (0, 2), '/': (0, 3), 'sin': (0, 4),
            '4': (1, 0), '5': (1, 1), '6': (1, 2), '*': (1, 3), 'cos': (1, 4),
            '1': (2, 0), '2': (2, 1), '3': (2, 2), '-': (2, 3), 'tan': (2, 4),
            '0': (3, 0), '.': (3, 1), '^': (3, 2), '+': (3, 3), 'log': (3, 4),
            '(': (4, 0), ')': (4, 1), 'sqrt': (4, 2), 'ln': (4, 3), 'π': (4, 4),
            'C': (5, 0), 'e': (5, 1), 'Ans': (5, 2), '=': (5, 3, 1, 2)
        }

        # Add buttons to the grid layout
        for btn_text, pos in buttons.items():
            button = QPushButton(btn_text)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            button.setStyleSheet("font-size: 18px;")
            if len(pos) == 2:
                self.buttons_layout.addWidget(button, pos[0], pos[1])
            else:
                self.buttons_layout.addWidget(button, pos[0], pos[1], pos[2], pos[3])
            
            button.clicked.connect(lambda checked, text=btn_text: self.on_button_clicked(text))
        
        # Add the grid layout of buttons to the main layout
        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)

        # Store the last answer
        self.last_answer = ''
    
    def on_button_clicked(self, button_text):
        current_text = self.display.text()

        if button_text == 'C':
            self.display.clear()
        elif button_text == '=':
            try:
                expression = current_text.replace('π', str(math.pi)).replace('e', str(math.e))

                expression = expression.replace('^', '**')

                expression = expression.replace('sin', 'math.sin(math.radians')
                expression = expression.replace('cos', 'math.cos(math.radians')
                expression = expression.replace('tan', 'math.tan(math.radians')

                result = eval(expression, {"__builtins__": None}, math.__dict__)
                self.display.setText(str(result))
                self.last_answer = str(result)
            
            except ZeroDivisionError:
                self.display.setText("Error: Division by zero!")
            except Exception as e:
                self.display.setText("Error")
        elif button_text == 'Ans':
            self.display.setText(current_text + self.last_answer)
        elif button_text in ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt']:
            if button_text in ['log', 'ln', 'sqrt']:
                self.display.setText(current_text + 'math.' + button_text + '(')
            else:
                self.display.setText(current_text + 'math.' + button_text + '(math.radians(')
        elif button_text == 'π':
            self.display.setText(current_text + 'π')
        elif button_text == 'e':
            self.display.setText(current_text + 'e')
        else:
            self.display.setText(current_text + button_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())
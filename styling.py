import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy

class PublicArea(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize 
        self.setWindowTitle("Public Area")
        self.setGeometry(100, 100, 800, 600)
        
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)  # Add margins to reduce the full screen fill effect
        layout.setSpacing(20)  # Add spacing between widgets
        widget.setLayout(layout)
        
        # Styling
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                color: #000000;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLineEdit, QPushButton {
                background-color: #ffffff;
                border: 1px solid #000000;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QLabel {
                font-weight: bold;
            }
        """)

        # Welcome Label
        self.welcome_label = QLabel("WELCOME")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("""
            font-size: 32px;
            border: 1px solid #000000;
            padding: 10px;
        """)
        layout.addWidget(self.welcome_label)

        # Spacer
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Instruction Label
        self.instruction_label = QLabel("Please enter your master password")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setStyleSheet("""
            font-size: 20px;
            border: 1px solid #000000;
            padding: 10px;
        """)
        layout.addWidget(self.instruction_label)

        # Entry Field
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Entry field")
        self.entry.setAlignment(Qt.AlignCenter)
        self.entry.setStyleSheet("""
            font-size: 18px;
            border: 1px solid #000000;
            padding: 5px;
        """)
        layout.addWidget(self.entry)

        # Enter Button
        self.enter_button = QPushButton("Enter")
        self.enter_button.setStyleSheet("""
            font-size: 18px;
            border: 1px solid #000000;
            padding: 5px;
        """)
        layout.addWidget(self.enter_button)

        # Spacer
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

# Main application loop
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PublicArea()
    window.show()
    sys.exit(app.exec_())

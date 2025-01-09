import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *        #QApplication, QMainWindow, QVBoxLayout, QWidget, QSplitter, QListWidget
from PyQt5.QtCore import *           # Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget
from PasswordWidget import PasswordWidget

class PublicArea(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #Initilliaze 
        self.setWindowTitle("Public Area")
        self.setGeometry(100, 100, 800, 600)
        
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout() 
        widget.setLayout(layout)
        
        
        #styling
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLineEdit, QPushButton {
                background-color: #3c3f41;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 5px;
            }
            QLineEdit:focus, QPushButton:pressed {
                border: 1px solid #0078d7;
            }
            QSplitter::handle {
                background-color: #555555;
            }
            QFrame {
                border: none;
            }
            QLabel {
                font-weight: bold;
            }
        """)

        #Welcome Label
        self.welcome_label = QLabel("Welcome")
        layout.addWidget(self.welcome_label)
        
        #Instruction Label 
        self.instruction_label = QLabel("Please provide a masterpassword")
        layout.addWidget(self.instruction_label)
        self.instruction_label.setStyleSheet("""
                color: white; /* White text */
                border: 2px solid #0078d7; /* Green border */
                border-radius: 15px; /* Rounded corners */
                padding: 10px;
            """)  # Change the border color and width as needed

        #Entryfield
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Your Password...")
        layout.addWidget(self.entry)
   
   
#Debug        
# Main application loop
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PublicArea()
    window.show()
    sys.exit(app.exec_())
        
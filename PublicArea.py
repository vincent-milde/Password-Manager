import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *        #QApplication, QMainWindow, QVBoxLayout, QWidget, QSplitter, QListWidget
from PyQt5.QtCore import *           # Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget
from PasswordDataBase import PasswordDataBase
hasAcess = False    
class PublicArea(QMainWindow):
    #Constructor method
    def __init__(self):
        #init main methods
        super().__init__()
        self.init_ui()
        self.init_styling()
        

##################################
#                                #
#           UI ELements          #
#                                #
##################################   
     
    def init_ui(self):
        #Initilliaze 
        self.setWindowTitle("Public Area")
        self.setGeometry(100, 100, 800, 600)
        widget = QWidget()
        self.setCentralWidget(widget)
        
        #main layout
        layout = QVBoxLayout()
        widget.setLayout(layout)
        layout.setContentsMargins(50,50,50,50)
        layout.setSpacing(20)

        #styling with frame
        self.frame = QFrame()
        frame = self.frame
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)
        frame_layout = QGridLayout()
        frame.setLayout(frame_layout)
        layout.addWidget(frame)
        #Frame Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(5, 5)
        shadow.setColor(QColor(0,0,0, 160))
        frame.setGraphicsEffect(shadow)
        
        #Welcome Label
        self.welcome_label = QLabel("Welcome")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        #self.welcome_label.setFixedSize(300, 100)  # Set a fixed size for the label
        frame_layout.addWidget(self.welcome_label)
        
        # Instruction Label
        self.instruction_label = QLabel("Please provide a master password")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        #self.welcome_label.setFixedSize(300, 100)  # Set a fixed size for the label
        frame_layout.addWidget(self.instruction_label)

        #Entryfield
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Your Password...")
        self.entry.setEchoMode(QLineEdit.Password)
        frame_layout.addWidget(self.entry)
        
        #Login button
        self.login_button = QPushButton()
        self.login_button.setText("Login")
        self.login_button.clicked.connect(self.login_button_handler)
        frame_layout.addWidget(self.login_button)
    
    
##################################
#                                #
#             Styling            #
#                                #
##################################
    
    def init_styling(self):

        #Main style sheet
        PALETTE = {
            "background_color": "#522258",  # Main background
            "text_color": "#EFDBCB",        # Standard text color (assume white for contrast)
            "accent_color": "#8C3061",      # Accent color for important elements
            "highlight_color": "#C63C51",   # Highlight elements like buttons
            "secondary_bg": "#D95F59",      # Secondary background or subtle accents
        }

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {PALETTE['background_color']};
                color: {PALETTE['text_color']};
                font-family: Arial, sans-serif;
                font-size: 14px;
            }}
            QLineEdit, QPushButton, QLabel {{
                background-color: {PALETTE['highlight_color']};
                border: 1px solid {PALETTE['accent_color']};
                padding: 5px;
                border-radius: 5px;
            }}
            QLineEdit:focus, QPushButton:pressed {{
                border: 1px solid {PALETTE['highlight_color']};
            }}
        """)

        # Frame Styling
        self.frame.setStyleSheet(f"""
            background-color: {PALETTE['accent_color']};
            border: 2px solid {PALETTE['highlight_color']};
            border-radius: 15px;
            padding: 20px;
        """)
        
        # Welcome Label Styling
        self.welcome_label.setStyleSheet(f"""
            font-size: 48px;
            font-weight: bold;
            color: {PALETTE['text_color']};
            background-color: {PALETTE['highlight_color']}
        """)
        
        # Instruction Label Styling
        self.instruction_label.setStyleSheet(f"""
            font-size: 20px;
            margin: 10px 0px;
            background-color: {PALETTE['highlight_color']}
        """)
        
        self.login_button.setStyleSheet(f"""
            font-size: 25px;                       
            font-weight: bold;
            padding-left: 50px;
            padding-right: 50px;
            background-color: {PALETTE["secondary_bg"]};
            color: {PALETTE["text_color"]};
            border: 2px solid {PALETTE["highlight_color"]};
            border-radius: 10px;
            padding: 10px;
        """)
        
        
##################################
#                                #
#            Handlers            #
#                                #
##################################

    def login_button_handler(self):
        print("login button has been pressed")
        password = self.entry.text()
        db = PasswordDataBase(password)
        #check if there is a database
        if db.database_exists():       
            self.db_exists_handler(password,db)
        #create a new database
        elif not db.database_exists:
            self.db_does_not_exist_handler(password, db)
            
        #precaution
        else:
            Warning("undefined state when trying to log in")
            
    def db_exists_handler(self,password, db):               
        #if correct password
        if db.compare_masterpassword_hash(password):
            db.init_db(password)
            hasAcess = True
        #wrong password
        else:
            print("Wrong password!")    
            self.entry.clear()  
            self.instruction_label.setText()
                         
    def db_does_not_exist_handler(self,password, db):
        pass
              
#Debug        
# Main application loop
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PublicArea()
    window.show()
    sys.exit(app.exec_())
        
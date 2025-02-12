import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *        #QApplication, QMainWindow, QVBoxLayout, QWidget, QSplitter, QListWidget
from PyQt5.QtCore import *           # Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget
from PasswordDataBase import PasswordDataBase
hasAcess = False    
class PublicArea(QMainWindow):
    
    #signals for passing data
    login_successful = pyqtSignal(object, str, bool)  #(database, password, hasAcess)
    
    #Constructor method
    def __init__(self):
        #init object
        super().__init__()

        #global variables
        self.masterpassword = ""
        self.pass_old = None
        self.db = PasswordDataBase()
        self.hasAcess = False
        #init the GUI
        self.init_ui()
        self.init_styling()
        self.db_exists_handler(None)
        
        

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
        self.instruction_label = QLabel("Please provide a new master password (min 6)")
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
            "background_color": "#345DA7",  # Main background
            "text_color": "#FFFFFF",        # Standard text color (assume white for contrast)
            "accent_color": "#3B8AC4",      # Accent color for important elements
            "highlight_color": "#4BB4DE",   # Highlight elements like buttons
            "secondary_bg": "#EFDBCB",      # Secondary background or subtle accents
        }

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {PALETTE['background_color']};
                color: {PALETTE['text_color']};
                font-family: Arial, sans-serif;
                font-size: 14px;
            }}
            QLineEdit, QPushButton, QLabel {{
                background-color: {PALETTE['accent_color']};
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
            background-color: {PALETTE['background_color']};
            border: 2px solid {PALETTE['highlight_color']};
            border-radius: 15px;
            padding: 20px;
        """)
        
        # Welcome Label Styling
        self.welcome_label.setStyleSheet(f"""
            font-size: 48px;
            font-weight: bold;
            color: {PALETTE['text_color']};
            background-color: {PALETTE['accent_color']}
        """)
        
        # Instruction Label Styling
        self.instruction_label.setStyleSheet(f"""
            font-size: 20px;
            margin: 10px 0px;
            background-color: {PALETTE['accent_color']}
        """)
        #Login button styling
        self.login_button.setStyleSheet(f"""
            font-size: 25px;                       
            font-weight: bold;
            padding-left: 50px;
            padding-right: 50px;
            background-color: {PALETTE["highlight_color"]};
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
        password = self.entry.text()
        db = self.db
        #check if there is a database if not make a new one
        if not db.database_exists():       
            self.db_does_not_exist_handler(password)
        elif db.database_exists:
            self.db_exists_handler(password)
            
        #precaution
        else:
            Warning("undefined state when trying to log in")
    #database exists...      
    def db_exists_handler(self,password):   
        db = self.db         
           
        #if database exists and password is not none
        if db.database_exists() and password:
            
            #correct password
            if db.compare_masterpassword_hash(password):
                
                db.init_db(password)
                
                #pass data to main window
                self.masterpassword = password
                self.hasAcess = True
                
                #emit a signal for piping to main window
                self.login_successful.emit(self.db, self.masterpassword, self.hasAcess) 
                
            #wrong password
            elif password:
                print("Wrong password!")    
                self.entry.clear()  
                self.instruction_label.setText("Wrong password, try again.")
                
        #if db exists change default label text (init branch)        
        elif db.database_exists():
            print("Database exists")    
            self.entry.clear()  
            self.instruction_label.setText("Please enter your masterpassword")
            
    #database does not exist                    
    def db_does_not_exist_handler(self,password):
        
        #database and variables to store last password for checking
        db = self.db
        pass_new = self.entry.text()
        self.entry.clear()
        
        #password has to be at least 6 characters
        if len(pass_new) >= 6: 
            
            self.instruction_label.setText("Please confirm the password")
            
            #if the password is correct
            if self.pass_old == pass_new:
                
                #create new database with provided password
                db.init_db(pass_new)
                self.instruction_label.setText("Passwords is correct")
                
                #pass data to main window
                self.masterpassword = pass_new
                self.hasAcess = True
                
                #emit a signal for piping to main window
                self.login_successful.emit(self.db, self.masterpassword, self.hasAcess) 
            
            #if this was the first entry                     
            elif not self.pass_old:
                self.pass_old = pass_new
            #must have been atleast the 2nd try and passwords did not match
            else:
                self.instruction_label.setText("Passwords did not match, please try again")
                self.entry.clear()
                self.pass_old = None
                
        #if the password is wrong and too short (to avoid saying too short try again)
        elif self.pass_old:
            self.instruction_label.setText("Passwords did not match, please try again")
            self.entry.clear()
            self.pass_old = None
        #password is too short
        else:
            self.instruction_label.setText("Password is too short please try again")
            self.pass_old = None
            
              
#Debug        
# Main application loop
"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PublicArea()
    window.show()
    sys.exit(app.exec_())
"""
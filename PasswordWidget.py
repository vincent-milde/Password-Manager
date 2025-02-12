import sys
from PyQt5.QtWidgets import *        #QApplication, QMainWindow, QVBoxLayout, QWidget, QSplitter, QListWidget
from PyQt5.QtCore import *           # Qt
from PyQt5.QtGui import *

#placeholder for masterpassword

#Super weird custom password widget
class PasswordWidget(QWidget):
    def __init__(self):
        
        #Initillize main
        super().__init__()
        self.hasAcess = False
        
        #Initilazing layout for the Text field and the 2 buttons to show/hide and copy
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        #Label
        self.label = QLabel()
        self.label.setText("default:")
        layout.addWidget(self.label)
        
        #Text Area
        self.line_edit = QLineEdit()
        layout.addWidget(self.line_edit)
        
        #initillize lineEdit
        self.hidePassword()
        self.line_edit.setReadOnly(True)
                       
        #Button Area
        self.show_button = QPushButton()
        self.copy_button = QPushButton()     
        
        #initillize Buttons
        #show
        self.show_button.setText("Show")
        self.show_button.clicked.connect(self.showButtonClicked)       
        layout.addWidget(self.show_button)
        
        #copy
        self.copy_button.setText("Copy")
        self.copy_button.clicked.connect(self.copyButtonClicked)
        layout.addWidget(self.copy_button)
        
        #set password for the widget
        self.setPassword("password")
    
    def setLabel(self, str):
        self.label.setText(str)
    
    def setAccess(self,setBool):
        if setBool:
            self.hasAcess = True
        elif setBool:
            self.hasAcess = False
        else:
            Warning("Acess state undefined!")
            
    def toggleEditeable(self):
        if self.hasAcess:
            if self.line_edit.isReadOnly():
                self.line_edit.setReadOnly(False)
                self.showPassword()
            elif not self.line_edit.isReadOnly():
                self.line_edit.setReadOnly(True)
            else:
                Warning("Edit state undefined!")
            
    def setEditable(self, toggleBool):
        if self.hasAcess and self.password_is_Hidden == False:
            if toggleBool == True:
                self.line_edit.setReadOnly(False)
                self.showPassword()
            elif toggleBool == False:
                self.line_edit.setReadOnly(True)
            else:
                Warning("Edit state undefined!")
            
    def showButtonClicked(self):
        if self.hasAcess :
            if self.password_is_Hidden == True :
                self.showPassword()
            elif self.password_is_Hidden == False :
                self.hidePassword()
        else:
            self.hidePassword
            print("Access Denied")
            Warning("No Access but bypassed into GUI")
    
    def copyButtonClicked(self):
        if self.hasAcess :
            #Add logic to copy password to clipboard
            print("copy button clicked") 
        else:
            self.hidePassword()
            print("Access Denied")
            Warning("No Access but bypassed into GUI")
                   
    def setPassword(self, password):
        self.password = password
        self.line_edit.setText(password)    
    
    #returns the text of the line edit not the password variable!
    def getText(self):
        return self.line_edit.text()
        
    def hidePassword(self):
        self.line_edit.setEchoMode(QLineEdit.Password)
        self.password_is_Hidden = True
        
    def showPassword(self):
        if self.hasAcess:
            self.line_edit.setEchoMode(QLineEdit.Normal)
            self.password_is_Hidden = False
        else:
            print("Access Denied")
            Warning("No Access but tried to show password")
   
'''
#Debug


            
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Password GUI tester")
        self.setGeometry(100, 100, 800, 600)
        
        self.password_Widget = PasswordWidget()
        self.setCentralWidget(self.password_Widget)

# Main application loop
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
'''        
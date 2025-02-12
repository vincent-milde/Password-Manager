import sys
from PyQt5.QtWidgets import *        #QApplication, QMainWindow, QVBoxLayout, QWidget, QSplitter, QListWidget
from PyQt5.QtCore import *           # Qt
from PyQt5.QtGui import *
from PasswordWidget import PasswordWidget
from PasswordDataBase import PasswordDataBase
#placeholder for masterpassword

   
class PasswordArea(QMainWindow):
    
    def __init__(self, db, masterpassword, hasAcess):
        #Initiliaze main window
        super().__init__()
        
        #global variables
        self.db = db
        self.masterpassword = masterpassword
        self.hasAcess = hasAcess
        self.stored_domain = None
        self.stored_username = None
        self.stored_password = None
        self.edit_state = False
            
        self.setWindowTitle("PasswordArea")
        self.setGeometry(100, 100, 800, 600)
        
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
        
        #pack main widget
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout() 
        widget.setLayout(layout)
        
        #Split the Password manager in 2 Areas horizontally
        splitterH = QSplitter(Qt.Horizontal)
        layout.addWidget(splitterH)
        
        #Add left and right frame
        left = self.create_left_side()
        right = self.create_right_side()
        
        splitterH.addWidget(left)
        splitterH.addWidget(right)
        
    #Create the Frame etc for the Left side    
    def create_left_side(self):
        
        #Main Frame
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)
        layout = QVBoxLayout()
        frame.setLayout(layout)
        
        #Search Bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search...")
        layout.addWidget(search_bar)
        
        #List Widget
        self.list_widget = QListWidget()
        #add domains to the list widget
        self.list_add_items(self.list_widget)
        
        #connect the list widget to the password details (right side)
        self.list_widget.itemClicked.connect(self.password_details)
        
        #add custom policy for right click
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)

        layout.addWidget(self.list_widget)

        # Password Details Placeholder
        return frame

    
    #adds domains to the list widget
    def list_add_items(self, list_widget):
        db = self.db
        domains = db.get_domains()
        for domain in domains:
            list_widget.addItem(domain[0])
    
    #displays the password for the selected domain
    def password_details(self, domain):
        print(f"Selected Item: {domain.text()}")
        db = self.db
        # Get the username and password for the selected domain
        username, password = db.fetch_by_domain(domain.text())
        
        #update the passwordwidgets and domain label
        self.domain_label.setText(domain.text())
        self.username_widget.setPassword(username)
        self.password_widget.setPassword(password)     
        
        #hide the password and username
        self.username_widget.hidePassword()
        self.password_widget.hidePassword()
        
    #right click menu
    def show_context_menu(self, position):
        # Get the clicked item
        item = self.list_widget.itemAt(position)
        menu = QMenu()
        if item:  # Context menu only if an item was clicked

            
            # Add actions
            
            #delete action
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(lambda: self.delete_item(item))
            menu.addAction(delete_action)

            # Show the menu
            menu.exec_(self.list_widget.viewport().mapToGlobal(position))
        else: #doesnt have to be an item clicked
            # Add actions
            add_action = QAction("Add", self)
            add_action.triggered.connect(self.add_item)
            menu.addAction(add_action)
            
            # Show the menu
            menu.exec_(self.list_widget.viewport().mapToGlobal(position))

    def delete_item(self, item):
        # Confirm deletion
        reply = QMessageBox.question(
            self, "Delete File", f"Are you sure you want to delete '{item.text()}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.list_widget.takeItem(self.list_widget.row(item))
            self.db.delete_entry(item.text())
            
            
    #create a custom dialog for adding a password
    def add_item(self):
        self.dialog = QDialog()
        self.dialog.setGeometry(100,100,400,200)
        
        #style sheet
                #styling
        self.dialog.setStyleSheet("""
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
        
        # Create layout
        layout = QVBoxLayout()
        
        # Create fields and labels
        self.label_domain = QLabel("Domain")
        self.field_domain = QLineEdit()
        
        self.label_username = QLabel("Username")
        self.field_username = QLineEdit()
        
        self.label_password = QLabel("Password")
        self.field_password = QLineEdit()
        
        # Create button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.on_submit)
        
        # Add widgets to layout
        layout.addWidget(self.label_domain)
        layout.addWidget(self.field_domain)
        
        layout.addWidget(self.label_username)
        layout.addWidget(self.field_username)
        
        layout.addWidget(self.label_password)
        layout.addWidget(self.field_password)
        
        layout.addWidget(self.submit_button)
        
        self.dialog.setLayout(layout)
        self.dialog.exec()
    
    def on_submit(self):
        # Retrieve the values from the fields
        domain = self.field_domain.text()
        username = self.field_username.text()
        password = self.field_password.text()
        
        
        # Handle the submitted data
        self.db.add_entry(domain, username, password)
        
        #refresh the list widget
        self.list_widget.addItem(domain)
        
        # Close the dialog
        self.dialog.accept()
    
    
    #Create the Frame etc for the right side 
    def create_right_side(self):
        
        main_frame = QFrame()
        main_layout = QVBoxLayout(main_frame)
        
        #Frame 1 (Showcase of username password etc)
        frame1 = QFrame()
        layout_top = QVBoxLayout()
        frame1.setLayout(layout_top)
        
            #Domain Label Section
        domain_layout = QHBoxLayout()
        
                #Label
        self.domain_label = QLabel()
        self.domain_label.setText("Domain")
        
                #Edit Button
        self.edit_button = QPushButton()
        self.edit_button.setText("Edit")
        self.edit_button.setFixedSize(100, 30)
        self.edit_button.clicked.connect(self.edit_button_clicked)  # Correct signal connection
        
        #Add Widgets
        domain_layout.addWidget(self.domain_label)
        domain_layout.addWidget(self.edit_button)
        
        #Add Domain edit Section to top layout
        layout_top.addLayout(domain_layout)
            
    #username Section

        #Create Weird Readonly but also not read only Widget
        self.username_widget = PasswordWidget()
        self.username_widget.setLabel("username: ")
        self.username_widget.setPassword("Vincent")
        self.username_widget.setAccess(self.hasAcess)
        layout_top.addWidget(self.username_widget)

    #password Section
        self.password_widget = PasswordWidget()
        self.password_widget.setLabel("password: ")
        self.password_widget.setPassword("Milde")
        self.password_widget.setAccess(self.hasAcess)
        layout_top.addWidget(self.password_widget)
        
    #Frame 2 (Showcase of databreaches) ---  WIP
        frame2 = QFrame()
        
        #finilazing layout hiarchy
        main_layout.addWidget(frame1)
        main_layout.addWidget(frame2)        
        
        return main_frame
    
    #Has 2 States: edit button mode and confirm button mode:
    def edit_button_clicked(self):  
        
        #change from edit button mode to confirm button mode:
        if self.edit_state == False:
            #store old data
            self.stored_domain = self.domain_label.text()
            self.stored_username = self.username_widget.getText()
            self.stored_password = self.password_widget.getText()
            
            #change the button text
            self.edit_button.setText("Confirm")
            self.username_widget.toggleEditeable()
            self.password_widget.toggleEditeable() #only works if acces is set to true
            self.edit_state = True

        elif  self.edit_state == True:
            reply = QMessageBox.question(self, "Confirm Action", "Are you sure you want to change the password?", QMessageBox.Yes | QMessageBox.No)

            #if yes 
            if reply == QMessageBox.Yes and self.domain_label.text() == self.stored_domain:

                self.db.edit_data(self.stored_domain, self.username_widget.getText() , self.password_widget.getText())
                QMessageBox.information(self, "Success", "Password changed successfully!")

            #if domain is changed while editing    
            elif reply == QMessageBox.Yes and self.domain_label.text() != self.stored_domain:
                QMessageBox.warning(self, "Error", "Canceling change...")
                
            #if no
            else:
                #turn off editability
                self.username_widget.toggleEditeable()
                self.password_widget.toggleEditeable()

                #reset the passwordwidgets
                self.username_widget.setPassword(self.username_widget.getText())
                self.password_widget.setPassword(self.username_widget.getText())
            
            #change the button text
            self.edit_button.setText("Edit")
            self.username_widget.setEditable(False)
            self.password_widget.setEditable(False)
            self.edit_state = False
        else:
            Warning("Edit state undefined!")    
    
#Debug
'''

# Main application loop
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordArea()
    window.show()
    sys.exit(app.exec_())
'''
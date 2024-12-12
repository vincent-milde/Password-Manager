import sys
from PyQt5.QtWidgets import *        #QApplication, QMainWindow, QVBoxLayout, QWidget, QSplitter, QListWidget
from PyQt5.QtCore import *           # Qt
from PyQt5.QtGui import *

#placeholder for masterpassword
HasAcess = True

class PasswordArea(QMainWindow):
    def __init__(self):
        #Initiliaze main window
        super().__init__()

        self.setWindowTitle("PasswordArea")
        self.setGeometry(100, 100, 800, 600)
        
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
        
        splitterH.addWidget(left)
        
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
        search_bar
        layout.addWidget(search_bar)
        
        #List Widget
        list_widget = QListWidget()
        list_widget.addItems([f"Item {i}" for i in range(1, 11)])
        list_widget.itemClicked.connect(self.password_details)
        layout.addWidget(list_widget)

        # Password Details Placeholder
    
        return frame

    def password_details(self, item):
        print(f"Selected Item: {item.text()}")
    
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
        self.domain_label.setText("Placeholder")
        
        #Edit Button
        self.edit_button = QPushButton()
        self.edit_button.setText("Edit")
        self.edit_button.clicked.connect(self.edit_button_clicked)  # Correct signal connection



        
        
        layout_top.addWidget(self.domain_label)
    #username Section
        
    #password Section
        
        
    #Frame 2 (Showcase of databreaches) ---  WIP
        frame2 = QFrame()
        
        #finilazing layout hiarchy
        main_layout.addWidget(frame1)
        main_layout.addWidget(frame2)        

    def edit_button_clicked(self):  # Correct method name
            print("Edit button clicked!")


# Main application loop
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordArea()
    window.show()
    sys.exit(app.exec_())

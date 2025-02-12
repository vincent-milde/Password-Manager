import sys
from PyQt5.QtWidgets import *        
from PyQt5.QtCore import *           
from PyQt5.QtGui import *
from PasswordArea import PasswordArea
from PublicArea import PublicArea
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #main window size etc
        self.setWindowTitle("Layered GUI Example")
        self.setGeometry(100, 100, 800, 600)

        #global variables
        self.masterpassword = ""
        self.hasAcess = False
        self.db = None
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        

        # Stacked widget for multiple layers (public and private area)
        self.stacked_widget_area = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget_area)
        self.public_layer()
        
    def public_layer(self):
        #get public area widget
        public_area = PublicArea()
        self.stacked_widget_area.addWidget(public_area) 
        self.stacked_widget_area.setCurrentIndex(0)
        
        #retrieving data from password entry for future use and connect login event
        public_area.login_successful.connect(self.login_event_handler)
        
    def login_event_handler(self, db, masterpassword, hasAcess):
        
        #pass data from public area to main window
        self.db =  db
        self.masterpassword = masterpassword
        self.hasAcess = hasAcess
        
        #iniate private layer
        self.private_layer()
        self.stacked_widget_area.setCurrentIndex(1)
        
    def private_layer(self):  
        #frame for the private area
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)
        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)  
        self.stacked_widget_area.addWidget(frame)
        
        # Navigation bar (fixed buttons at the top)
        nav_bar = QHBoxLayout()

        # Set fixed height for the navigation bar
        self.nav_bar_container = QWidget()
        self.nav_bar_container.setLayout(nav_bar)
        self.nav_bar_container.setFixedHeight(50)  # Control the height here
        frame_layout.addWidget(self.nav_bar_container)

        # Add buttons to the navigation bar
        self.home_button = QPushButton("Home")
        self.settings_button = QPushButton("Settings")
        self.about_button = QPushButton("About")
        nav_bar.addWidget(self.home_button)
        nav_bar.addWidget(self.settings_button)
        nav_bar.addWidget(self.about_button)
        
        #Stacked widget for private area
        self.stacked_widget_private = QStackedWidget()
        frame_layout.addWidget(self.stacked_widget_private)
        
        # Add layers to the stacked widget
        self.add_home_layer()
        self.add_settings_layer()
        self.add_about_layer()

        # Connect buttons to layers
        self.home_button.clicked.connect(lambda: self.stacked_widget_private.setCurrentIndex(0))
        self.settings_button.clicked.connect(lambda: self.stacked_widget_private.setCurrentIndex(1))
        self.about_button.clicked.connect(lambda: self.stacked_widget_private.setCurrentIndex(2))

    def add_home_layer(self):
        home_layer = PasswordArea(self.db, self.masterpassword, self.hasAcess)

        self.stacked_widget_private.addWidget(home_layer)

    def add_settings_layer(self):
        settings_layer = QWidget()
        layout = QVBoxLayout(settings_layer)
        layout.addWidget(QPushButton("Settings Page"))
        self.stacked_widget_private.addWidget(settings_layer)

    def add_about_layer(self):
        about_layer = QWidget()
        layout = QVBoxLayout(about_layer)
        layout.addWidget(QPushButton("About Page"))
        self.stacked_widget_private.addWidget(about_layer)
    
# Main application loop
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

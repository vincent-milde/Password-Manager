import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QStackedWidget
from PyQt5.QtCore import Qt
from PasswordArea import PasswordArea
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Layered GUI Example")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Navigation bar (fixed buttons at the top)
        nav_bar = QHBoxLayout()

        # Set fixed height for the navigation bar
        self.nav_bar_container = QWidget()
        self.nav_bar_container.setLayout(nav_bar)
        self.nav_bar_container.setFixedHeight(50)  # Control the height here
        main_layout.addWidget(self.nav_bar_container)

        # Add buttons to the navigation bar
        self.home_button = QPushButton("Home")
        self.settings_button = QPushButton("Settings")
        self.about_button = QPushButton("About")
        nav_bar.addWidget(self.home_button)
        nav_bar.addWidget(self.settings_button)
        nav_bar.addWidget(self.about_button)

        # Stacked widget for dynamic content
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Add layers to the stacked widget
        self.add_home_layer()
        self.add_settings_layer()
        self.add_about_layer()

        # Connect buttons to layers
        self.home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.settings_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.about_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

    def add_home_layer(self):
        home_layer = PasswordArea()
        layout = QVBoxLayout(home_layer)
        layout.addWidget(QPushButton("Welcome to Home"))
        self.stacked_widget.addWidget(home_layer)

    def add_settings_layer(self):
        settings_layer = QWidget()
        layout = QVBoxLayout(settings_layer)
        layout.addWidget(QPushButton("Settings Page"))
        self.stacked_widget.addWidget(settings_layer)

    def add_about_layer(self):
        about_layer = QWidget()
        layout = QVBoxLayout(about_layer)
        layout.addWidget(QPushButton("About Page"))
        self.stacked_widget.addWidget(about_layer)

# Main application loop
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

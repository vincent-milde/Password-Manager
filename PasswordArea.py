import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QSplitter
from PyQt5.QtCore import Qt
class MainWindow(QMainWindow):
    def __init__(self):
        #Initiliaze main window
        super().__init__()

        self.setWindowTitle("PasswordArea")
        self.setGeometry(100, 100, 800, 600)
        
        #pack main widget
        P_Widget = QWidget()
        self.setCentralWidget(P_Widget)
        
        #Split the Password manager in 2 Areas horizontally
        splitterH = QSplitter(Qt.Horizontal)
        

# Main application loop
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

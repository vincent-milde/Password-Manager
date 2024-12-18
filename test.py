import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QMenu, QAction, QMessageBox
)
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QListWidget Right Click Menu")
        self.setGeometry(100, 100, 400, 300)

        # Initialize QListWidget
        self.list_widget = QListWidget()
        self.setCentralWidget(self.list_widget)

        # Add sample items
        for i in range(5):
            self.list_widget.addItem(f"File {i+1}")

        # Enable custom context menu
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        # Get the clicked item
        item = self.list_widget.itemAt(position)
        
        if item:  # Context menu only if an item was clicked
            menu = QMenu()

            # Add actions
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(lambda: self.delete_item(item))
            menu.addAction(delete_action)

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


# Main application loop
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

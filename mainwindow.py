from PyQt6.QtWidgets import QMainWindow, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hello, World!")
        button = QPushButton("Click")
        self.setCentralWidget(button)

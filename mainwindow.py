from PyQt6.QtWidgets import QDialog, QWidget, QPushButton, QStackedWidget


class MainWindow(QDialog):
    def __init__(self, widget: QStackedWidget):
        super().__init__()
        
        self.widget = widget
        self.button = QPushButton("To Screen 2", self)
        self.button.clicked.connect(lambda *args: self.widget.setCurrentIndex(self.widget.currentIndex() + 1))


class Screen2(QDialog):
    def __init__(self, widget: QStackedWidget):
        super().__init__()

        self.widget = widget
        self.button = QPushButton("To Screen 1", self)
        self.button.clicked.connect(lambda *args: self.widget.setCurrentIndex(self.widget.currentIndex() - 1))

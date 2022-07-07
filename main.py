from PyQt6.QtWidgets import QApplication, QStackedWidget
import sys

from mainwindow import MainWindow, Screen2


app = QApplication(sys.argv)

window = QStackedWidget()
mainwindow = MainWindow(window)
screen2 = Screen2(window)
window.addWidget(mainwindow)
window.addWidget(screen2)
window.show()

app.exec()

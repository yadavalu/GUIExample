from PyQt6.QtWidgets import QDialog, QWidget, QPushButton, QStackedWidget
from PyQt6 import QtCore
from PyQt6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtWidgets

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


class TransitionWidget(QtWidgets.QStackedWidget):
    _nextIndex = _nextWidget = None
    _orientation = QtCore.Qt.Horizontal

    def __init__(self):
        super().__init__()
        self._animation = QtCore.QVariantAnimation(
            startValue=0., endValue=1., duration=750)
        self._animation.valueChanged.connect(self._aniUpdate)
        self._animation.finished.connect(self._aniFinished)
        self._animation.setEasingCurve(QtCore.QEasingCurve.InOutExpo)

    def setDuration(self, duration):
        self._animation.setDuration(duration)

    def setCurve(self, curve):
        if isinstance(curve, QtCore.QEasingCurve):
            self._animation.setEasingCurve(curve)

    def setOrientation(self, orientation):
        self._orientation = orientation

    def getRange(self, prevIndex, nextIndex):
        rect = self.rect()
        currentStart = nextEnd = QtCore.QPoint()
        if self._orientation == QtCore.Qt.Horizontal:
            if prevIndex < nextIndex:
                currentEnd = QtCore.QPoint(-rect.width(), 0)
                nextStart = QtCore.QPoint(rect.width(), 0)
            else:
                currentEnd = QtCore.QPoint(rect.width(), 0)
                nextStart = QtCore.QPoint(-rect.width(), 0)
        else:
            if prevIndex < nextIndex:
                currentEnd = QtCore.QPoint(0, -rect.width())
                nextStart = QtCore.QPoint(0, rect.width())
            else:
                currentEnd = QtCore.QPoint(0, rect.width())
                nextStart = QtCore.QPoint(0, -rect.width())
        return currentStart, currentEnd, nextStart, nextEnd

    def setCurrentIndex(self, index):
        if index == self.currentIndex():
            return
        # prepare the next widget changes
        if self._nextWidget is not None:
            self._nextWidget.hide()
        self._nextIndex = index
        self._nextWidget = self.widget(index)
        self._nextWidget.show()
        rect = self.rect()
        rect.translate(self.rect().topRight())
        self._nextWidget.setGeometry(rect)
        self._nextWidget.raise_()
        self._animation.start()

    def _aniFinished(self):
        super().setCurrentIndex(self._nextIndex)
        self._nextIndex = self._nextWidget = None

    def _aniUpdate(self, value):
        if not self._animation.state():
            return
        currentStart, currentEnd, nextStart, nextEnd = self.getRange(self.currentIndex(), self._nextIndex)
        rect = self.rect()
        self.currentWidget().setGeometry(rect.translated(QtCore.QLineF(currentStart, currentEnd).pointAt(value).toPoint()))
        self._nextWidget.setGeometry(rect.translated(QtCore.QLineF(nextStart, nextEnd).pointAt(value).toPoint()))
        self.update()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWidget = QtWidgets.QWidget()
    mainLayout = QtWidgets.QHBoxLayout(mainWidget)
    transitionWidget = TransitionWidget()
    mainLayout.addWidget(transitionWidget)
    widgets = [
        QtWidgets.QCheckBox,
        QtWidgets.QComboBox,
        QtWidgets.QDateEdit,
        QtWidgets.QDateTimeEdit,
        QtWidgets.QDial,
        QtWidgets.QDoubleSpinBox,
        QtWidgets.QFontComboBox,
        QtWidgets.QLCDNumber,
        QtWidgets.QLabel,
        QtWidgets.QLineEdit,
        QtWidgets.QProgressBar,
        QtWidgets.QPushButton,
        QtWidgets.QRadioButton,
        QtWidgets.QSlider,
        QtWidgets.QSpinBox,
        QtWidgets.QTimeEdit,
    ]
    pageCount = len(widgets)
    for page in range(pageCount):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)
        pageLabel = QtWidgets.QLabel('Page {}'.format(page + 1))
        mainlayout = QtWidgets.QVBoxLayout(widget)
        mainlayout.addWidget(widgets[page]())
        mainlayout.addWidget(QtWidgets.QLabel("{str}".format(str=str(widgets[page]))[26:-2]))
        layout.addLayout(mainlayout, 0, 0, 1, 2)
        prevBtn = QtWidgets.QPushButton('Previous')
        if not page:
            prevBtn.setEnabled(False)
        layout.addWidget(prevBtn)
        nextBtn = QtWidgets.QPushButton('Next')
        layout.addWidget(nextBtn)
        if page == pageCount - 1:
            nextBtn.setEnabled(False)
        transitionWidget.addWidget(widget)
        prevBtn.clicked.connect(lambda *_, page=page: transitionWidget.setCurrentIndex(page - 1))
        nextBtn.clicked.connect(lambda *_, page=page: transitionWidget.setCurrentIndex(page + 1))
    mainWidget.show()
    sys.exit(app.exec())


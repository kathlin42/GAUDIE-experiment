import config

from PyQt5.QtWidgets import QWidget, QLabel, QSlider
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class Familiarity(QWidget):

    def __init__(self, app, width, height, enter_button):
        super().__init__()

        self.app = app
        self.width = width
        self.height = height

        self.enter_button = enter_button

        # Introduction text
        self.instrLabel = QLabel(app)
        self.instrLabel.setWordWrap(True)
        self.instrLabel.setText(config.familiarity_text)
        self.instrLabel.setStyleSheet("QLabel { color : white; }")
        self.instrLabel.setFont(QFont('Arial', 18))
        self.instrLabel.setAlignment(Qt.AlignCenter)

        # Slider widget
        self.slider = QSlider(Qt.Horizontal, app)
        self.slider.setTickInterval(1)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.valueChanged.connect(self.value_change)
        self.slider.hide()

        # Textfield label
        self.slider_val = QLabel(app)
        self.slider_val.setWordWrap(True)
        self.slider_val.setText("0")
        self.slider_val.setStyleSheet("QLabel { color : white; }")
        self.slider_val.setFont(QFont('Arial', 20))
        self.slider_val.setAlignment(Qt.AlignCenter)
        self.slider_val.hide()

    def value_change(self):
        self.enter_button.show()
        self.slider_val.setText(str(self.slider.value()))

    def get_vals(self):
        return self.slider.value()

    def hide_familiarity(self):
        self.instrLabel.hide()
        self.slider.setValue(0)
        self.enter_button.hide()
        self.slider.hide()
        self.slider_val.hide()

    def show_familiarity(self):
        self.slider_val.setText("0")

        self.instrLabel.show()
        self.slider.show()
        self.slider_val.show()

    def do_resize(self, width, height):
        self.width = width
        self.height = height

        self.instrLabel.setGeometry(int(self.width / 2 - 400), int(self.height * 0.3 - 150),
                                    800, 300)

        self.enter_button.setGeometry(int(self.width / 2 - 125), int(self.height * 0.7 - 50), 250, 100)

        self.slider.setGeometry(int(self.width / 2 - 400), int(self.height * 0.5 - 25),
                                800, 50)

        self.slider_val.setGeometry(int(self.width / 2 - 25), int(self.height * 0.55 - 25), 50, 50)

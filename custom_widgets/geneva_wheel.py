import config

from PyQt5.QtWidgets import QWidget, QLabel, QSlider, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class GenevaWheel(QWidget):

    def __init__(self, app, width, height, enter_button):
        super().__init__()

        self.app = app
        self.width = width
        self.height = height

        self.enter_button = enter_button

        self.buttons = []
        self.button_stats = []

        for i, item in enumerate(config.geneva_wheel_items):

            button = QPushButton(item, app)
            button.setStyleSheet("QPushButton { color : white; background-color: grey;}")
            button.setFont(QFont('Arial', 18))
            button.clicked.connect(lambda param, item=item, it=i: self.on_click(item, it))
            button.show()
            self.buttons.append(button)
            self.button_stats.append(False)

        # Introduction text
        self.instrLabel = QLabel(app)
        self.instrLabel.setWordWrap(True)
        self.instrLabel.setText(config.geneva_text)
        self.instrLabel.setStyleSheet("QLabel { color : white; }")
        self.instrLabel.setFont(QFont('Arial', 18))
        self.instrLabel.setAlignment(Qt.AlignCenter)

        # Slider widget
        self.slider = QSlider(Qt.Horizontal, app)
        self.slider.setTickInterval(1)
        self.slider.setMinimum(1)
        self.slider.setMaximum(6)
        self.slider.valueChanged.connect(self.value_change)
        self.slider.hide()

        # Textfield label
        self.slider_val = QLabel(app)
        self.slider_val.setWordWrap(True)
        self.slider_val.setText("1")
        self.slider_val.setStyleSheet("QLabel { color : white; }")
        self.slider_val.setFont(QFont('Arial', 20))
        self.slider_val.setAlignment(Qt.AlignCenter)
        self.slider_val.hide()

        self.clicked_item = None
        self.active_buttons = []

    def on_click(self, item, it):
        self.clicked_item = item

        if self.button_stats[it]:
            self.button_stats[it] = False
            self.active_buttons.append(it)

            self.slider.hide()
            self.enter_button.hide()
            self.slider_val.hide()

            self.buttons[it].setStyleSheet("QPushButton { color : white; background-color: grey;}")
        else:
            if len(self.active_buttons) > 0:
                self.deactivate_all_buttons()

            self.button_stats[it] = True
            self.active_buttons.append(it)

            self.slider.show()
            self.slider_val.show()
            self.enter_button.show()

            self.buttons[it].setStyleSheet("QPushButton { color : white; background-color: orange;}")

    def value_change(self):
        self.slider_val.setText(str(self.slider.value()))

    def deactivate_all_buttons(self):
        for i in self.active_buttons:
            self.buttons[i].setStyleSheet("QPushButton { color : white; background-color: grey;}")
            self.button_stats[i] = False
        self.active_buttons[:] = []

    def get_vals(self):
        return [self.clicked_item, self.slider.value()]

    def hide_wheel(self):
        self.instrLabel.hide()
        self.enter_button.hide()
        self.slider.hide()
        self.slider_val.hide()

        for button in self.buttons:
            button.hide()

        self.deactivate_all_buttons()

    def show_wheel(self):
        self.slider_val.setText("1")
        self.slider.setValue(1)

        self.instrLabel.show()

        for button in self.buttons:
            button.show()

    def do_resize(self, width, height):
        self.width = width
        self.height = height

        d = [0, 1, 2.5, 3.5, 3.8, 4, 4, 3.8, 3.5, 2.5, 1]
        sign = -1

        j = 1
        for i, item in enumerate(self.buttons):
            w_pos = (self.width / 2) + (sign * self.width / 2 * 0.15 * d[j])
            item.setGeometry(int(w_pos - 125), int(self.height * 0.09 * j - 40), 250, 80)

            if i % 2 == 1:
                j += 1

            sign = sign * -1

        self.instrLabel.setGeometry(int(self.width / 2 - 400), int(self.height * 0.5 - 150),
                                    800, 300)

        self.enter_button.setGeometry(int(self.width / 2 - 125), int(self.height * 0.7 - 50), 250, 100)

        self.slider.setGeometry(int(self.width / 2 - 150), int(self.height * 0.3 - 25),
                                300, 50)

        self.slider_val.setGeometry(int(self.width / 2 - 25), int(self.height * 0.35 - 25), 50, 50)

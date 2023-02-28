import config

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class EmotionCheckBox(QWidget):

    def __init__(self, app, width, height, enter_button):
        super().__init__()

        self.app = app
        self.width = width
        self.height = height

        self.enter_button = enter_button

        self.buttons = []
        self.button_stats = []

        for i, item in enumerate(config.emotion_checkbox_items):

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
        self.instrLabel.setText(config.emotion_checkbox_text)
        self.instrLabel.setStyleSheet("QLabel { color : white; }")
        self.instrLabel.setFont(QFont('Arial', 18))
        self.instrLabel.setAlignment(Qt.AlignCenter)

        self.clicked_item = None
        self.active_buttons = []

    def on_click(self, item, it):
        self.clicked_item = item

        if self.button_stats[it]:
            self.button_stats[it] = False
            self.active_buttons.append(it)

            self.enter_button.hide()

            self.buttons[it].setStyleSheet("QPushButton { color : white; background-color: grey;}")
        else:
            if len(self.active_buttons) > 0:
                self.deactivate_all_buttons()

            self.button_stats[it] = True
            self.active_buttons.append(it)

            self.enter_button.show()

            self.buttons[it].setStyleSheet("QPushButton { color : white; background-color: orange;}")

    def deactivate_all_buttons(self):
        for i in self.active_buttons:
            self.buttons[i].setStyleSheet("QPushButton { color : white; background-color: grey;}")
            self.button_stats[i] = False
        self.active_buttons[:] = []

    def hide_emotion(self):
        self.instrLabel.hide()
        self.enter_button.hide()

        for button in self.buttons:
            button.hide()

        self.deactivate_all_buttons()

    def show_emotion(self):
        self.instrLabel.show()

        for button in self.buttons:
            button.show()

    def get_vals(self):
        return self.clicked_item

    def do_resize(self, width, height):
        self.width = width
        self.height = height

        j = 0
        k = [-300, 0, 300]
        for i, item in enumerate(self.buttons):
            w_pos = (self.width / 2) + k[i % 3]
            item.setGeometry(int(w_pos - 125), int(self.height * 0.4 + j - 40), 250, 80)

            if i == 2:
                j = 100

        self.instrLabel.setGeometry(int(self.width / 2 - 400), int(self.height * 0.2 - 150),
                                    800, 300)

        self.enter_button.setGeometry(int(self.width / 2 - 125), int(self.height * 0.7 - 50), 250, 100)



import sys
import os
import random
import config

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSlider, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QUrl, QTimer, pyqtSlot
from PyQt5 import QtMultimedia

import csv

from custom_widgets import GenevaWheel
from custom_widgets import EmotionCheckBox
from custom_widgets import Familiarity


class App(QWidget):

    def __init__(self, audio_list, test_audio_list, sam_types):
        super().__init__()

        # Initialize object list ------------------------------------------------
        self.audioList = None  # Can be either self.trueAudioList or self.testAudioList depending Test Run or Real Run
        self.trueAudioList = audio_list  # Audio list for real experiment
        self.testAudioList = test_audio_list  # Audio test run

        # List strings with SAM image file names in that order Valence, Arousal, Dominance
        self.samTypes = ['', '', '']
        for sam in sam_types:
            if 'Arousal' in sam:
                self.samTypes[1] = sam
            if 'Dominance' in sam:
                self.samTypes[2] = sam
            if 'Valence' in sam:
                self.samTypes[0] = sam
        # self.samList = []

        # Set GUI window variables ----------------------------------------------
        self.setStyleSheet("background-color: black;")
        self.title = 'Experiment'
        self.left = 100
        self.top = 100
        self.width = 1920
        self.height = 1080

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Initialize Widgets and objects -----------------------------------------
        # Image widget
        self.imgLabel = QLabel(self)
        pixmap = QPixmap('res/SAM/SAM_Arousal.png')
        self.img_width = pixmap.width()
        self.img_height = pixmap.height()
        self.imgLabel.setPixmap(pixmap)
        self.imgLabel.hide()

        # Slider widget
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setTickInterval(1)
        self.slider.setMinimum(0)
        self.slider.setValue(50)
        self.slider.setMaximum(100)
        self.slider.hide()

        # Textfield label
        self.textLabel = QLabel(self)
        self.textLabel.setWordWrap(True)
        self.textLabel.setText("Some Instructions")
        self.textLabel.setStyleSheet("QLabel { color : white; }")
        self.textLabel.setFont(QFont('Arial', 20))
        self.textLabel.setAlignment(Qt.AlignCenter)
        self.textLabel.hide()

        # Introduction text
        self.introLabel = QLabel(self)
        self.introLabel.setWordWrap(True)
        self.introLabel.setText(config.intro_text)
        self.introLabel.setStyleSheet("QLabel { color : white; }")
        self.introLabel.setFont(QFont('Arial', 16))
        # self.introLabel.setAlignment(Qt.AlignCenter)
        self.introLabel.hide()

        # Countdown_text
        self.cntLabel = QLabel(self)
        self.cntLabel.setText("12")
        self.cntLabel.setStyleSheet("QLabel { color : white; }")
        self.cntLabel.setFont(QFont('Arial', 30))
        self.cntLabel.setAlignment(Qt.AlignCenter)
        self.cntLabel.hide()

        # Experiment Button - Starts the real experiment
        self.experiment_button = QPushButton("Start Experiment", self)
        self.experiment_button.setStyleSheet("QPushButton { color : white; background-color: grey;}")
        self.experiment_button.setFont(QFont('Arial', 30))
        self.experiment_button.clicked.connect(self.on_click_experiment)
        # self.experiment_button.hide()

        # Test Button - Starts a test run
        self.test_button = QPushButton("Start Test", self)
        self.test_button.setStyleSheet("QPushButton { color : white; background-color: grey;}")
        self.test_button.setFont(QFont('Arial', 30))
        self.test_button.clicked.connect(self.on_click_test)
        # self.test_button.hide()

        # Continue Button - displayed in the introduction screen. After clicking, the run starts
        self.continue_button = QPushButton("Starten", self)
        self.continue_button.setStyleSheet("QPushButton { color : white; background-color: grey;}")
        self.continue_button.setFont(QFont('Arial', 25))
        self.continue_button.clicked.connect(self.on_click_continue)
        self.continue_button.hide()

        # Geneva Wheel Button
        self.geneva_button = QPushButton("Bestätigen", self)
        self.geneva_button.setStyleSheet("QPushButton { color : white; background-color: grey;}")
        self.geneva_button.setFont(QFont('Arial', 25))
        self.geneva_button.clicked.connect(self.on_click_geneva)
        self.geneva_button.hide()

        # Audio Play button
        self.play_button = QPushButton("Audio abspielen", self)
        self.play_button.setStyleSheet("QPushButton { color : white; background-color: grey;}")
        self.play_button.setFont(QFont('Arial', 25))
        self.play_button.clicked.connect(self.on_click_play_audio)
        self.play_button.hide()

        # Emotion Checkbox Button
        self.emotion_button = QPushButton("Bestätigen", self)
        self.emotion_button.setStyleSheet("QPushButton { color : white; background-color: grey;}")
        self.emotion_button.setFont(QFont('Arial', 25))
        self.emotion_button.clicked.connect(self.on_click_emotion)
        self.emotion_button.hide()

        # Familiarity Button
        self.familiarity_button = QPushButton("Bestätigen", self)
        self.familiarity_button.setStyleSheet("QPushButton { color : white; background-color: grey;}")
        self.familiarity_button.setFont(QFont('Arial', 25))
        self.familiarity_button.clicked.connect(self.on_click_familiarity)
        self.familiarity_button.hide()

        # Dominance Button
        self.dominance_button = QPushButton("Bestätigen", self)
        self.dominance_button.setStyleSheet("QPushButton { color : white; background-color: grey;}")
        self.dominance_button.setFont(QFont('Arial', 25))
        self.dominance_button.clicked.connect(self.on_click_dominance)
        self.dominance_button.hide()

        # Audio Player
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setVolume(config.SOUND_VOL)
        self.player.stateChanged.connect(self.player_state_changed)

        # Countdown Timer
        self.cnt_timer = QTimer()
        self.cnt_timer.timeout.connect(self.timer_timeout)

        # Player Timer
        self.play_timer = QTimer()
        self.play_timer.timeout.connect(self.get_current_state)

        # Geneva wheel class object
        self.geneva_wheel = GenevaWheel(self, self.width, self.height, self.geneva_button)
        self.geneva_wheel.hide_wheel()

        # EmotionCheckbox class object
        self.emotion_checkbox = EmotionCheckBox(self, self.width, self.height, self.emotion_button)
        self.emotion_checkbox.hide_emotion()

        # EmotionCheckbox class object
        self.familiarity = Familiarity(self, self.width, self.height, self.familiarity_button)
        self.familiarity.hide_familiarity()

        self.resizeEvent(None)

        self.show()

        # Other variables --------------------------------------------------------
        self.time_left_int = 0  # Shows how much time is left since start of countdown

        self.playback_time = []  # Time series of the audio playback time
        self.slider_pos = []  # Time series of the slider position of the given playback time
        self.geneva_ratings = []
        self.emotion_ratings = []
        self.familiarity_ratings = []
        self.dominance_ratings = []
        self.audio_corr_list = []

        self.audio_index = 0  # Index of the current audio file in self.audioList
        self.sam_index = 0  # Index of the current sam file in self.samTypes

        self.subj_number = '000'  # Current subject number

        self.is_test = False  # True if test run was initiated

        # Dictionary contains instruction text for every SAM file
        self.instruction_text = {
            'SAM_Arousal.png': config.arousal_text,
            'SAM_Valence.png': config.valence_text,
            'SAM_Dominance.png': config.dominance_text
        }

    @pyqtSlot()
    def on_click_experiment(self):
        """
        On click event for self.button widget
        """
        # Create save folder if not exits already
        if not os.path.exists(config.save_dir):
            os.makedirs(config.save_dir)

        # Get file list and check what the last subj number was to determine the next subj number
        file_list = os.listdir(config.save_dir)
        self.subj_number = '000' if len(file_list) == 0 else str(int(file_list[-1]) + 1).zfill(3)
        os.makedirs(os.path.join(config.save_dir, self.subj_number))

        self.experiment_button.hide()
        self.test_button.hide()
        self.continue_button.show()
        self.introLabel.show()

        self.audioList = self.trueAudioList  # Set self.trueAudioList as the used audioList in this run

    @pyqtSlot()
    def on_click_test(self):
        """
        On click event for self.test_button widget
        """
        self.experiment_button.hide()
        self.test_button.hide()
        self.continue_button.show()
        self.introLabel.show()

        self.audioList = self.testAudioList
        self.is_test = True

    @pyqtSlot()
    def on_click_continue(self):
        """
        On Click event for self.continue_button widget
        """
        self.continue_button.hide()
        self.introLabel.hide()

        # Create randomise audioList and samList
        # self.randomise_sam_audio()

        # Shuffle audioList
        random.shuffle(self.audioList)

        self.start_counter(3)

    @pyqtSlot()
    def on_click_geneva(self):
        """
        On Click event for self.geneva_button widget
        """
        # Get geneva wheel data and resume experiment
        self.geneva_ratings.append(self.geneva_wheel.get_vals())
        self.geneva_wheel.hide_wheel()

        # Continue with emotion checkbox
        self.emotion_checkbox.show_emotion()

    @pyqtSlot()
    def on_click_emotion(self):
        """
        On Click event for self.emotion_button widget
        """
        # Get emotion checkbox data and resume experiment
        self.emotion_ratings.append(self.emotion_checkbox.get_vals())
        self.emotion_checkbox.hide_emotion()

        # Continue with familiarity rating
        self.familiarity.show_familiarity()

    @pyqtSlot()
    def on_click_familiarity(self):
        """
        On Click event for self.familiarity_button widget
        """
        # Get familiarity data and resume experiment
        self.familiarity_ratings.append(self.familiarity.get_vals())
        self.familiarity.hide_familiarity()

        # Continue with next audio
        # self.start_counter(3)
        self.start_run(self.samTypes[self.sam_index], self.audioList[self.audio_index])

    @pyqtSlot()
    def on_click_dominance(self):
        """
        On Click event for self.dominance_button widget
        """
        self.dominance_ratings.append(self.slider.value())

        self.audio_index += 1
        self.sam_index = 0

        if not self.is_test:
            self.save_ratings_csv()

        # If all audio files where played the experiment end, i.e. reset everything to default
        if self.audio_index >= len(self.audioList):
            self.reset_gui(show_button=True)
            self.audio_index = 0
            self.is_test = False
        else:
            self.reset_gui()
            self.start_counter(3)
            # self.start_run(self.samTypes[self.sam_index], self.audioList[self.audio_index])

    def start_counter(self, seconds):
        """
        Start counter at x seconds
        :param seconds: Counter time
        """
        self.cntLabel.show()
        self.cntLabel.setText(str(seconds))
        self.time_left_int = seconds
        self.cnt_timer.start(1000)

    def timer_timeout(self):
        """
        Is called in combination with self.cnt_timer.start(x) every x milliseconds.
        If self.time_left_int == 0, i.e Countdown ends, then start the run
        """
        self.time_left_int -= 1
        self.cntLabel.setText(str(self.time_left_int))
        if self.time_left_int == 0:
            self.cnt_timer.stop()
            self.cntLabel.hide()
            self.start_run(self.samTypes[self.sam_index], self.audioList[self.audio_index])

    def start_run(self, sam_file, audio_file, set_audio=True):
        """
        :param sam_file: list of sam images
        :param audio_file: list of audio files
        :param set_audio: If true, load audio file and set play button
        """
        print(audio_file)
        # Set sam image
        pixmap = QPixmap(os.path.join(config.sam_dir, sam_file))
        self.img_width = pixmap.width()
        self.img_height = pixmap.height()
        self.imgLabel.setPixmap(pixmap)
        self.imgLabel.setGeometry(int(self.width / 2 - self.img_width / 2),
                                  int(self.height * 0.3 - self.img_height / 2),
                                  self.img_width,
                                  self.img_height)

        # Set Instruction text
        self.textLabel.setText(self.instruction_text[sam_file])
        self.textLabel.show()

        # Set Audio
        if set_audio:
            audio_dir = config.audio_test_dir if self.is_test else config.audio_dir
            url = QUrl.fromLocalFile(os.path.join(audio_dir, audio_file))
            print(url)
            content = QtMultimedia.QMediaContent(url)
            self.player.setMedia(content)
            self.play_button.show()
        else:
            self.slider.show()
            self.imgLabel.show()
            self.dominance_button.show()

    @pyqtSlot()
    def on_click_play_audio(self):
        """
        On Click event for self.play_button widget
        """
        self.slider.show()
        self.imgLabel.show()
        self.player.play()
        self.play_button.hide()

    def player_state_changed(self, state):
        """
        This is basically an event handler, if the state of self.player changed
        :param state: State of the self.player 0: stopped, 1: playing, 2 paused
        """

        # If self.player started, start recording by starting the play_timer
        if state == 1 and not self.is_test:
            self.play_timer.start(int(1000 / config.SAMPLING_RATE))  # in milliseconds

        # If self.player stopped, i.e audio ends
        elif state == 0:

            if not self.is_test:
                self.play_timer.stop()
                self.save_playback_csv()  # Save currently recorded states

            if self.sam_index == 0:  # if valence
                # Iterate to SAM image
                self.sam_index += 1

                self.reset_gui()
                self.audio_corr_list.append(self.audioList[self.audio_index])

                # Start geneva, emotion, familiarty route
                self.geneva_wheel.show_wheel()

            else:  # if arousal

                self.reset_gui()
                self.start_run(self.samTypes[2], self.audioList[0], set_audio=False)

    def get_current_state(self):
        """
        Samples the current playback time of the media player (self.player) and current state of the slider.
        This is called in combination with self.play_timer.start(x) every x milliseconds
        """
        self.playback_time.append(self.player.position() / 1000)
        self.slider_pos.append(self.slider.value())

    def save_playback_csv(self):
        """
        Save self.playback_time and self.slider_pos values as .csv file
        """
        # Insert column names to time series
        self.playback_time.insert(0, 'playback_time')
        self.slider_pos.insert(0, 'slider_pos')

        # Create file name consisting of currently played audio file name and currently displayed SAM image file name
        file_name = os.path.join(config.save_dir, self.subj_number, '{}_{}.csv'.format(
            self.audioList[self.audio_index][:-4], self.samTypes[self.sam_index][:-4]))

        # Write values to csv
        with open(file_name, 'w', newline='', encoding='iso-8859-1') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(zip(self.playback_time, self.slider_pos))  # Concatenate both time series column wise

        print('playback:', self.audioList[self.audio_index], self.samTypes[self.sam_index], 'saved')

        # Empty time series lists
        self.playback_time[:] = []
        self.slider_pos[:] = []

    def save_ratings_csv(self):
        """
        Save ratings as .csv file
        """
        l = [['audio', 'geneva_wheel', 'geneva_slider', 'emotion', 'familiarity', 'dominance']]
        for i in range(len(self.audio_corr_list)):
            l.append([self.audio_corr_list[i],
                      self.geneva_ratings[i][0],
                      self.geneva_ratings[i][1],
                      self.emotion_ratings[i],
                      self.familiarity_ratings[i],
                      self.dominance_ratings[i]])

        file_name = os.path.join(config.save_dir, self.subj_number, 'ratings.csv')

        with open(file_name, 'a', newline='', encoding='iso-8859-1') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(l)

        print(file_name, 'saved')

        # Empty ratings
        self.audio_corr_list[:] = []
        self.familiarity_ratings[:] = []
        self.geneva_ratings[:] = []
        self.emotion_ratings[:] = []
        self.dominance_ratings[:] = []

    def reset_gui(self, show_button=False):
        """
        Reset GUI to default state, by hiding everything.
        :param show_button: boolean determines if button widgets should shown or not
        """
        self.imgLabel.hide()
        self.slider.setTickInterval(1)
        self.slider.setMinimum(0)
        self.slider.setValue(50)
        self.slider.setMaximum(100)
        self.slider.hide()
        self.textLabel.hide()
        self.cntLabel.hide()
        self.dominance_button.hide()
        if show_button:
            self.experiment_button.show()
            self.test_button.show()

    def resizeEvent(self, event):
        """
        Reposition widgets if windows gets resized
        :param event:
        """
        self.width = self.size().width()
        self.height = self.size().height()

        self.imgLabel.setGeometry(int(self.width / 2 - self.img_width / 2),
                                  int(self.height * 0.3 - self.img_height / 2), self.img_width, self.img_height)

        self.slider.setGeometry(int(self.width / 2 - self.img_width / 2), int(self.height * 0.5 - self.img_height / 2),
                                self.img_width, 50)

        self.textLabel.setGeometry(int(self.width / 2 - self.img_width / 2), int(self.height * 0.6 - 50),
                                   self.img_width, 200)

        self.cntLabel.setGeometry(int(self.width / 2 - 50), int(self.height * 0.8 - 50), 100, 100)

        self.experiment_button.setGeometry(int(self.width / 2 - 250), int(self.height * 0.3 - 100), 500, 200)

        self.test_button.setGeometry(int(self.width / 2 - 250), int(self.height * 0.6 - 100), 500, 200)

        self.introLabel.setGeometry(int(self.width / 2 - self.img_width / 2), int(self.height * 0.6 - 325),
                                    self.img_width, 650)

        self.continue_button.setGeometry(int(self.width / 2 - 125), int(self.height * 0.2 - 50), 250, 100)

        self.play_button.setGeometry(int(self.width / 2 - 175), int(self.height * 0.3 - 50), 350, 100)

        self.dominance_button.setGeometry(int(self.width / 2 - 175), int(self.height * 0.8 - 50), 350, 100)

        self.geneva_wheel.do_resize(self.width, self.height)
        self.emotion_checkbox.do_resize(self.width, self.height)
        self.familiarity.do_resize(self.width, self.height)

    def randomise_sam_audio(self):

        m_list = self.audioList * len(self.samTypes)

        if not self.is_test:
            # Shuffle audio list
            self.audioList = self.shuffle(m_list[:])
            while not self.audioList:
                self.audioList = self.shuffle(m_list[:])
        else:
            self.audioList = m_list

        sam = {
            self.samTypes[0]: [],
            self.samTypes[1]: [],
            self.samTypes[2]: []
        }

        r = [self.samTypes[1], self.samTypes[2]]

        for audio in self.audioList:
            random.shuffle(r)

            if audio not in sam[self.samTypes[0]]:
                self.samList.append(self.samTypes[0])
                sam[self.samTypes[0]].append(audio)
            elif audio not in sam[r[0]]:
                self.samList.append(r[0])
                sam[r[0]].append(audio)
            else:
                self.samList.append(r[1])
                sam[r[1]].append(audio)

    def shuffle(self, m_list):
        """
        Randomise list without repetition of values twice in a row
        :param m_list: audio list
        :return: shuffled audio list
        """
        val = random.choice(m_list)
        m_list.remove(val)
        result = [val]
        counter = 0
        for i in range(len(m_list)):
            val = random.choice(m_list)

            while val == result[-1]:
                val = random.choice(m_list)
                counter += 1

                if counter > len(m_list):
                    return False

            m_list.remove(val)
            result.append(val)

        return result


if __name__ == '__main__':
    audio_list = os.listdir(config.audio_dir)
    audio_test_list = os.listdir(config.audio_test_dir)
    sam_list = os.listdir(config.sam_dir)

    app = QApplication(sys.argv)
    ex = App(audio_list, audio_test_list, sam_list)
    sys.exit(app.exec_())

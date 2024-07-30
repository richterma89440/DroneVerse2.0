import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QRadioButton,
    QButtonGroup,
    QCheckBox,
    QComboBox,
)
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt5.QtCore import Qt


class UserInterface(QWidget):
    def __init__(self):
        super().__init__()

        self.chosen_detection = None
        self.chosen_control = None

        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Drone Control Interface")
        self.setGeometry(100, 100, 1920, 1080)  # Querformat Vollbild

        # Set background image
        self.set_background_image("images/DSC01497.jpg")

        main_layout = QVBoxLayout()

        # Set a larger font
        font = QFont()
        font.setPointSize(20)

        # DRONEVERSE Header
        header_label = QLabel("DRONEVERSE")
        header_label.setStyleSheet("color: white;")
        header_label.setFont(QFont("Arial", 80, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label, alignment=Qt.AlignTop)

        ## DETECTION METHODS
        detection_section = QVBoxLayout()
        detection_label = QLabel("How do you want to detect?")
        detection_label.setStyleSheet("color: white;")
        detection_label.setFont(font)
        detection_section.addWidget(detection_label)

        detection_methods_layout = QHBoxLayout()

        self.detection_group = QButtonGroup(self)

        # Gesture detection section
        gesture_section = QVBoxLayout()
        gesture_header = QLabel("Gesture detection")
        gesture_header.setStyleSheet("color: white;")
        gesture_header.setFont(QFont("Arial", 40, QFont.Bold))
        gesture_header.setAlignment(Qt.AlignLeft)
        gesture_section.addWidget(gesture_header)
        gesture_radio = QRadioButton("Gesture")
        gesture_radio.setStyleSheet("color: white;")
        gesture_radio.setFont(font)
        gesture_section.addWidget(gesture_radio)

        # Phone detection section
        phone_section = QVBoxLayout()
        phone_header = QLabel("OSC detection")
        phone_header.setStyleSheet("color: white;")
        phone_header.setFont(QFont("Arial", 40, QFont.Bold))
        phone_header.setAlignment(Qt.AlignLeft)
        phone_section.addWidget(phone_header)
        osc_radio = QRadioButton("OSC")
        osc_radio.setStyleSheet("color: white;")
        osc_radio.setFont(font)
        phone_section.addWidget(osc_radio)

        # Keyboard detection section
        keyboard_section = QVBoxLayout()
        keyboard_header = QLabel("Keyboard detection")
        keyboard_header.setStyleSheet("color: white;")
        keyboard_header.setFont(QFont("Arial", 40, QFont.Bold))
        keyboard_header.setAlignment(Qt.AlignLeft)
        keyboard_section.addWidget(keyboard_header)
        keyboard_radio = QRadioButton("Keyboard")
        keyboard_radio.setStyleSheet("color: white;")
        keyboard_radio.setFont(font)
        keyboard_section.addWidget(keyboard_radio)

        self.detection_group.addButton(gesture_radio)
        self.detection_group.addButton(osc_radio)
        self.detection_group.addButton(keyboard_radio)

        detection_methods_layout.addLayout(gesture_section)
        detection_methods_layout.addLayout(phone_section)
        detection_methods_layout.addLayout(keyboard_section)

        detection_section.addLayout(detection_methods_layout)

        ## GESTURES OPTIONS
        gestures_layout = QVBoxLayout()
        gestures_label = QLabel("Gestures Options:")
        gestures_label.setStyleSheet("color: white;")
        gestures_label.setFont(font)
        gestures_layout.addWidget(gestures_label)

        self.show_rois_checkbox = QCheckBox("Show Rois")
        self.show_rois_checkbox.setStyleSheet("color: white;")
        self.show_rois_checkbox.setFont(font)
        self.show_video_checkbox = QCheckBox("Show Video")
        self.show_video_checkbox.setStyleSheet("color: white;")
        self.show_video_checkbox.setFont(font)
        self.show_handskeleton_checkbox = QCheckBox("Show Handskeleton")
        self.show_handskeleton_checkbox.setStyleSheet("color: white;")
        self.show_handskeleton_checkbox.setFont(font)

        gestures_options_layout = QVBoxLayout()
        gestures_options_layout.addWidget(self.show_rois_checkbox)
        gestures_options_layout.addWidget(self.show_video_checkbox)
        gestures_options_layout.addWidget(self.show_handskeleton_checkbox)

        gestures_layout.addLayout(gestures_options_layout)
        gestures_layout.setContentsMargins(20, 0, 0, 0)  # Einrücken der Gesten-Optionen

        detection_section.addLayout(gestures_layout)

        main_layout.addLayout(detection_section)

        ## CONTROL METHODS
        control_section = QVBoxLayout()
        control_label = QLabel("What do you want to control?")
        control_label.setStyleSheet("color: white;")
        control_label.setFont(font)
        control_section.addWidget(control_label)

        control_methods_layout = QHBoxLayout()

        self.control_group = QButtonGroup(self)

        # Print controlled section
        print_section = QVBoxLayout()
        print_header = QLabel("Control Textoutputs")
        print_header.setStyleSheet("color: white;")
        print_header.setFont(QFont("Arial", 40, QFont.Bold))
        print_header.setAlignment(Qt.AlignLeft)
        print_section.addWidget(print_header)
        print_radio = QRadioButton("Print")
        print_radio.setStyleSheet("color: white;")
        print_radio.setFont(font)
        print_section.addWidget(print_radio)

        # Tello controlled section
        tello_section = QVBoxLayout()
        tello_header = QLabel("Control Tello Drone")
        tello_header.setStyleSheet("color: white;")
        tello_header.setFont(QFont("Arial", 40, QFont.Bold))
        tello_header.setAlignment(Qt.AlignLeft)
        tello_section.addWidget(tello_header)
        tello_radio = QRadioButton("Tello")
        tello_radio.setStyleSheet("color: white;")
        tello_radio.setFont(font)
        tello_section.addWidget(tello_radio)

        # Quadcopter controlled section
        quadcopter_section = QVBoxLayout()
        quadcopter_header = QLabel("Control Quadcopter Drone")
        quadcopter_header.setStyleSheet("color: white;")
        quadcopter_header.setFont(QFont("Arial", 40, QFont.Bold))
        quadcopter_header.setAlignment(Qt.AlignLeft)
        quadcopter_section.addWidget(quadcopter_header)
        quadcopter_radio = QRadioButton("Quadcopter")
        quadcopter_radio.setStyleSheet("color: white;")
        quadcopter_radio.setFont(font)
        quadcopter_section.addWidget(quadcopter_radio)

        self.control_group.addButton(print_radio)
        self.control_group.addButton(tello_radio)
        self.control_group.addButton(quadcopter_radio)

        control_methods_layout.addLayout(print_section)
        control_methods_layout.addLayout(tello_section)
        control_methods_layout.addLayout(quadcopter_section)

        control_section.addLayout(control_methods_layout)

        main_layout.addLayout(control_section)

        

        # Label und ComboBox für die Geschwindigkeitsauswahl
        speed_layout = QVBoxLayout()
        speed_layout.setSpacing(5)
        self.speed_label = QLabel("Wählen Sie den Schwierigkeitsgrad:")
        self.speed_label.setStyleSheet("color: white;")
        self.speed_label.setFont(QFont("Arial", 40, QFont.Bold))
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["Level 1", "Level 2", "Level 3"])
        self.speed_combo.currentIndexChanged.connect(self.update_speed)
        self.speed_combo.setFixedHeight(50)  # Set a fixed height for the combo box
        self.speed_combo.setFont(QFont("Arial", 30, QFont.Bold))

        speed_layout.addWidget(self.speed_label)
        speed_layout.addWidget(self.speed_combo)

        main_layout.addLayout(speed_layout)
        
        ## START BUTTONS
        buttons_layout = QHBoxLayout()
        start_button = QPushButton("Start")
        start_button.setFont(font)
        start_button.setFixedHeight(100)  # Set a fixed height for the button
        start_button.clicked.connect(self.start_clicked)
        quit_button = QPushButton("Quit program")
        quit_button.setFont(font)
        quit_button.setFixedHeight(100)  # Set a fixed height for the button
        quit_button.clicked.connect(self.quit_clicked)
        buttons_layout.addWidget(start_button)
        buttons_layout.addWidget(quit_button)

        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def update_speed(self):
        speed_level = self.speed_combo.currentIndex()
        if speed_level == 0:
            self.speed = 20
        elif speed_level == 1:
            self.speed = 30
        elif speed_level == 2:
            self.speed = 40
    
    def get_speed(self):     
        return self.speed
    
    def close_ui(self):
        self.close()
        
    def open_ui(self):
        self.show()
        
    def set_background_image(self, image_path):
        oImage = QPixmap(image_path)
        sImage = oImage.scaled(self.size(), Qt.IgnoreAspectRatio)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

    def start_clicked(self):
        detection_button = self.detection_group.checkedButton()
        control_button = self.control_group.checkedButton()

        if detection_button and control_button:
            self.chosen_detection = detection_button.text().lower()
            self.chosen_control = control_button.text().lower()
            self.close()
        else:
            error_dialog = QLabel("Please select both detection and control methods.")
            error_dialog.show()

    def quit_clicked(self):
        self.chosen_detection = None
        self.chosen_control = None
        QApplication.instance().quit()
        sys.exit(0)

def get_user_choices():
        app = QApplication(sys.argv)
        ui = UserInterface()
        ui.show()
        app.exec_()
        return ui.chosen_detection, ui.chosen_control


if __name__ == "__main__":
    chosen_detection, chosen_control = get_user_choices()
    if chosen_detection and chosen_control:
        print(f"Chosen Detection: {chosen_detection}")
        print(f"Chosen Control: {chosen_control}")
    else:
        print("Selection was not made properly.")

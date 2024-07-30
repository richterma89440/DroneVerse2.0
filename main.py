import logging
import sys
import time
from collections import defaultdict, Counter
from PyQt5.QtWidgets import QApplication
from threading import Thread
from gesturedetection import run_gesture_detection
from oscdetection import run_osc_detection
from keyboarddetection import run_keyboard_control
import userinterface

from collisiondetection import run_collision_detection, collision_status
from print_dronecontrol import PrintDroneController
from tello_dronecontrol import TelloDroneController
from quadcopter_dronecontrol import QuadcopterDroneController

chosen_detection = None
chosen_control = None
drone_controller = None

max_size_gestures = 15
max_size_osc = 300
max_size_keyboard = 1
directions_gestures = []
directions_osc = []
directions_keyboard = []

signal_counts = defaultdict(int)
last_output_time = time.time()
logging.basicConfig(
    format="%(asctime)s.%(msecs)03d - %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)


def filter_direction(directions, max_size):
    if len(directions) >= max_size:
        counter = Counter(directions)
        most_common_direction = counter.most_common(1)[0][0]
        directions.clear()
        return most_common_direction
    return None


def direction_from_gestures(direction):
    global signal_counts, last_output_time

    current_time, current_second = set_logging_info()

    directions_gestures.append(direction)
    filtered_direction = filter_direction(directions_gestures, max_size_gestures)
    if filtered_direction is not None:
        logging.info(
            f"{signal_counts[current_second]} Chosen Control: Gestures \t Direction from Control: {filtered_direction}"
        )
        send_direction_to_drone(filtered_direction)

    if current_time - last_output_time >= 60:
        last_output_time = current_time


def direction_from_osc(direction):
    global signal_counts, last_output_time

    current_time, current_second = set_logging_info()

    directions_osc.append(direction)
    filtered_direction = filter_direction(directions_osc, max_size_osc)
    if filtered_direction is not None:
        logging.info(
            f"{signal_counts[current_second]} Chosen Control: Phone \t Direction from Control: {direction}"
        )
        send_direction_to_drone(direction)

    if current_time - last_output_time >= 60:
        last_output_time = current_time


def direction_from_keyboard(direction):
    global signal_counts, last_output_time

    current_time, current_second = set_logging_info()

    directions_keyboard.append(direction)
    filtered_direction = filter_direction(directions_keyboard, max_size_keyboard)
    if filtered_direction is not None:
        logging.info(
            f"{signal_counts[current_second]} Chosen Control: Keyboard \t Direction from Control: {direction}"
        )
        send_direction_to_drone(direction)

    if current_time - last_output_time >= 60:
        last_output_time = current_time


def set_logging_info():
    current_time = time.time()
    current_second = int(current_time)
    signal_counts[current_second] += 1
    return current_time, current_second


def update_collision_status(status):
    global collision_status
    collision_status = status


def send_direction_to_drone(filtered_direction):
    global drone_controller
    if chosen_detection == "gesture" and chosen_control == "tello":
        drone_controller.speed_left_right = 0
        drone_controller.speed_up_down = 0
        drone_controller.speed_forward_back = 0
        drone_controller.yaw_speed = 0

    # Überprüfen Sie, ob eine Kollision in der gewünschten Richtung vorliegt
    if filtered_direction == "up":  # and not collision_status["up"]:
        drone_controller.up()
    elif filtered_direction == "down":  # and not collision_status["down"]:
        drone_controller.down()
    elif filtered_direction == "left" and not collision_status["left"]:
        drone_controller.left()
    elif filtered_direction == "right" and not collision_status["right"]:
        drone_controller.right()
    elif filtered_direction == "forward" and not collision_status["forward"]:
        drone_controller.forward()
    elif filtered_direction == "backward" and not collision_status["backward"]:
        drone_controller.backward()
    elif filtered_direction == "stop":
        drone_controller.stop()
    else:
        print(f"Invalid direction or collision detected: {filtered_direction}")


def start_user_interface():
    app = QApplication(sys.argv)
    ui = userinterface.UserInterface()
    ui.show()
    app.exec_()

def run_detection_and_control():
    global drone_controller
    if chosen_control == "tello":
        drone_controller = TelloDroneController()
    elif chosen_control == "quadcopter":
        drone_controller = QuadcopterDroneController()
    elif chosen_control == "print":
        drone_controller = PrintDroneController()
    else:
        print("Invalid control method.")
        return
    
    
    #app = QApplication(sys.argv)
    #app.exec_()
    #speed = userinterface.UserInterface().get_speed()  # Updated to call the method on an instance
    #drone_controller.set_speed(speed)
    
    if chosen_detection == "keyboard":
        run_keyboard_control(direction_from_keyboard)
    elif chosen_detection == "osc":
        run_osc_detection(direction_from_osc)
    elif chosen_detection == "gesture":
        run_gesture_detection(direction_from_gestures)
    else:
        print("Invalid detection method.")
        return

    run_collision_detection(update_collision_status)

if __name__ == "__main__":
    while True:
        chosen_detection, chosen_control = userinterface.get_user_choices()

        print(f"Chosen Detection: {chosen_detection}")
        print(f"Chosen Control: {chosen_control}")

        detection_thread = Thread(target=run_detection_and_control)
        detection_thread.start()
        detection_thread.join()
        
        if drone_controller:
            drone_controller.land()
        
        start_user_interface()
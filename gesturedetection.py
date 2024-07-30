# Sina Steinmüller
# Stand: 2024-07-26

import cv2
import mediapipe as mp
import math

# Initialisiere Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils  # Hand skeleton
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)


# Hauptfunktion zum Abrufen des Webcambildes und zur Erkennung der Handposition
def run_gesture_detection(direction_callback):
    # reset drone position
    # direction = "none"

    # testing boolean
    cap = cv2.VideoCapture(1)  # Öffne die Kamera
    _, frame = cap.read()  # Lese ein Frame von der Kamera

    # define rois
    height, width, roi_top, roi_bottom, roi_middle_left, roi_middle_right = define_rois(
        frame
    )

    while True:
        ret, frame = cap.read()  # Lese ein Frame von der Kamera
        if not ret:
            print("Fehler beim Abrufen des Bildes von der Kamera")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)  # Horizontal spiegeln
        results = hands.process(frame_rgb)

        # Zeichne die Regionen ein
        draw_rois(
            frame, height, width, roi_top, roi_bottom, roi_middle_left, roi_middle_right
        )

        direction = "stop"

        # Überprüfe, ob der Zeigefinger in der oberen, unteren oder mittleren Region liegt
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Spiegeln der x-Koordinaten der Landmarks, damit Skelett richtigrum ist
                for landmark in hand_landmarks.landmark:
                    landmark.x = 1.0 - landmark.x

                index_finger_tip = hand_landmarks.landmark[
                    mp_hands.HandLandmark.INDEX_FINGER_TIP
                ]

                finger_y = int(index_finger_tip.y * height)

                # Finger oben
                if finger_y < roi_top:
                    direction = "up"

                # Finger unten
                elif finger_y > roi_bottom:
                    direction = "down"

                else:
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    # Schwellwerte definieren
                    treshold_backward = 0.1
                    treshold_forward = 0.20

                    # Berechne die Distanz zwischen Daumen und Zeigefinger
                    distance = math.sqrt(
                        (index_finger_tip.x - thumb_tip.x) ** 2
                        + (index_finger_tip.y - thumb_tip.y) ** 2
                    )

                    if distance < treshold_backward:
                        direction = "backward"
                        print("ToDo update treshold! {distance}")

                    elif distance > treshold_forward:
                        direction = "forward"
                        print("ToDo update treshold! {distance}")

                    else:
                        if index_finger_tip.x < thumb_tip.x:
                            direction = "left"
                        elif index_finger_tip.x > thumb_tip.x:
                            direction = "right"
                        else:
                            direction = "stop"
                            print("Hand ist nicht ausgerichtet")

                # draw skeleton
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )
                direction_callback(direction)

        cv2.imshow("Frame", frame)  # Zeige das Frame mit OpenCV an
        key = cv2.waitKey(1)  # Warte auf eine Tastatureingabe (1 ms Timeout)

        # quit program
        if key & 0xFF == ord("q"):  # Beende die Schleife, wenn 'q' gedrückt wird
            break

    cap.release()  # Gib die Ressourcen frei
    cv2.destroyAllWindows()
    # return direction


def draw_rois(
    frame, height, width, roi_top, roi_bottom, roi_middle_left, roi_middle_right
):
    cv2.rectangle(
        frame,
        (roi_middle_left, roi_top),
        (roi_middle_right, roi_bottom),
        (0, 255, 0),
        2,
    )
    cv2.rectangle(frame, (0, 0), (width, roi_top), (255, 0, 0), 2)
    cv2.rectangle(frame, (0, roi_bottom), (width, height), (255, 0, 0), 2)


def define_rois(frame):
    height, width, _ = frame.shape
    roi_top = int(height / 4)
    roi_bottom = int(3 * height / 4)
    roi_middle_left = int(width / 4)
    roi_middle_right = int(3 * width / 4)
    return height, width, roi_top, roi_bottom, roi_middle_left, roi_middle_right


if __name__ == "__main__":
    # callback funktion, print hier wird überschrieben in main.py
    run_gesture_detection(lambda direction: print(f"gesturedetection.py {direction}"))

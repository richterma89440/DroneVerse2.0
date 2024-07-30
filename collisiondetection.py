import numpy as np
import cv2

collision_status = {"forward": False, "backward": False, "left": False, "right": False}


def crop_sides(image, crop_fraction):
    height, width = image.shape[:2]
    crop_width = int(width * crop_fraction)
    start_x = crop_width
    end_x = width - crop_width
    cropped_image = image[:, start_x:end_x]
    return cropped_image


def run_collision_detection(collision_callback):
    margin_size = 10
    cap = cv2.VideoCapture(0)
    old_frame = None

    while True:
        ret, frame = cap.read()
        cropped_frame = crop_sides(frame, 0.25)

        if ret:
            gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)

            if old_frame is not None:
                diff = cv2.absdiff(old_frame, gray)
                _, bin_diff = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY)
                cv2.imshow("diff_frame", bin_diff)

                top_margin = bin_diff[:margin_size, :]
                bottom_margin = bin_diff[-margin_size:, :]
                left_margin = bin_diff[:, :margin_size]
                right_margin = bin_diff[:, -margin_size:]

                collision_status["forward"] = np.any(top_margin == 255)
                collision_status["backward"] = np.any(bottom_margin == 255)
                collision_status["left"] = np.any(left_margin == 255)
                collision_status["right"] = np.any(right_margin == 255)

                if collision_status["forward"]:
                    print("Gefahrbereich vorne")
                if collision_status["backward"]:
                    print("Gefahrbereich hinten")
                if collision_status["left"]:
                    print("Gefahrbereich links")
                if collision_status["right"]:
                    print("Gefahrbereich rechts")

                if not any(collision_status.values()):
                    print("Sicherer Bereich")

                collision_callback(collision_status)

            old_frame = gray

            if cv2.waitKey(30) & 0xFF == ord("q"):
                break
        else:
            print("ERROR!")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_collision_detection(lambda status: print(f"collision_status: {status}"))

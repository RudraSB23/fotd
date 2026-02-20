import cv2
import os
import numpy as np

# From dark → light, tuned for better face detail
UTF8_CHARS = "█▓▒░▚▞▝▘▖▗▙▛▜▟⠁⠂⠄⠆⠒⠤⠦⠶⠷⠾⠿ "

def frame_to_ascii(frame, new_width=100):
    """Convert frame (OpenCV image) to ASCII art using UTF-8 characters."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Normalize brightness and smooth out noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

    height, width = gray.shape
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.65)  # slightly taller to preserve face shape
    resized = cv2.resize(gray, (new_width, new_height))

    # Map each pixel to a character
    ascii_art = ""
    num_chars = len(UTF8_CHARS) - 1
    for y in range(new_height):
        for x in range(new_width):
            pixel = int(resized[y, x])
            char_index = int((pixel / 255) * num_chars)
            ascii_art += UTF8_CHARS[char_index]
        ascii_art += "\n"

    return ascii_art


def echo_watch_event():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    folder = os.path.join(desktop, "LATTICE_SEES_YOU")
    os.makedirs(folder, exist_ok=True)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("⚠️  Lattice could not see you (camera not found).")
        return

    ret, frame = cap.read()
    cap.release()

    if ret:
        ascii_art = frame_to_ascii(frame, new_width=120)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(ascii_art)
        print("\n👁️  Lattice has seen you.\n")

        file_path = os.path.join(folder, "LATTICE_SEES_YOU.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(ascii_art)
    else:
        print("⚠️  Failed to capture image.")


if __name__ == "__main__":
    echo_watch_event()

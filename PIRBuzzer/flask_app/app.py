from flask import Flask, render_template
import json
import threading
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

alive = 0
data = {}

PIR_pin = 23
Buzzer_pin = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_pin, GPIO.IN)
GPIO.setup(Buzzer_pin, GPIO.OUT)


def main():
    motion_detection()


def motion_detection():
    data["alarm"] = False
    while True:
        if GPIO.input(PIR_pin):
            print("Motion detected")
            data["motion"] = 1
            beep(4)
        else:
            data["motion"] = 0
        if data["alarm"]:
            beep(2)
        time.sleep(1)


def beep(repeat):
    for i in range(0, repeat):
        for pulse in range(60):
            GPIO.output(Buzzer_pin, True)
            time.sleep(0.001)
            GPIO.output(Buzzer_pin, False)
            time.sleep(0.001)
        time.sleep(0.02)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/keep_alive")
def keep_alive():
    global alive, data
    alive += 1
    keep_alive_count = str(alive)
    data["keep_alive"] = keep_alive_count
    parsed_json = json.dumps(data)
    print(parsed_json)
    return str(parsed_json)


@app.route("/status=<name>-<action>", methods=["POST"])
def event(name, action):
    global data
    if name == "buzzer":
        if action == "on":
            data["alarm"] = True
        elif action == "off":
            data["alarm"] = False
    return str("Ok")


if __name__ == "__main__":
    sensorsThread = threading.Thread(target=motion_detection)
    sensorsThread.start()
    app.run(host="192.168.1.8", port="50000")

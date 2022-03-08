import RPi.GPIO as gpio
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
import time, cv2

app = Client("macchina", bot_token="token", api_id=1234567, api_hash="hash")

def init():    
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)

@app.on_message(filters.command("start"))
def start(app, message):
    app.send_message(message.chat.id, "Benvenuto nel mio fantastico bot per controllare la mia macchina.\nUtilizza i bottoni per comandarla", 
    reply_markup=ReplyKeyboardMarkup(
            [
                ["Avanti"],
                ["Sinistra", "Destra"],
                ["Indietro"]
                ["Foto"]
            ],
            resize_keyboard=True
        )
    )

@app.on_message(filters.regex("Avanti"))
def forward(app, message):
    init()
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(5)
    gpio.cleanup() 

@app.on_message(filters.regex("Destra"))
def left_turn(app, message):
    init()
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(0.4)
    gpio.cleanup()

@app.on_message(filters.regex("Sinistra"))
def right_turn(app, message):
    init()
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(0.4)
    gpio.cleanup()


@app.on_message(filters.regex("Indietro"))
def reverse(app, message):
    init()
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(3)
    gpio.cleanup()

@app.on_message(filters.regex("Foto"))
def foto(app, message):
    cam = cv2.VideoCapture(0)
    image = cam.read()
    if image:
        cv2.imwrite("foto.png", image)
    app.send_photo(message.chat.id, "foto.png")

app.run()
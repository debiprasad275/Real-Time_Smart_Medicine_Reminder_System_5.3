# ==============================
# IMPORTS
# ==============================

import sqlite3
import time
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

# GPIO
from gpiozero import AngularServo, OutputDevice

# OLED
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# DHT22
import Adafruit_DHT

# ==============================
# DATABASE
# ==============================

DB_NAME = "medicine.db"

def connect():
    return sqlite3.connect(DB_NAME)

def get_all_schedules():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM schedule")
    data = cursor.fetchall()
    conn.close()
    return data

def get_compartment(section_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM compartments WHERE section_id=?", (section_id,))
    data = cursor.fetchone()
    conn.close()
    return data

def log_intake(schedule_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO intake_log VALUES (NULL,?,?,?)",
        (schedule_id, datetime.now().strftime("%H:%M"), "taken")
    )
    conn.commit()
    conn.close()

# ==============================
# HARDWARE SETUP
# ==============================

# Servo (GPIO18 PWM)
servo = AngularServo(18, min_angle=0, max_angle=270)

# Pump (MOSFET via GPIO23)
pump = OutputDevice(23)

# Angles
S1_WATER = 90
S2_MED = 180
S3_MED = 270

# ==============================
# OLED SETUP
# ==============================

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

image = Image.new("1", (128, 64))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

def oled_display(text):
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0)
    draw.text((0, 10), text, font=font, fill=255)
    oled.image(image)
    oled.show()

# ==============================
# DHT22 SETUP
# ==============================

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

def show_temp_humidity():
    humidity, temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    if humidity and temp:
        msg = f"T:{temp:.1f}C H:{humidity:.1f}%"
        print(msg)
        oled_display(msg)

# ==============================
# HARDWARE FUNCTIONS
# ==============================

def move_servo(angle):
    print(f"Moving servo → {angle}")
    servo.angle = angle
    time.sleep(2)

def fill_water(water_ml):

    oled_display("Filling Water")

    move_servo(S1_WATER)

    pump.on()
    time.sleep(5)
    pump.off()

    print(f"{water_ml} ml filled")

def open_compartment(section_id):

    comp = get_compartment(section_id)

    if not comp:
        return

    angle = comp[3]
    medicine = comp[1]

    oled_display(f"Take {medicine}")

    move_servo(angle)
    time.sleep(3)

# ==============================
# AUDIO
# ==============================

def speak(text):
    os.system(f'espeak "{text}"')

# ==============================
# MAIN JOB
# ==============================

def medicine_job(schedule):

    schedule_id = schedule[0]
    section_id = schedule[1]
    water_ml = schedule[5]

    print("\n=== MEDICINE TIME ===")

    speak("Time to take medicine")

    # WATER
    fill_water(water_ml)

    time.sleep(2)

    # MEDICINE
    open_compartment(section_id)

    speak("Please take your medicine")

    time.sleep(45)

    # RETURN
    move_servo(S1_WATER)

    log_intake(schedule_id)

    oled_display("Done")

# ==============================
# SCHEDULER
# ==============================

scheduler = BackgroundScheduler()

def load_jobs():

    schedules = get_all_schedules()

    for s in schedules:

        hour, minute = map(int, s[2].split(":"))

        scheduler.add_job(
            medicine_job,
            'cron',
            hour=hour,
            minute=minute,
            args=[s],
            id=str(s[0]),
            replace_existing=True
        )

load_jobs()
scheduler.start()

# ==============================
# LOOP (SENSORS)
# ==============================

last_temp_time = time.time()

print("System Running")

while True:

    # Every 10 minutes → temp display
    if time.time() - last_temp_time > 600:
        show_temp_humidity()
        last_temp_time = time.time()

    time.sleep(5)
import speech_recognition as sr
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from time import sleep
import RPi.GPIO as GPIO
import os
import digitalio
import board
from adafruit_rgb_display import st7735

cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D24)
reset_pin = digitalio.DigitalInOut(board.D25)

BAUDRATE = 24000000

spi = board.SPI()

disp = st7735.ST7735R(spi, rotation=90, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE)

sleep(1)

height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height

image = Image.new("RGB", (width, height))

draw = ImageDraw.Draw(image)
disp.image(image)

draw.rectangle([(5, 5), (75, 59)], fill="#0000ff")
draw.rectangle([(85, 5), (155, 59)], fill="#0000ff")
draw.rectangle([(5, 69), (75, 123)], fill="#0000ff")
draw.rectangle([(85, 69), (155, 123)], fill="#0000ff")

draw.text((5, 5), "Bathroom", fill ="white", align ="center") 
draw.text((85, 5), "Kitchen", fill ="white", align ="center") 
draw.text((5, 69), "Bedroom", fill ="white", align ="center") 
draw.text((85, 69), "Living room", fill ="white", align ="center") 

disp.image(image)

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(4,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)

GPIO.output(17,GPIO.LOW)
GPIO.output(3,GPIO.LOW)
GPIO.output(4,GPIO.LOW)
GPIO.output(18,GPIO.LOW)

os.system("espeak 'Hello! I am your voice assistant, raspistant!'")

def speak(txt):
  os.system("espeak \"" + txt + "\"")

light1 = False
light2 = False
light3 = False
light4 = False

while True:
    try:
      with mic as source:
        audio = r.listen(source)
      words = r.recognize_google(audio)
      print("I heard:")
      print(words)
      if "turn on the bedroom light" in words or "turn on the bed room light" in words:
        speak("Ok, bedroom Light is on")
        light1 = True
      elif "turn on the bathroom light" in words or "turn on the bath room light" in words:
        light2 = True
        speak("Ok, bathroom Light is on")
      elif "turn on the kitchen light" in words:
        light3 = True
        speak("Ok, kitchen Light is on")
      elif "turn on the living room light" in words or "turn on the livingroom light" in words:
        light4 = True
        speak("Ok, living room Light is on")
      elif "turn on all the light" in words:
        light1 = True
        light2 = True
        light3 = True
        light4 = True
        speak("Ok, all the lights are on")
        
      if "turn off the bedroom light" in words or "turn off the bed room light" in words:
        speak("Ok, bedroom Light is off")
        light1 = False
      elif "turn off the bathroom light" in words or "turn off the bath room light" in words:
        light2 = False
        speak("Ok, bathroom Light is off")
      elif "turn off the kitchen light" in words:
        light3 = False
        speak("Ok, kitchen Light is off")
      elif "turn off the living room light" in words or "turn off the livingroom light" in words:
        light4 = False
        speak("Ok, living room Light is off")
      elif "turn off all the light" in words:
        light1 = False
        light2 = False
        light3 = False
        light4 = False
        speak("Ok, all the lights are off")

      GPIO.output(17, GPIO.HIGH if light1 == True else GPIO.LOW)
      GPIO.output(3, GPIO.HIGH if light2 == True else GPIO.LOW)
      GPIO.output(4, GPIO.HIGH if light3 == True else GPIO.LOW)
      GPIO.output(18, GPIO.HIGH if light4 == True else GPIO.LOW)
      
      draw.rectangle([(5, 5), (75, 59)], fill= "#0000ff" if light2 == False else "#00ff00")
      draw.rectangle([(85, 5), (155, 59)], fill= "#0000ff" if light3 == False else "#00ff00")
      draw.rectangle([(5, 69), (75, 123)], fill= "#0000ff" if light1 == False else "#00ff00")
      draw.rectangle([(85, 69), (155, 123)], fill= "#0000ff" if light4 == False else "#00ff00")
      
      draw.text((5, 5), "Bathroom", fill ="white", align ="center") 
      draw.text((85, 5), "Kitchen", fill ="white", align ="center") 
      draw.text((5, 69), "Bedroom", fill ="white", align ="center") 
      draw.text((85, 69), "Living room", fill ="white", align ="center") 
      
      disp.image(image)
    except KeyboardInterrupt:
        exit(0)
    except:
      continue

from gpiozero import LED, Button
from datetime import datetime
import time
from signal import pause
from picamera import PiCamera

indicator = LED(17)
button = Button(15)
camera = PiCamera()
camera.resolution = (4056, 3040)
previewRes = (1280, 720)

def capture_image():
    indicator.on()
    timenow = datetime.now()
    filename = "/home/pi/piCam/capture-%02d%02d%02d%04d.jpg" % (timenow.hour, timenow.minute, timenow.second, timenow.microsecond)
    camera.capture("%s" %filename)
    print("Captured %s" % filename)
    time.sleep(0.1)
    indicator.off()
    camera.start_preview(resolution=previewRes)
# add folder creation if doesn't exist

def exit_handler():
    for x in range(0,3):
        indicator.on()
        time.sleep(0.1)
        indicator.off()
        time.sleep(0.1)
    camera.stop_preview()
    
button.when_held = exit_handler
button.when_pressed = capture_image
camera.start_preview(resolution=previewRes)

pause()
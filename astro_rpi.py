from gpiozero import LED, Button
from datetime import datetime
import time
from signal import pause
from picamera import PiCamera
from os import system

indicator = LED(17)
#button = Button(15)
camera = PiCamera()
camera.resolution = (4056, 3040)
previewRes = (1024, 768)
run = True
preview_on = False

def capture_image():
    indicator.on()
    timenow = datetime.now()
    filename = "/home/pi/piCam/capture-%02d%02d%02d%04d.jpg" % (timenow.hour, timenow.minute, timenow.second, timenow.microsecond)
    camera.capture("%s" %filename)
    print("Captured %s" % filename)
    #time.sleep(0.1)
    indicator.off()
# add folder creation if doesn't exist

def capture_vid():
    indicator.on()
    timenow = datetime.now()
    filename = "/home/pi/piCam/capture-%02d%02d%02d%04d.h264" % (timenow.hour, timenow.minute, timenow.second, timenow.microsecond)
    camera.start_recording("%s" %filename)
    camera.wait_recording(30)
    camera.stop_recording
    print("Captured %s" % filename)
    #time.sleep(0.1)
    indicator.off()
    
while run == True:
    print('Options')
    print('1    Toggle preview')
    print('2    Single image capture')
    print('3    10x burst image capture')
    print('4    30s video capture')
    print('0    Exit')
    print('\n')
    input_var = int(input('Enter an option: '))

    if input_var == 1:
        if preview_on == False:
            camera.start_preview(resolution=previewRes)
            preview_on = True
        else:
            camera.stop_preview()
            preview_on = False
    elif input_var == 2:
        capture_image()
    elif input_var == 3:
        for x in range(0,9):
            capture_image()
    elif input_var == 4:
        print('Video recording begin...')
        camera.resolution = (1920, 1080)
        capture_vid()
        print('Video recording end')
    elif input_var == 0:
        run = False
        exit
    else:
        #system('clear')
        print(' ')
        print('=============')
        print('Invalid input')
        print('=============')

"""
######################################################################

 █████╗ ███████╗████████╗██████╗  ██████╗         ██████╗ ██████╗ ██╗
██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗        ██╔══██╗██╔══██╗██║
███████║███████╗   ██║   ██████╔╝██║   ██║        ██████╔╝██████╔╝██║
██╔══██║╚════██║   ██║   ██╔══██╗██║   ██║        ██╔══██╗██╔═══╝ ██║
██║  ██║███████║   ██║   ██║  ██║╚██████╔╝███████╗██║  ██║██║     ██║
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
                                                                     
                        By Jared Kizer

Utilize the Raspberry Pi and High Quality Camera for astrophotography

Currently only tested with solar system objects, this program offers
basic camera configuration as well as image capture and preview to
hone in on solar objects. 
######################################################################
"""
import time
import os
from datetime import datetime
from signal import pause
from picamera import PiCamera
import math
from os import system

# program setup
camera = PiCamera()
default_res = (4056, 3040)
default_framerate = 60
default_shuttersp = 16666
default_iso = 400
camera.resolution = default_res
camera.framerate = default_framerate
camera.shutter_speed = default_shuttersp
camera.iso = default_iso
working_folder = "/home/pi/astro_rpi"
#Check if save director exists and create it if necessary
if not os.path.exists(working_folder):
    os.makedirs(working_folder)

#main program loop
def main():
    preview_on = False
    run = True
    previewRes = (1024, 768)
    system('clear')    
    while run == True:
        print('==========================')
        print('Astro_RPI Home')
        print('1    Toggle fast tracking preview')
        print('2    Toggle image preview')
        print('3    Configure settings')
        print('4    Single image capture')
        print('\n')
        print('0    Exit')
        print('\n')
        input_var = int(input('Enter an option: '))

        if input_var == 1:
            if preview_on == False: 
                set_defaults()
                camera.start_preview(resolution=previewRes)
                preview_on = True
                system('clear')
            else: 
                camera.stop_preview()
                preview_on = False
                system('clear')
        elif input_var == 2:
            if preview_on == False:
                camera.start_preview(resolution=previewRes)
                preview_on = True
                system('clear')
            else:
                camera.stop_preview()
                preview_on = False
                system('clear')
        elif input_var == 3:
            configure_settings()
        elif input_var == 4:
            system('clear')
            capture_image()
        elif input_var == 0:
            run = False
            exit
        else:
            print('=============')
            print('Invalid input')
            print('=============')

def capture_image():
    timenow = datetime.now()
    filename = working_folder + "/capture-%02d%02d%02d%04d.jpg" % (timenow.hour, timenow.minute, timenow.second, timenow.microsecond)
    camera.capture("%s" %filename)
    print("Captured %s" % filename)

def configure_settings():
    system('clear')
    configuring = True
    while configuring == True:
        system('clear')
        print('==========================')
        print('Camera Settings')
        print('1    Load Profile')
        print('2    Configure ISO')
        #print('3    Configure Shutter Speed')
        print('\n')
        print('9    Revert to default camera options')
        print('0    Exit Configuration')
        print('\n')
        input_var = int(input('Enter an option: '))

        if input_var == 1:
            load_profile()
            configuring = False
            system('clear')
            exit
        elif input_var == 2:
            configure_ISO()
        elif input_var == 3:
            print('Option 3 is disabled')
            #configure_shuttersp()
        elif input_var == 9:
            set_defaults()
            configuring = False
            system('clear')
            exit
        elif input_var == 0:
            configuring = False
            system('clear')
            exit
        else:
            print('=============')
            print('Invalid input')
            print('=============')

def load_profile():
    system('clear')
    print('==========================')
    print('Load Profile')
    print('1    Jupiter')
    print('2    Saturn')
    print('\n')
    input_var = int(input('Enter an option: '))

    if input_var == 1:
        jupiter_profile()
    elif input_var == 2:
        saturn_profile()
    else:
        print('=============')
        print('Invalid input')
        print('=============')

def configure_ISO():
    system('clear')
    print('==========================')
    print('Configure ISO')
    print('1    100')
    print('2    200')
    print('3    320')
    print('4    400')
    print('5    500')
    print('6    640')
    print('7    800')
    print('\n')
    input_var = int(input('Enter an option: '))

    if input_var == 1:
        camera.iso = 100
    elif input_var == 2:
        camera.iso = 200
    elif input_var == 3:
        camera.iso = 320
    elif input_var == 4:
        camera.iso = 400
    elif input_var == 5:
        camera.iso = 500
    elif input_var == 6:
        camera.iso = 640
    elif input_var == 7:
        camera.iso = 800
    else:
        print('=============')
        print('Invalid input')
        print('=============')

def configure_shuttersp(): #currently disabled as framerate control is causing crashes
    system('clear')
    print('==========================')
    print('Configure Shutter Speed')
    print('Note this calculates framerate as well')
    print('\n')
    print('Opt   Shutter   Framerate')
    print('1     0.0167       60.0')
    print('2     0.0333       30.0')
    print('3     0.0667       15.0')
    print('4     0.1000       10.0')
    print('5     0.2000        5.0')
    print('6     1.0000        1.0')
    print('7     2.0000        0.5')
    print('8    10.0000        0.1')
    print('\n')
    input_var = int(input('Enter an option: '))

    if input_var == 1:
        camera.shutter_speed = 16666
        camera.framerate = 60
    elif input_var == 2:
        camera.shutter_speed = 33333
        camera.framerate = 30
    elif input_var == 3:
        camera.shutter_speed = 66666
        camera.framerate = 15
    elif input_var == 4:
        camera.shutter_speed = 100000
        camera.framerate = 10
    elif input_var == 5:
        camera.shutter_speed = 200000
        camera.framerate = 5
    elif input_var == 6:
        camera.shutter_speed = 1000000
        camera.framerate = 1
    elif input_var == 7:
        camera.shutter_speed = 2000000
        camera.framerate = 0.5
    elif input_var == 8:
        camera.shutter_speed = 10000000
        camera.framerate = 0.1
    else:
        print('=============')
        print('Invalid input')
        print('=============')

#current profiles

def jupiter_profile():
    #camera.shutter_speed = 33333
    camera.framerate = 30
    camera.iso = 200

def saturn_profile():
    #camera.shutter_speed = 33333
    camera.framerate = 30
    camera.iso = 400

def set_defaults():
    camera.resolution = default_res
    camera.framerate = default_framerate
    #camera.shutter_speed = default_shuttersp
    camera.iso = default_iso

#weird python way of calling the main function
if __name__ == "__main__":
    main()
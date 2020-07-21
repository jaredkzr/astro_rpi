import time
import os
from datetime import datetime
from signal import pause
import picamera
import math
from os import system
from fractions import Fraction

splash = """
######################################################################
 █████╗ ███████╗████████╗██████╗  ██████╗         ██████╗ ██████╗ ██╗
██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗        ██╔══██╗██╔══██╗██║
███████║███████╗   ██║   ██████╔╝██║   ██║        ██████╔╝██████╔╝██║
██╔══██║╚════██║   ██║   ██╔══██╗██║   ██║        ██╔══██╗██╔═══╝ ██║
██║  ██║███████║   ██║   ██║  ██║╚██████╔╝███████╗██║  ██║██║     ██║
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
######################################################################
"""
"""                                                        
                        By Jared Kizer

Utilize the Raspberry Pi and High Quality Camera for astrophotography

Currently only tested with solar system objects, this program offers
basic camera configuration as well as image capture and preview to
hone in on solar objects. 
######################################################################
"""

# program setup
print("Astro_RPi is initializing...")
default_res = (4056, 3040)
default_framerate = 10
default_shuttersp = 16666
default_iso = 400
              
camera = picamera.PiCamera(
    resolution = default_res,
    framerate = default_framerate,
    sensor_mode = 3)
camera.sensor_mode = 3
camera.shutter_speed = default_shuttersp
camera.iso = default_iso
time.sleep(3) #Give time to set gains
camera.exposure_mode = 'off' #Disable automatic exposure correction
camera.awb_mode = 'off' #Disable automatic white balance correction
camera.awb_gains = (camera.analog_gain)
picamera.PiCamera.CAPTURE_TIMEOUT = 120 #long timeout to allow for lengthy integration times on long exposures
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
        print(splash)
        print('\n')
        print('Home                                     Current Configuration')
        print('1    Toggle fast tracking preview        ISO: %.1f' % (camera.iso))
        print('2    Toggle image preview                Shutter Speed: %.3f s' % (camera.shutter_speed / 1000000))
        print('3    Configure settings                  Framerate: %.1f fps' % (camera.framerate))
        print('4    Single image capture                Analog Gain: %.3f' % (frac2float(camera.analog_gain)))
        print('0    Exit                                Digital Gain: %.3f' % (frac2float(camera.digital_gain)))
        print('\n')
        
        try:
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
                print('Capturing...')
                print('(This can take a while for long exposures)')
                capture_image()
            elif input_var == 0:
                run = False
                exit
            else:
                system('clear')
                print('=============')
                print('Invalid input')
                print('=============')
                time.sleep(1)
                system('clear')
        except ValueError:
            system('clear')
            print('=============')
            print('Invalid input')
            print('=============')
            time.sleep(1)
            system('clear')

def capture_image():
    try:
        timenow = datetime.now()
        filename = working_folder + "/capture-%02d%02d%02d%04d.jpg" % (timenow.hour, timenow.minute, timenow.second, timenow.microsecond)
        camera.capture("%s" %filename)
        print("Captured %s" % filename)
    except:
        system('clear')
        print('===============')
        print('Capture Failure')
        print('===============')
        time.sleep(1)
        system('clear')

def configure_settings():
    system('clear')
    configuring = True
    while configuring == True:
        system('clear')
        print(splash)
        print('\n')
        print('Camera Settings')
        print('1    Load Profile')
        print('2    Configure ISO')
        print('3    Configure Shutter Speed and Framerate')
        print('\n')
        print('9    Revert to default camera options')
        print('0    Exit Configuration')
        print('\n')

        try:
            input_var = int(input('Enter an option: '))
            if input_var == 1:
                load_profile()
                configuring = False
                system('clear')
                exit
            elif input_var == 2:
                configure_ISO()
            elif input_var == 3:
                configure_shuttersp()
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
                system('clear')
                print('=============')
                print('Invalid input')
                print('=============')
                time.sleep(1)
                system('clear')

        except ValueError:
            system('clear')
            print('=============')
            print('Invalid input')
            print('=============')
            time.sleep(1)
            system('clear')

def load_profile():
    system('clear')
    print(splash)
    print('\n')
    print('Load Profile')
    print('1    Jupiter')
    print('2    Saturn')
    print('\n')

    try:
        input_var = int(input('Enter an option: '))
        if input_var == 1:
            jupiter_profile()
        elif input_var == 2:
            saturn_profile()
        else:
            system('clear')
            print('=============')
            print('Invalid input')
            print('=============')
            time.sleep(1)
            system('clear')
    except ValueError:
            system('clear')
            print('=============')
            print('Invalid input')
            print('=============')
            time.sleep(1)
            system('clear')

def configure_ISO():
    system('clear')
    print(splash)
    print('\n')
    print('Configure ISO')
    print('1    100')
    print('2    200')
    print('3    320')
    print('4    400')
    print('5    500')
    print('6    640')
    print('7    800')
    print('\n')

    try:
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
            system('clear')
            print('=============')
            print('Invalid input')
            print('=============')
            time.sleep(1)
            system('clear')
    except ValueError:
            system('clear')
            print('=============')
            print('Invalid input')
            print('=============')
            time.sleep(1)
            system('clear')

def configure_shuttersp(): #currently disabled as framerate control is causing crashes
    system('clear')
    print(splash)
    print('\n')
    print('Configure Shutter Speed')
    print('Opt   Shutter   Framerate')
    print('1     0.0167       10.0')
    print('2     0.0333       10.0')
    print('3     0.0667       10.0')
    print('4     0.1000       10.0')
    print('5     0.2000        5.0')
    print('6     1.0000        1.0')
    print('7     5.0000        0.2')
    print('8    10.0000        0.1')
    print('\n')

    try:
        input_var = int(input('Enter an option: '))

        if input_var == 1:
            camera.framerate = 60
            camera.shutter_speed = 16666

        elif input_var == 2:
            camera.framerate = 30
            camera.shutter_speed = 33333
            
        elif input_var == 3:
            camera.framerate = 10
            camera.shutter_speed = 66666
            
        elif input_var == 4:
            camera.framerate = 10
            camera.shutter_speed = 100000
            
        elif input_var == 5:
            camera.framerate = 5
            camera.shutter_speed = 200000
            
        elif input_var == 6:
            camera.framerate = 1
            camera.shutter_speed = 1000000

        elif input_var == 7:
            camera.framerate = 0.2
            camera.shutter_speed = 5000000

        elif input_var == 8:
            camera.framerate = 0.1
            camera.shutter_speed = 10000000
            
        else:
            system('clear')
            print('=============')
            print('Invalid input')
            print('=============')
            time.sleep(1)
            system('clear')

    except ValueError:
            system('clear')
            print('=============')
            print('Invalid input')
            print('=============')
            time.sleep(1)
            system('clear')

#current profiles
def jupiter_profile():
    camera.framerate = 10
    camera.shutter_speed = 33333
    camera.iso = 200

def saturn_profile():
    camera.framerate = 10
    camera.shutter_speed = 33333
    camera.iso = 400

def set_defaults():
    camera.resolution = default_res
    camera.framerate = default_framerate
    camera.shutter_speed = default_shuttersp
    camera.iso = default_iso


def frac2float(frac_str):
    try:
        return float(frac_str)
    except ValueError:
        num, denom = frac_str.split('/')
        try:
            leading, num = num.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac

#call main func
if __name__ == "__main__":
    main()
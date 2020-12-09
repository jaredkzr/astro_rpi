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

# imaging constants
default_res = (2028, 1520)
default_framerate = 10
default_shuttersp = 20000
default_iso = 100
default_mode = 2
preview_res = (1012, 760)
              
camera = picamera.PiCamera(
    resolution = default_res,
    framerate = default_framerate,
    sensor_mode = default_mode)
camera.sensor_mode = default_mode
time.sleep(0.1)
camera.resolution = default_res
camera.framerate = default_framerate
camera.shutter_speed = default_shuttersp
camera.iso = default_iso
time.sleep(1) #Give time to set gains
#camera.exposure_mode = 'off' #Disable automatic exposure correction
#camera.awb_mode = 'off' #Disable automatic white balance correction
#camera.awb_gains = (camera.analog_gain)
picamera.PiCamera.CAPTURE_TIMEOUT = 120 #long timeout to allow for lengthy integration times on long exposures
working_folder = "/home/pi/astro_rpi"
is_recording = False
#Check if save director exists and create it if necessary
if not os.path.exists(working_folder):
    os.makedirs(working_folder)

#main program loop
def main():
    preview_on = False
    run = True
    system('clear')    
    while run == True:
        print(splash)
        print('\n')
        print('Home                                     Current Configuration')
        print('1    Toggle fast tracking preview        ISO: %.1f' % (camera.iso))
        print('2    Toggle image preview                Shutter Speed: %.3f s' % (camera.shutter_speed / 1000000))
        print('3    Configure settings                  Framerate: %.1f fps' % (camera.framerate))
        print('4    Single image capture                Analog Gain: %.3f' % (frac2float(camera.analog_gain)))
        print('5    15s video capture                   Digital Gain: %.3f' % (frac2float(camera.digital_gain)))
        print('0    Exit                                Recording: %s' % (is_recording))
        print('\n')
        
        try:
            input_var = int(input('Enter an option: '))
            if input_var == 1:
                system('clear')
                print('Fast tracking preview has been removed.')
                time.sleep(1)
                system('clear')
#                if preview_on == False: 
#                    set_previewMode()
#                    time.sleep(0.25)
#                    camera.start_preview(resolution=preview_res)
#                    preview_on = True
#                    system('clear')
#                else: 
#                    camera.stop_preview()
#                    set_defMode()
#                    time.sleep(0.25)
#                    preview_on = False
#                    system('clear')
            elif input_var == 2:
                if preview_on == False:
                    camera.start_preview(resolution=preview_res)
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
            elif input_var == 5:
                system('clear')
                capture_video()             
            elif input_var == 0:
                camera.close()
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

def capture_video():
    #Record video
    timenow = datetime.now()
    filename = working_folder + "/video-%02d%02d%02d%04d.h264" % (timenow.hour, timenow.minute, timenow.second, timenow.microsecond)
    camera.resolution = (1920,1080)
    camera.shutter_speed = 20000
    camera.framerate = 30
    camera.start_preview()
    camera.start_recording("%s" %filename, bitrate=25000000, quality = 12)
    camera.wait_recording(15)
    camera.stop_recording()
    camera.stop_preview()
    print("Captured %s" % filename)

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
        print('9    Reset camera settings')
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
                camera.close()
                set_defMode()
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

def configure_shuttersp(): 
    system('clear')
    print(splash)
    print('\n')
    print('Configure Shutter Speed')
    print('Opt   Shutter   Framerate')
    print('1     0.0200       50.0')
    print('2     0.0250       30.0')
    print('3     0.0300       30.0')
    print('4     0.0400       25.0')
    print('5     0.0500       20.0')
    print('6     0.0600       10.0')
    print('7     0.0750       10.0')
    print('8     0.1000       10.0')
    print('\n')

    try:
        input_var = int(input('Enter an option: '))
        # shutter speed in microseconds
        #framerate in fps
        if input_var == 1:
            #camera.framerate = 50
            camera.shutter_speed = 19999

        elif input_var == 2:
            #camera.framerate = 30
            camera.shutter_speed = 25000
            
        elif input_var == 3:
            #camera.framerate = 30
            camera.shutter_speed = 30000
            
        elif input_var == 4:
            #camera.framerate = 25
            camera.shutter_speed = 40000
            
        elif input_var == 5:
            #camera.framerate = 20
            camera.shutter_speed = 50000
            
        elif input_var == 6:
            #camera.framerate = 10
            camera.shutter_speed = 60000

        elif input_var == 7:
            #camera.framerate = 10
            camera.shutter_speed = 75000

        elif input_var == 8:
            #camera.framerate = 10
            camera.shutter_speed = 100000
            
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

def set_defMode():
    camera.sensor_mode = default_mode
    #time.sleep(0.1)
    camera.resolution = default_res
    camera.framerate = default_framerate
    camera.shutter_speed = default_shuttersp
    camera.iso = default_iso
    

def set_previewMode():
    camera.sensor_mode = preview_mode
    #time.sleep(0.1)
    camera.resolution = preview_res
    camera.framerate = preview_framerate
    camera.shutter_speed = preview_shuttersp
    camera.iso = preview_iso

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
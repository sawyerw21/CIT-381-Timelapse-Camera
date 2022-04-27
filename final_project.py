from gpiozero import LED
from gpiozero import MotionSensor as MS
from gpiozero import Button
from picamera import PiCamera as Camera
import os

# Create the GPIO Objects
indicator = LED(19, active_high=False)
start = Button(26, bounce_time=0.25)
motion = MS(16)

# Function to determine if timelapse will start from motion
def askMotion():
    motionChoice = ''
    # Lists for choice inputs
    yes = ['y', 'yes']
    no = ['n', 'no']

    # Get input for Motion Detection
    mC = motionChoice.lower()
    while mC not in yes and mC not in no:
        mC = input("Do you want to start the timelapse when motion is detected?\n")
        if mC in yes:
            return True
        elif mC in no:
            return False
        else:
            print("Please enter yes or no")


# Function to get user inputs to create the timeLapse bash command
def getCommand(tlName):
    # Create input variables
    tlLength = 0  # Length of the timelapse
    tlInterval = 0  # Interval between timelapse pictures

    # Get input for Timelapse Length
    while tlLength < 10:
        tlLength = int(input("How long do you want the timelapse to be? (Give in seconds)\n"))
        if tlLength < 10: print("Must be longer than 10 seconds")

    # Get input for Timelapse Interval
    while tlInterval < 1:
        tlInterval = int(input("How long do you want the time between pictures to be? (Give in seconds)\n"))
        if tlInterval < 1: print("Must be longer than 1 second")

    # Get input for the Timelapse name
    tlLength = tlLength * 1000 # Convert the timelapse length to milliseconds
    tlInterval = tlInterval * 1000 # Convert the timelapse interval to milliseconds

    tlCommand = "raspistill -t {0} -w 1280 -h 720 -q 75 --timelapse {1} --framestart 1 -o {2}%04d.jpg".format(tlLength, tlInterval, tlName)
    return tlCommand


def takeTimeLapse(command, led):
    led.on()
    os.system(command)
    led.off()

def compileTimelapse(name):
     cmd = "convert -delay 8 -loop 0 -dispose previous *.jpg  {}.gif".format(name)
     os.system(cmd)
    
def main():
    motionSensor = askMotion()  # Ask for motion
    tlName = input("What do you want to name your timelapse?\n")
    command = getCommand(tlName)  # Get the timelapse command
    os.mkdir(tlName)
    os.chdir(tlName)
    print("Press the button when you're ready to start")
    while True:
        if start.value == 1:  # If the button is pressed, the timelapse is ready to start
            if motionSensor:  # If motion is selected, it will wait for motion before starting the timelapse
                if motionSensor.motion_detected:
                    takeTimeLapse(command, indicator)
                    break
            else:  # If motion is not selected, the timelapse will start right away
                takeTimeLapse(command, indicator)
                break
    compileTimelapse(tlName)

main()


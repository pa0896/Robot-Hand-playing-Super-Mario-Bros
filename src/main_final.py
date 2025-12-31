#imports
import torch
import subprocess
from time import sleep
from hand_movements.hands import grab_controller,move_forward,jump,move_relax,jump_relax,controller_release
import RPi.GPIO as GPIO
from music_play.music_func import music_func_thread
import warnings
#only for debugging
import os

#private declarations
capture_command = ['rpicam-jpeg','--width','640','--height','480','--timeout','20','--output','/home/ampellicht/Project/captures/capture.jpeg']
delete_command = ['rm','-rf','/home/ampellicht/Project/captures/capture.jpeg']
model = None
start_btn = 5
Interrupt_Flag = False
move_flag = False # move_flag has been used to prevent low voltage conditions


#function declarations
#initialise
def init():
    global model, Interrupt_Flag
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(start_btn,GPIO.IN,pull_up_down=GPIO.PUD_UP)
        music_func_thread(0)
        model = torch.hub.load('ultralytics/yolov5','custom',path="/home/ampellicht/Project/ai_model/1.pt")
        print("Model loaded")
        #grab_controller()
        print("Ready to play -> Press the button")
        while True:
            if GPIO.input(start_btn) == GPIO.LOW:
                print("Starting program now")
                break
            else:
                continue
    except KeyboardInterrupt:
        Interrupt_Flag = True
        music_func_thread(2)
        controller_release()
        print("Press the button again to exit the program now......")
        try:
            while True:
                if GPIO.input(start_btn) == GPIO.LOW:
                    print("Exiting program now")
                    break
                else:
                    continue
        except KeyboardInterrupt:
            print("Wrong button pressed but still exiting")

def task_enemy():
    '''
    move_relax()
    sleep(1)
    jump()
    sleep(1)
    jump_relax()
    sleep(1)
    move_forward()
    '''
    jump()
    sleep(1)
    jump_relax()
    sleep(1)

def movement():
    move_forward()
    sleep(1)
    move_relax()
    sleep(1)

def main_thread(): 
    global model, capture_command, move_flag
    #start another music
    #make it random later
    music_func_thread(1)
    print("in main thread")

    try:
        while True:
            detected_objects = []
            # capturing the image, storing it in a variable for future access and then deleting the image
            subprocess.run(capture_command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            img = '/home/ampellicht/Project/captures/capture.jpeg'
            results = model(img)
            pred = results.pandas().xyxy[0]
            subprocess.run(delete_command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

            for index,rows in pred.iterrows():
                print(int(rows['xmin']),int(rows['xmax']),int(rows['ymin']),int(rows['ymax']),rows['class'],rows['confidence'])
                match rows['class']:
                    #biggest pipe
                    case 0:
                        if rows['confidence'] < 0.8:
                            continue
                        big_pipe_x = int(rows['xmin'])
                        detected_objects.append(0)
                    #gap
                    case 1:
                        if rows['confidence'] < 0.8:
                            continue
                        gap_x = int(rows['xmin'])
                        detected_objects.append(1)
                    #goomba
                    case 2:
                        if rows['confidence'] < 0.8:
                            continue
                        mid_x_goomba = int((int(rows['xmax']) + int(rows['xmin'])) / 2)
                        mid_y_goomba = int((int(rows['ymax']) + int(rows['ymin'])) / 2)
                        detected_objects.append(2)
                    #koopa
                    case 3:
                        if rows['confidence'] < 0.8:
                            continue
                        mid_x_koopa = int((int(rows['xmax']) + int(rows['xmin'])) / 2)
                        mid_y_koopa = int((int(rows['ymax']) + int(rows['ymin'])) / 2)
                        detected_objects.append(3)
                    #mario
                    case 4:
                        if rows['confidence'] < 0.8:
                            continue
                        mid_x_mario = int((int(rows['xmax']) + int(rows['xmin'])) / 2)
                        mid_y_mario = int((int(rows['ymax']) + int(rows['ymin'])) / 2)
                        detected_objects.append(4)
                    #medium height pipe
                    case 5:
                        if rows['confidence'] < 0.8:
                            continue
                        mid_pipe_x = int(rows['xmin'])
                        detected_objects.append(5)
                    #obstacle
                    case 6:
                        if rows['confidence'] < 0.8:
                            continue
                        obs_min_x = int(rows['xmin'])
                        obs_max_x = int(rows['xmax'])
                        detected_objects.append(6)
                    #small pipe
                    case 7:
                        if rows['confidence'] < 0.8:
                            continue
                        small_pipe_x = int(rows['xmin'])
                        detected_objects.append(7)
                    #platform is case 8 ignoring for now
                    case 8:
                        if rows['confidence'] < 0.8:
                            continue
                        detected_objects.append(8)
                        print(detected_objects)
                    case _:
                        print("No detections")

            #check if the list is empty, if it is, then rerun the loop
            if not detected_objects:
                continue

            #prevent multiple detections of the same object, therefore make the list unique
            unique_detected = list(set(detected_objects))
            print(unique_detected)
            #reorder the list
            unique_detected.sort()

            # remove the biggest pipe element (case 0) from the list and add at the end of it
            # because it is not a priority
            if(unique_detected[0] == 0):
                unique_detected.remove(0)
                unique_detected.append(0)

            print(unique_detected)

            #check the distance between mario and the other objects or enemies
            #checking can be priortised based on immiediate threat
            for object in unique_detected:
                match object:
                    #goomba
                    case 2:
                        if((mid_x_goomba - mid_x_mario)  < 300):
                            print("Danger from goomba")
                            task_enemy()
                        else:
                            movement()
                    #koopa
                    case 3:
                        if((mid_x_koopa - mid_x_mario) < 200):
                            print("Danger from Koopa")
                            task_enemy()
                        else:
                            movement()
                    #gap
                    case 1:
                        if((gap_x - mid_x_mario) < 150):
                            task_enemy()
                        else:
                            #may implement here a run slow
                            movement()
                    #obstacle
                    case 6:
                        task_enemy()
                    #pipes
                    case 0:
                        if((big_pipe_x - mid_x_mario) < 150):
                            task_enemy()
                        else:
                            movement()
                    case 5:
                        if((mid_pipe_x - mid_x_mario) < 150):
                            task_enemy()
                        else:
                            movement()
                    case 7:
                        if((small_pipe_x - mid_x_mario) < 150):
                            task_enemy()
                        else:
                            movement()
                    case _:
                        movement()
    except KeyboardInterrupt:
        music_func_thread(2)
        controller_release()
        print("Press the button again to exit the program now......")
        while True:
            if GPIO.input(start_btn) == GPIO.LOW:
                print("Exiting program now")
                break
            else:
                continue
    except IndexError:
        music_func_thread(2)
        controller_release()
        print("Index Error, start the program again")
        while True:
            if GPIO.input(start_btn) == GPIO.LOW:
                print("Exiting program now")
                break
            else:
                continue


#main()
if __name__ == "__main__":
    #print(os.getcwd())
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    warnings.filterwarnings("ignore",category=UserWarning)
    init()
    if Interrupt_Flag == False:
        main_thread()
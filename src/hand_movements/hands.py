from servo_motor.servo_func import servo_0, servo_180,servo_stop
from time import sleep

'''
1 is connected to left hand thumb and is pin #
2 is connected to left hand index and is pin #
3 is connected to left hand middle and is pin #
4 is connected to left hand ring and is pin #
5 is connected to left hand pinky and is pin #
6 is connected to right hand pinky and is pin #
7 is connected to right hand ring and is pin #
8 is connected to right hand middle and is pin #
9 is connected to right hand index and is pin #
10 is connected to right hand thumb and is pin #
'''

#variable space
BIG_SERVO = 0
SMALL_SERVO = 1
LEFT_BIG_SERVO = 0
RIGHT_BIG_SERVO = 1
BIG_SERVO_TUPLE = (0,1)
SMALL_SERVO_TUPLE = (0,1,2,3,4,5,6,7)


def grab_controller():
	for i in SMALL_SERVO_TUPLE:
		servo_180(SMALL_SERVO,i)
		sleep(5)
	
def move_forward():
	#left thumb actuation
	servo_180(BIG_SERVO,LEFT_BIG_SERVO)
	return True

def jump():
	#right thumb actuation
	servo_180(BIG_SERVO,RIGHT_BIG_SERVO)

def move_relax():
	#left thumb relax
	servo_0(BIG_SERVO,LEFT_BIG_SERVO)
	
def jump_relax():
	#right thumb relax
	servo_0(BIG_SERVO,RIGHT_BIG_SERVO)
	
def controller_release():
	for i in SMALL_SERVO_TUPLE:
		servo_0(SMALL_SERVO,i)
		sleep(2)
	for j in BIG_SERVO_TUPLE:
		servo_0(BIG_SERVO,j)
		sleep(2)
	servo_stop()


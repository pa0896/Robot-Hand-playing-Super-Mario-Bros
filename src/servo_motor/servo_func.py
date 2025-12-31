import pigpio

#18,19 and 21 are used for speaker
big_servos = (24,15)
small_servos = (7,8,12,14,16,20,23,25)
servos_left = (14,16,20,23)
pwm = pigpio.pi()

def init():
	global big_servos, small_servos
	for big_servo in big_servos:
		pwm.set_mode(big_servo,pigpio.OUTPUT)
		pwm.set_PWM_frequency(big_servo,330)
	for small_servo in small_servos:
		pwm.set_mode(small_servo,pigpio.OUTPUT)
		pwm.set_PWM_frequency(small_servo,50)

def servo_0(servo,servo_num):
	#big servo
	if(servo == 0):
		if servo_num == 0:
			pwm.set_servo_pulsewidth(big_servos[servo_num],1900)
		else:
			pwm.set_servo_pulsewidth(big_servos[servo_num],550)
	#small servo
	else:
		if(small_servos[servo_num] == 23 | small_servos[servo_num] == 25):
			pwm.set_servo_pulsewidth(small_servos[servo_num],2500)
		else:
			pwm.set_servo_pulsewidth(small_servos[servo_num],550)

def servo_180(servo,servo_num):
	#big servo
	if(servo == 0):
		if servo_num == 0:
			pwm.set_servo_pulsewidth(big_servos[servo_num],650)
		else:
			pwm.set_servo_pulsewidth(big_servos[servo_num],1900)
	#small servo
	else:
		if(small_servos[servo_num] == 23 | small_servos[servo_num] == 25):
			pwm.set_servo_pulsewidth(small_servos[servo_num],550)
		else:
			pwm.set_servo_pulsewidth(small_servos[servo_num],2500)

def servo_stop():
	for big_servo in big_servos:
		pwm.set_PWM_dutycycle(big_servo,0)
		pwm.set_PWM_frequency(big_servo,0)
	for small_servo in small_servos:
		pwm.set_PWM_dutycycle(small_servo,0)
		pwm.set_PWM_frequency(small_servo,0)



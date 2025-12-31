import torch
import subprocess
import struct
from time import sleep
from hand_movements.hands import grab_controller,move_forward,jump,move_relax,jump_relax

model = torch.hub.load('ultralytics/yolov5','custom',path='/home/ampellicht/Project/ai_model/1.pt')
#model = torch.hub.load('ultralytics/yolov5','custom',path='/home/ampellicht/Project/ai_model/best.onnx')
#class detection
#print(model.names)

capture_command = ['rpicam-jpeg','--width','640','--height','480','--timeout','20','--output','/home/ampellicht/Project/captures/capture.jpeg']
delete_command = ['rm','-rf','/home/ampellicht/Project/captures/capture.jpeg']

# immiediately grab controller or wait for something to happen??
# grab_controller()

while True:
	#take the image from the camera
	subprocess.run(capture_command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
	img = '/home/ampellicht/Project/captures/capture.jpeg'
	results = model(img)
	results.print()
	pred = results.pandas().xyxy[0]
	
	detected_objects = []
	
	# only for debugging purposes
	for index,row in pred.iterrows():
		#print(row['xmin'],row['xmax'],row['ymin'],row['ymax'],row['class'])
		print(int(row['xmin']),int(row['xmax']),int(row['ymin']),int(row['ymax']),row['class'],row['confidence'])
		#print(index)
		#print(type(row['xmin']))
		#print(type(row['class']))
		#msg = str(row['xmin'])+str(row['xmax'])+str(row['ymin'])+str(row['ymax'])+str(row['class'])
		'''
		only for sending something over uart pins
		baxmin = bytearray(struct.pack("f",round(row['xmin'],2)))
		baxmax = bytearray(struct.pack("f",round(row['xmax'],2)))
		baymin = bytearray(struct.pack("f",round(row['ymin'],2)))
		baymax = bytearray(struct.pack("f",round(row['ymax'],2)))
		baxmin = bytearray(struct.pack("i",int(row['xmin'])))
		baxmax = bytearray(struct.pack("i",int(row['xmax'])))
		baymin = bytearray(struct.pack("i",int(row['ymin'])))
		baymax = bytearray(struct.pack("i",int(row['ymax'])))
		class_type = bytearray(struct.pack("i",row['class']))
		baxmin.extend(b'\xFF\xFE')
		baxmin.extend(baxmax)
		baxmin.extend(b'\xFF\xFE')
		baxmin.extend(baymin)
		baxmin.extend(b'\xFF\xFE')
		baxmin.extend(baymax)
		baxmin.extend(b'\xFF\xFE')
		baxmin.extend(class_type)
		print(baxmin)
		#print(len(baxmin))
		serial_comms(baxmin)
		'''
		
	subprocess.run(delete_command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
	
	#use confidence to ascertain if the object should be taken into consideration or not. Using now a threshold value of 50%
	pred = pred[pred['confidence'] >= 0.8]
	print(pred)
	
	#process to extract the mid-point of detection of the characters and to add to the list what was detected
	for index,row in pred.iterrows():
		match row['class']:
			case 0:
				# biggest pipe
				pipe_x = int(row['xmin'])
				detected_objects.append(0)
			case 1:
				#take the left most coordinate of the gap into account, no need to calculate mid point 
				gap_x = int(row['xmin'])
				print("gap")
				detected_objects.append(1)
			case 2:
				# goomba
				mid_x_goomba = int((int(row['xmax']) + int(row['xmin'])) / 2)
				mid_y_goomba = int((int(row['ymax']) + int(row['ymin'])) / 2)
				print(mid_x_goomba,"  ",mid_y_goomba)
				detected_objects.append(2)
			case 3:
				# koopa
				mid_x_koopa = int((int(row['xmax']) + int(row['xmin'])) / 2)
				mid_y_koopa = int((int(row['ymax']) + int(row['ymin'])) / 2)
				detected_objects.append(3)
			case 4:
				# mario
				mid_x_mario = int((int(row['xmax']) + int(row['xmin'])) / 2)
				mid_y_mario = int((int(row['ymax']) + int(row['ymin'])) / 2)
				print(mid_x_mario,"  ",mid_y_mario)
				#detected_objects.append(4)
			case 5:
				# medium pipe
				pipe_x = int(row['xmin'])
				print("medium pipe")
				detected_objects.append(5)
			case 6:
				# obstacle
				obs_min_x = int(row['xmin'])
				obs_max_x = int(row['xmax'])
				print("obstacle")
				detected_objects.append(6)
			case 7:
				# pipe
				pipe_x = int(row['xmin'])
				print("pipe")
				detected_objects.append(7)
			case 8:
				# platform
				print("platform")
				detected_objects.append(8)
			case _:
				print("in default case")
	
	print("in here")
	#prevent multiple detections of some things
	unique_objects = list(set(detected_objects))
	
	# if no detections, then continue the loop
	if not unique_objects:
		#servo_run(11,2.5)
		continue
	#need to reorder the list
	unique_objects.sort()
	#need to remove the first element biggest pipe because it is not a priority, this adds it to the end of the list
	if(unique_objects[0] == 0):
		unique_objects.remove(0)
		unique_objects.append(0)
	
	#check the distance of the two objects
	#objects can be prioritised by order of their entry in the match statement
	for objects in unique_objects:
		match objects:
			#goomba
			case 2:
				# random distance 200
				if(abs(mid_x_mario-mid_x_goomba) > 200):
					continue
				else:
					#if certain distance matches then only remove entry otherwise continue
					detected_objects.remove(2)
					#need to call both the servo motor commands simultaneously or maybe let one of the thumbs be always at the on position
					jump()
					continue
			#koopa
			case 3:
				# random distance 200
				if(abs(mid_x_mario-mid_x_koopa) > 200):
					continue
				else:
					detected_objects.remove(3)
					#call servo motor module to jump
					jump()
			#gap
			case 1:
				# need to check the random distance
				if(abs(mid_x_mario-gap_x) > 200):
					continue
				else:
					#call servo motor to move forward and jump
					jump()
			#obstacle
			case 6:
				# need to keep continously moving forward and jumping, might be another way to gracefully handle this
				pass
			#pipes
			case 0 | 5 | 7 :
				# need to check the random distance
				if(abs(mid_x_mario-pipe_x) > 50):
					continue
				else:
					# call servo motor to move forward and jump
					jump()
					detected_objects.clear()
			case _:
				print("No objects detected")


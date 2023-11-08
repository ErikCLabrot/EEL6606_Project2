import cv2 as cv
import numpy as np 
import threading
import queue
import time
from djitellopy import Tello
from detection import detector
from GlobalPlanner import globalplanner
class UI(object):

	def __init__(self):
		#Init tello
		self.state_queue = queue.Queue()

		self.bat = 0
		self.angles = [0.,0.,0.,0.]

		self.tello = Tello()

		#Init video
		self.detec = detector()
		self.planner = globalplanner()

	def run(self):
		#Check error states

		self.tello.connect()
		self.tello.streamon()
		frame = self.tello.get_frame_read()
		self.tello.takeoff()
		time.sleep(4)
		run = True
		height = self.tello.get_height()
		if height > 20:
			self.tello.move_up(20)

			self.tello.move_down(height)
		while run:
			h,w,_ = frame.frame.shape
			img = cv.cvtColor(frame.frame,cv.COLOR_BGR2RGB)
			rvecs, tvecs = self.detec.detect(img)
			cv.imshow("Stream",img)
			key = cv.waitKey(16) & 0xFF
			if(key == 32):
				self.tello.land()
				run = False


			if(len(rvecs) > 0):
				print("Planning and Executing")

				height = self.tello.get_height()
				wp = self.planner.calcPlan(rvecs[0],tvecs[0])
				run = False

				print(wp[0])

				if(int(wp[0]) > 20):
					self.tello.move_right(-int(wp[1]))
					self.tello.move_left(int(wp[0]))
				elif(int(wp[0]) < -20):
					self.tello.move_left(int(wp[1]))
					self.tello.move_right(-int(wp[0]))

				self.tello.move_up(int(wp[2]))
				self.tello.move_forward(int(wp[3]))
				self.tello.land()

		self.tello.end()


import numpy as np

class globalplanner(object):
	def __init__(self):
		self.hMargin = 5 #cm
		self.xMargin = 2 #cm
		self.zMargin = 20 #cm
		self.offset = 20 #cm
	def calcPlan(self, rvec, tvec):
		print(len(rvec))
		print(len(tvec))
		print(rvec[0][0])
		print(tvec[0][0])
		wp = [0,0,0,0]

		if not(abs(tvec[0]) <= self.xMargin):
			wp[0] = -tvec[0] + -np.sign(tvec[0])*self.offset
			wp[1] = np.sign(tvec[0])*self.offset

		wp[2] = self.hMargin + self.offset

		wp[3] = tvec[2] + self.zMargin

		return wp

		#Several WP. One dimensional change at a time. Hover to height Z, roll to acceptable bounds, pitch through goal
		#Height = height diff + Ycm, point Y cm over marker
		#Left/Right = -X <= rolldiff <= X
		#Distance = tvec.z + scalar 

		#return [x,y,z] 

		#UPDATE
		#GARBO SDK ONLY ALLOWS MOVES x>20cm! Lame. Rework path planning a little bit.
		#Example: Drone 6cm to left. Travel 20cm to left, 26cm to right. 0cm offset achieved. Do this. Extra movement required to align. 
		#Scuffed. But. Works. Words to live by.
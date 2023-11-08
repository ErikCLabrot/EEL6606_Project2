import cv2 as cv
import numpy as np 
import threading
import queue
from djitellopy import Tello

class detector(object):
	def __init__(self):
		self.mtrx = np.array([[914.88712703, 0, 473.06006785], [0, 910.68258674, 348.11604291], [  0, 0, 1 ]])
		self.dist = np.array([ 2.66546113e-02, -3.89699367e-01,  1.36861296e-03, -1.14203954e-04, 1.04497706e+00])
		self.markerSize = 4.60375 #cm
		self.aruco_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_50)
		self.aruco_params = cv.aruco.DetectorParameters()
		self.detector = cv.aruco.ArucoDetector(self.aruco_dict, self.aruco_params)

	def detect(self, frame):
		self.corners, self.ids, self.rj = self.detector.detectMarkers(frame)
		if len(self.corners) > 0:
			rvecs, tvecs = self.getTF(self.corners)
			return rvecs, tvecs
		else:
			return [],[]

	def getTF(self, corners):
		marker_points = np.array([[-self.markerSize / 2, self.markerSize / 2, 0],
                          [self.markerSize / 2, self.markerSize / 2, 0],
                          [self.markerSize / 2, -self.markerSize / 2, 0],
                          [-self.markerSize / 2, -self.markerSize / 2, 0]], dtype=np.float32)
		#"Numpy array slices won't work as input because solvePnP requires contiguous arrays"
		trash = []
		rvecs = []
		tvecs = []
		i = 0
		for c in corners:
		    nada, R, t = cv.solvePnP(marker_points, corners[i], self.mtrx, self.dist, False, cv.SOLVEPNP_IPPE_SQUARE)
		    rvecs.append(R)
		    tvecs.append(t)
		    trash.append(nada)

		#print(rvecs)
		#print(tvecs)

		return rvecs, tvecs
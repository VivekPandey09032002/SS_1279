#!/usr/bin/env python3
############## Task1.1 - ArUco Detection ##############

import numpy as np
import cv2
import cv2.aruco as aruco
import sys
import math
import time

""" This function is made for camera calibration  """


def cameraCalibration(corners, image):
	CHECKBOARD = (5, 5)
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
	threedpoints = []
	twopoints = []
	
	objectp3d = np.zeros ( (1, CHECKBOARD[0] * CHECKBOARD[1], 3), np.float32)
	objectp3d [0, :, : 2] = np.mgrid [ 0:CHECKBOARD[0], 0:CHECKBOARD[1]].T.reshape(-1,2)
	
	threedpoints.append(objectp3d)
	corners2 = cv2.cornerSubPix ( image, corners, (11,11), (-1,-1), criteria)
	twopoints.append(corners2)
	ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(
	threedpoints, twodpoints, grayColor.shape[::-1], None, None)	
	print(matrix)
	print(r_vecs)
	










""" Camera calibration ends """



def mark_ArUco(img,Detected_ArUco_markers,ArUco_marker_angles):
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
    parameters = aruco.DetectorParameters_create()
    corners, ids, _ = aruco.detectMarkers(img, aruco_dict, parameters = parameters)
    img = aruco.drawDetectedMarkers(img,corners,ids,(0,0,255))
    
    
    lis = [(125,125,125),(0,255,0),(180,105,255),(255,255,255),(0,0,255),(255,0,0)]
    # angle
    
    for id in Detected_ArUco_markers.keys():
        corners = Detected_ArUco_markers[id]
        corners = np.int0(corners)
        i=0
        for corner in corners:
        	x,y = corner.ravel()
        	cv2.circle(img,(x,y),5,lis[i],-1)
        	i=i+1
        cx = 0
        cy = 0
        for arr in corners:
        	cx += arr[0]
        	cy += arr[1]
        cx = cx // 4;
        cy = cy // 4;	
        center = tuple([cx,cy])
        cv2.circle(img,(cx,cy),5,lis[4],-1)
        tl = corners[0]
        tr = corners[1]
        midx = (tl[0] + tr[0]) // 2
        midy = (tl[1] + tr[1]) // 2		
        middle = tuple([midx, midy])
        cv2.line(img,center,middle,(255,0,0),1)
        # printing the angles
        print(id)
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = ( cx-35 , cy-15)
        fontScale = 0.6
        color = (0, 255 , 0)
        thickness = 2
        img = cv2.putText(img, str(ArUco_marker_angles[id]), org, font, fontScale, color, thickness, cv2.LINE_AA)
	 
		
		        
        
      
		
    return img

def detect_ArUco(img):
	## function to detect ArUco markers in the image using ArUco library
	## argument: img is the test image
	## return: dictionary named Detected_ArUco_markers of the format {ArUco_id_no : corners}, where ArUco_id_no indicates ArUco id and corners indicates the four corner position of the aruco(numpy array)
	## 		   for instance, if there is an ArUco(0) in some orientation then, ArUco_list can be like
	## 				{0: array([[315, 163],
	#							[319, 263],
	#							[219, 267],
	#							[215,167]], dtype=float32)}

    Detected_ArUco_markers = {}
    ## enter your code here ##
    imggray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
    parameters = aruco.DetectorParameters_create()
    corners, ids, _ = aruco.detectMarkers(imggray, aruco_dict, parameters = parameters)

    for i in range(0,len(ids)):
        Detected_ArUco_markers[ids[i][0]] = corners[i][0]
    # print(Detected_ArUco_markers)
    return Detected_ArUco_markers


def Calculate_orientation_in_degree(Detected_ArUco_markers):
	## function to calculate orientation of ArUco with respective to the scale mentioned in problem statement
	## argument: Detected_ArUco_markers  is the dictionary returned by the function detect_ArUco(img)
	## return : Dictionary named ArUco_marker_angles in which keys are ArUco ids and the values are angles (angles have to be calculated as mentioned in the problem statement)
	##			for instance, if there are two ArUco markers with id 1 and 2 with angles 120 and 164 respectively, the 
	##			function should return: {1: 120 , 2: 164}

	ArUco_marker_angles = {}
	## enter your code here ##
	
	for ids, corner in Detected_ArUco_markers.items():

		top_right_angle = (math.degrees(math.atan2(-corner[1][1] + corner[3][1], corner[1][0] - corner[3][0]))) % 360
		angle = (top_right_angle + 45) % 360
		ArUco_marker_angles[ids] = int(angle)	
         


	return ArUco_marker_angles	## returning the angles of the ArUco markers in degrees as a dictionary



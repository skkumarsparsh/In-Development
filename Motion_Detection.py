from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import cv2
import numpy as np
import datetime
import time
import smtplib

# 'google drive authentication' stuff
gauth = GoogleAuth()
drive = GoogleDrive(gauth)

# 'sending an email' stuff
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login("sparshbbhs@gmail.com","thisisatest")
msg = "Motion Detected! See Google Drive."

# capture Video from the camera module
cap = cv2.VideoCapture(0)

# make count 0
count = 0

# stores the present date and time
lastUploaded = datetime.datetime.now()

# kernel is created for the dilation process
k = np.ones((3,3),np.uint8) # creates a 3X3 Matrix filled with ones and
                            # has the data type uint8 (unsigned integer)
                            # which can contain values from 0 to 255

# first two subsequent frames captured
t0 = cap.read()[1]
t1 = cap.read()[1]

# initially motion detected 0 times
motionCounter = 0

while True:
    # difference between two subsequent frames
    d=cv2.absdiff(t1,t0)

    # stores present date and time
    timestamp = datetime.datetime.now()

    # converting difference to grayscale
    grey = cv2.cvtColor(d,cv2.COLOR_BGR2GRAY)

    # grayscale converted to gaussian blur
    blur = cv2.GaussianBlur(grey,(3,3),0)

    # gaussian blur converted to binary image
    ret, th = cv2.threshold(blur, 15, 155, cv2.THRESH_BINARY)

    # dilating the image before using the contour function
    dilated = cv2.dilate(th,k,iterations=2)

    # contour function to find edges
    _, contours, heierarchy = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # copying the original frame to a temporary frame for display
    t2 = t0

    # drawing green edges around the area with movement
    cv2.drawContours(t2, contours, -1, (0,255,0), 2)

    # showing output in a new window
    cv2.imshow('Output',t2)

    # going through each and every contour in the image
    for c in contours:
        # if contour is lesser than a threshold size, ignore
        if cv2.contourArea(c) < 5000:
            continue

        # if motion occurred after 2 secs
        if (timestamp - lastUploaded).seconds >= 2.0:
            motionCounter += 1

            # if 8 motions occured in 2 secs
            if motionCounter >= 8:
                # write to a temporary file location
                cv2.imwrite("/home/pi/Desktop/StoredImages/frame%d.jpg" % count, t2)

                # upload the temporary pic to Google drive
                file1 = drive.CreateFile({'parent':'/home/pi/Desktop/StoredImages/'})
                file1.SetContentFile('/home/pi/Desktop/StoredImages/frame%d.jpg' % count)
                file1.Upload()

                # sending a mail about motion detected
                server.sendmail("sparshbbhs@gmail.com","skkumarsparsh@gmail.com",msg)

                # increasing count by 1 and resetting everything
                count=count+1
                lastUploaded = timestamp
                motionCounter = 0

    # making the next frame the previous and reading a new frame
    t0 = t1
    t1 = cap.read()[1]

    # esc key breaks the entire loop
    if cv2.waitKey(5) == 27:
        break

# stops the video stream and exits the window
cap.release()
cv2.destroyAllWindows()

# stops the email server connection
server.quit()

import cv2
import numpy as np

# capture Video from the camera module
cap = cv2.VideoCapture(0)

# kernel is created for the dilation process
k = np.ones((3,3),np.uint8) # creates a 3X3 Matrix filled with ones and
                            # has the data type uint8 which contains values from 0 to 255

# first two subsequent frames captured
t0 = cap.read()[1]
t1 = cap.read()[1]

while True:
    # difference between two subsequent frames
    d=cv2.absdiff(t1,t0)

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

    # making the next frame the previous and reading a new frame
    t0 = t1
    t1 = cap.read()[1]

    # esc key breaks the entire loop
    if cv2.waitKey(5) == 27:
        break

# stops the video stream and exits the window
cap.release()
cv2.destroyAllWindows()

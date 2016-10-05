from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from picamera import PiCamera
from time import sleep

camera = PiCamera()

sleep(3)
camera.resolution = (1920, 1080)
camera.start_recording('/home/pi/Desktop/videotest.h264')
sleep(10)
camera.stop_recording()

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

file1 = drive.CreateFile({'parent':'/home/pi/Desktop'})
file1.SetContentFile('videotest.h264')
file1.Upload()



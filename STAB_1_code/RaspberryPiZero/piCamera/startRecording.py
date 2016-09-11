import time
import picamera
camera = picamera.PiCamera()

time = time.strftime("%H_%M_%S")
date = time.strftime("%Y_%m_%d")

filename = time + 'EST' + date + 'video' + '.h264'

camera.resolution = (1280, 720) #1280x720
camera.framerate = 60 #frames/sec
recordingDuration = 5 #seconds

#Start filming...
camera.start_recording(filename)
camera.wait_recording(recordingDuration)
camera.stop_recording()

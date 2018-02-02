import cv2
options = {"models":"cfg/yolo.cfg", "load":"bin/yolo.weights", "threshold":0.1}
tfnet = TFNet(options)
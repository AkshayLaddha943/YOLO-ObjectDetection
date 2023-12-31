# -*- coding: utf-8 -*-
"""YOLOv3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19nmuDxjqAheoe6tyHIFC-DDBTzBMvN4b
"""

import cv2
import numpy as np

#load YOLOv3 weights and cfg file
net = cv2.dnn.readNet("yolov3.weights","yolov3.cfg")

#load the class values
classes = []
with open("coco.names", "r") as f:
  classes = [line.strip() for line in f.readlines()]
#print(classes)

#get the convolution layer
layernames = net.getLayerNames()
outputlayers = [layernames[i-1] for i in net.getUnconnectedOutLayers()]
#print(outputlayers)

colors = np.random.uniform(0, 255, size=(len(classes), 3))

#load image or video``
cap = cv2.VideoCapture("Movingvehicles2.mp4")
font = cv2.FONT_HERSHEY_SIMPLEX

#width and height of video frame
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#Define the codec and create VideoWriter object
codecc = cv2.VideoWriter_fourcc(*'mp4v')
vids = cv2.VideoWriter('yolo.mp4', codecc, 30, (width, height))

while True:
  ret, frame = cap.read()
  if not ret:
    break
  height, width, channels = frame.shape
  blob = cv2.dnn.blobFromImage(frame,0.00392,(320,320),(0,0,0),True,crop=False)
  net.setInput(blob)
  output = net.forward(outputlayers)

  class_ids = []
  confidences = []
  boxes = []
  for out in output:
    for detection in out:
      scores = detection[5:]
      class_id = np.argmax(scores)
      confidence = scores[class_id]
      if confidence > 0.3:

        #object detected
        center_x = int(detection[0]*width)
        center_y= int(detection[1]*height)
        w = int(detection[2]*width)
        h = int(detection[3]*height)

        #rectangle co-ordinaters
        x=int(center_x - w/2)
        y=int(center_y - h/2)

        boxes.append([x,y,w,h]) #put all rectangle areas
        confidences.append(float(confidence)) #how confidence was that object detected and show that percentage
        class_ids.append(class_id) #name of the object tha was detected

  # any box having value less than 0.6- that will be removed
  indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.6)

  for i in range(len(boxes)):
    if i in indexes:
      x,y,w,h = boxes[i]
      label = str(classes[class_ids[i]])
      confidence= confidences[i]
      color = colors[class_ids[i]]
      cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
      cv2.putText(frame,label+" "+str(round(confidence,2)),(x,y+30),font,1,(255,255,255),2)

  #writing the frame
  vids.write(frame)
  #wait 1ms the loop will start again and we will process the next frame
  cv2.imshow("Video", frame)
  if cv2.waitKey(25) & 0xFF == ord('q'):
    break

cap.release()
vids.release()
cv2.destroyAllWindows()
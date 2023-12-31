import cv2 
import numpy as np
from pyzbar.pyzbar import decode
import time
# import keras_retinanet
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color
from keras_retinanet.utils.gpu import setup_gpu

# import miscellaneous modules
import matplotlib.pyplot as plt

import os

import glob

# set tf backend to allow memory to grow, instead of claiming everything
import tensorflow as tf

model = models.load_model('model.h5', backbone_name='resnet50')


# load label to names mapping for visualization purposes
labels_to_names = {0: 'leave'}
def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def center(left,width):
    if (left + width - 650)<100 and (left + width - 650)>-100:
        return 1
    else:
        return 0


def capture():
    cap = cv2.VideoCapture('video1.mp4')
    i=0

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        ret, frame = cap.read()
        #frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
        

        if i%15 ==0:
            cv2.imshow('Input', frame)

            cv2.imwrite('Frame'+str(i/15)+'.jpg',frame)
        i+=1

        
        

        c = cv2.waitKey(1)
        if c == 27 or i/15==15:
            break



    cap.release()
    cv2.destroyAllWindows()
    return 7



cap=cv2.VideoCapture(0)
cap.set(3,1300)
cap.set(4,1300)


while True:

    success,img =cap.read()
    counter=0
    


    for barcode in decode(img):

        print(barcode)

    
        #center check
        if center(barcode.rect[0],barcode.rect[2]):
            print('centered')
        else:
            print('not centered')
        
        #message printing
        mydata=barcode.data.decode('utf-8')
        print(mydata)

        #preparing points arrays and drawing polygon
        pts= np.array([barcode.polygon],np.int32)
        pts=pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(255,0,255),5)
        x=[]
        y=[]
        for i in barcode.polygon:
            x.append(i[0])
        for i in barcode.polygon:
            y.append(i[1])
        x=np.array(x)
        y=np.array(y)
        print(PolyArea(x,y))
        counter=counter+1
    
    
    
    cv2.imshow('result',img)
    c = cv2.waitKey(1)

    if c == 27:
        next=True
        break
        



    

    if counter !=0:
        next=True
        break

#######################################################################################
#extract images
#######################################################################################

if next==True:
    capture()
    
    imgs = [cv2.imread(file) for file in glob.glob("*.jpg")]

    i=0

    for image in imgs:
        

        # copy to draw on
        draw = image.copy()
        draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)

        # preprocess image for network
        image = preprocess_image(image)
        image, scale = resize_image(image)

        # process image
        start = time.time()
        boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
        print("processing time: ", time.time() - start)
        

        # correct for image scale
        boxes /= scale

        # visualize detections
        for box, score, label in zip(boxes[0], scores[0], labels[0]):
            # scores are sorted so we can break
            if score < 0.4:
                break
            print(box,score,label)

            color = label_color(label)

            b = box.astype(int)
            draw_box(draw, b, color=color)

            caption = "{} {:.3f}".format(labels_to_names[label], score)
            draw_caption(draw, b, caption)
        draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)

        
        cv2.imwrite(os.path.join('C:/Users/user/Desktop/for the project/full code/detected','Frame'+str(i)+'.jpg'),draw)
        i+=1


        time.sleep(0.2)







    




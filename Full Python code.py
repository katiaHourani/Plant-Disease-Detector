from cmath import polar
from math import fabs
import cv2 as cv
import time
import numpy as np
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import serial
from serial import Serial
import socket
import os
import sys
import zipfile

zip_name='main.zip'
k=10
#---------------initializing Serial-------------
if __name__ == '__main__':
    ser = serial.Serial('COM6', 9600, timeout=1)
    ser.reset_input_buffer()
    

#---------------socket connection----------

s=socket.socket()
host=''
port=8080
s.bind((host,port))
s.listen(1)
print(host)
print("waiting for host to connect.....")
conn , addr =s.accept()
print(addr, " has connected")
ser.write(b"12") #turn on lamp using arduino green color 


#-------------- variable-------------------
# "0" random search
# "1" approach the target
checked=[]
finished=True



#--------------initializing camera-----------------
def capture1():

    global cap

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    cap.set(cv.CAP_PROP_FRAME_WIDTH,640)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT,480)

capture1()

#--------------Functions-------------------------
def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))


def center(x1,x2):

    if(  (((x1+x2)/2 -320 ) < 50) & (((x1+x2)/2 -320 ) > -50 )):
        return 0
    
    if(  (((x1+x2)/2 -320 ) > 50) ):
        return 1

    if( (((x1+x2)/2 -320 ) < -50 ) ):
        return 2

def check(plantnumber):
    for i in checked:
        if i==plantnumber:
            return True
    return False

def capAndSend():

    p=1
    while p !=11:
        filename=str(p)+".jpg"
        success, img = cap.read()
        cv.imwrite(filename, img)
        p=p+1


    with zipfile.ZipFile(zip_name, 'w') as file:
        for j in range(1, (k+1)):
            file.write('{}.jpg'.format(j))
            print('[+] {}.jpg is sent'.format(j))
    
    filename=input(str("please enter the file name: "))
    file=open(filename,'rb')
    file_data=file.read(1024)
    conn.send(file_data)
    print("data is successfully sent")

    finished=True
        

# -------------start detecting barcode------------

ser.write(b"0") 

while True:
    success, img = cap.read()

    if finished:
        
        lapse=time.time()
        ser.write(b"0")  
        print("sending :") 
        print("0") 
        
    
    for barcode in decode(img, symbols=[ZBarSymbol.QRCODE]):
        mydata=barcode.data.decode('utf-8')
        #print(barcode)

        
        

        #preparing points arrays and drawing polygon
        pts= np.array([barcode.polygon],np.int32)
        pts=pts.reshape((-1,1,2))
        cv.polylines(img,[pts],True,(255,0,255),5)
        x=[]
        y=[]
        for i in barcode.polygon:
            x.append(i[0])
        for i in barcode.polygon:
            y.append(i[1])
        x=np.array(x)
        y=np.array(y)
        print(PolyArea(x,y))
        print(x)
        print(y)

        #send serial

        if not check(mydata):
            finished=False
            lapse=time.time()


            if center(x[0],x[2])==0 and PolyArea(x,y)> 30000 :
                #ready to scan
                ser.write(b"1")
                print("sending: ")
                print("1")
                #call capAndScan() function
                capAndSend()

            elif  center(x[0],x[2])==0 and PolyArea(x,y)< 30000 :
                #go straight
                ser.write(b"2")
                print("sending: ")
                print("2")

            elif ( center(x[0],x[2])==1) and PolyArea(x,y)< 30000 :
                #rotate left then go straight
                ser.write(b"3")
                print("sending: ")
                print("3")

            elif ( center(x[0],x[2])==1) and PolyArea(x,y)> 30000 :
                #only rotate left
                ser.write(b"4")
                print("sending: ")
                print("4")

            elif ( center(x[0],x[2])==2) and PolyArea(x,y)< 30000 :
                #rotate right then go straight
                ser.write(b"5")
                print("sending: ")
                print("5")

            elif ( center(x[0],x[2])==2) and PolyArea(x,y)> 30000 :
                #only rotate right
                ser.write(b"6")
                print("sending: ")
                print("6")

            else:
                #rotate a little bit only
                ser.write(b"7")
                print("sending: ")
                print("7")  
    period=time.time()-lapse
    print(period)
    if(period>20):
        finished=True
    cv.imshow("h",img)

    c=cv.waitKey(1)
    if(c==27):
        break
    

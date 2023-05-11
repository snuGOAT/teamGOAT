# !/usr/bin/env python3
import rospy
import numpy as np
import cv2
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header


# 해야할 것 :
# grabcut algorithm 확인하기 ( 56-75 ), 68번 이미지 확인 후 주석.
# 아마 배경이 전부 흑으로 처리되어서 나와 사각형으로 slicing 하기(시간 땜에)

class DetermineColor:
    def __init__(self):
        self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.callback)
        self.color_pub = rospy.Publisher('/rotate_cmd', Header, queue_size=10)
        self.bridge = CvBridge()
        self.count = 0

        self.result = [0,0,0] # R B None

    def distance(self, A):
        V = np.max(A)
        S = (V-np.min(A))/V if V!=0 else 0
        H = 60 * (A[1]-A[0])/(V-np.min(A)) if V==A[2] else ( 120 + 60*(A[0]-A[2])/(V-np.min(A)) if V==A[1] else (240 + 60 * (A[2]-A[1])/(V-np.min(A))))
        H = H+360 if H<0 else H
        print(H,S,V)
        if 0<=H<=30 or 330<=H<=360  : #red
            self.result[0] += 1

        elif 190<=H<=260 : #blue
            self.result[1] += 1

        else :
            self.result[2] += 1


    def callback(self, data):
        try:
            # listen image topic
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
         
            #cv2.imshow('Image',image) # 가져온 프레임 보여주기.
            cv2.waitKey(1)
            
            # prepare rotate_cmd msg
            # DO NOT DELETE THE BELOW THREE LINES!
            msg = Header()
            msg = data.header
            # msg.frame_id = '0'  # default: STOP

            # 여기서 시작.
            self.result = [0, 0, 0]

            mask = np.zeros(image.shape[:2],np.uint8)
            bgdModel = np.zeros((1,65),np.float64)
            fgdModel = np.zeros((1,65),np.float64)
            # Step 1
            length = len(image)
            width = len(image[0])
            rect = (0,0, length, width)
            cv2.grabCut(image,mask,rect,bgdModel,fgdModel, 3,cv2.GC_INIT_WITH_RECT) # 3 : 반복횟수
            # Step 2
            mask_2 = np.where((mask==2) | (mask==0), 0, 1).astype('uint8')
            img_grabcut = image*mask_2[:,:,np.newaxis]
            print("length : %s, width : %s" %(len(img_grabcut), len(img_grabcut[0])))
            cv2.imshow('image', img_grabcut)

            # resize_img = cv2.resize(image, (300, 500)) # 이미지 크기 확인.(해야됨) 480 640
            # image2 = image[200:400][50:300]
            # print(image2[1])
            resize_img = cv2.resize(img_grabcut, (0,0), fx=0.5,fy=0.5)
            #print(resize_img) 
            
            # cv2.imshow('Image',image2)
            for i in range(len(resize_img)) :
                for j in range(len(resize_img[0])) :
                    self.distance(resize_img[i][j])
                    
            print(self.result)
                             
            max = np.max(self.result)
            if max == self.result[0] : 
                msg.frame_id = '-1'
                print('red')
            elif max == self.result[1] :
                msg.frame_id = '+1'
                print('blue')
            else : 
                msg.frame_id = '0'
                print('None')

            # determine background color
            # TODO
            # determine the color and assing +1, 0, or, -1 for frame_id
            # msg.frame_id = '+1' # CCW (Blue background)
            # msg.frame_id = '0'  # STOP
            # msg.frame_id = '-1' # CW (Red background)

		
            # publish color_state
            self.color_pub.publish(msg)

        except CvBridgeError as e:
            print(e)


    def rospy_shutdown(self, signal, frame):
        rospy.signal_shutdown("shut down")
        sys.exit(0)

if __name__ == '__main__':
    detector = DetermineColor()
    rospy.init_node('CompressedImages1', anonymous=False)
    rospy.spin()




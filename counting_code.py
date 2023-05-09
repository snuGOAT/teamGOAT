# !/usr/bin/env python3
import rospy
import numpy as np
import cv2
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header

class DetermineColor:
    def __init__(self):
        self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.callback)
        self.color_pub = rospy.Publisher('/rotate_cmd', Header, queue_size=10)
        self.bridge = CvBridge()
        self.count = 0

        self.result = [0,0,0] # R B None

    def distance(self, A):
        R = [0, 0, 255] # BGR
        B = [255, 0, 0] # BGR
        G = [0, 255, 0]
        Y = [0, 255/np.sqrt(2), 255/np.sqrt(2)]
        Rad = 250*250/2 # 300aseo jaldam
        
        disR=np.sum( [(int(R[i])-int(A[i]))**2 for i in range(3)] )
        disB=np.sum( [(int(B[i])-int(A[i]))**2 for i in range(3)] )
        disG=np.sum( [(int(G[i])-int(A[i]))**2 for i in range(3)] )
        #print(disR)
        '''
        if disR > disB:
            self.result[1] += 1
        else:
            self.result[0] += 1		
        '''
        if disR <= disB and disR <= disG: 
            self.result[0] += 1

        elif disB <= disG : 
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
            msg.frame_id = '0'  # default: STOP

            # 여기서 시작.
            self.result = [0, 0, 0]
            #resize_img = cv2.resize(image, (300, 500)) # 이미지 크기 확인.(해야됨) 480 640
            image2 = image[200:400][50:300]
            print(image2[1])
            resize_img = cv2.resize(image2, (0,0), fx=0.5,fy=0.5)
            #print(resize_img) 
            #print(resize_img)
            
            
            cv2.imshow('Image',image2)
            
            for i in range(len(resize_img)) :
                for j in range(len(resize_img[0])) :
                    self.distance(resize_img[i][j]) # 함수 실행 어케함?
                    
            #print(np.sum(resize_img) / (len(resize_img)*len(resize_img[0])))
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

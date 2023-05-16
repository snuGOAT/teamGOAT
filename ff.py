	# !/usr/bin/env python3
import rospy
import numpy as np
import cv2
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header

np.seterr(divide='ignore', invalid='ignore') 

class DetermineColor:
    def __init__(self):
        self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.callback)
        self.color_pub = rospy.Publisher('/rotate_cmd', Header, queue_size=10)
        self.bridge = CvBridge()
        self.count = 0
           

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
            resize_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            Width = len(resize_img[0])
            Height = len(resize_img)
            H = resize_img[:, :, 0] # H tjdqns      			
            # print(H)
            
            R = H[0<=H<=38 or 330<=H<=360].size
            B = H[190<=H<=270].size
            G = Width*Height-R-B
            
            M = np.max([R, B, G])
            if M == R :
                msg.frame_id = '-1'
            elif M == B :
                msg.frame_id = '+1'
            else : 
                msg.frame_is = '0'

        except CvBridgeError as e:
            print(e)


    def rospy_shutdown(self, signal, frame):
        rospy.signal_shutdown("shut down")
        sys.exit(0)

if __name__ == '__main__':
    detector = DetermineColor()
    rospy.init_node('CompressedImages1', anonymous=False)
    rospy.spin()

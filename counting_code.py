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

        self.result = np.array([0, 0, 0])

    def distance(self, A)
        R = (0, 0, 255) # BGR
        B = (255, 0, 0) # BGR
        Rad = 10**2
        disR = 0
        disB = 0

        for i in range(3) :
            disR += (R[i]-A[i])**2
            disB +=(B[i]-A[i])**2
        if disR < Rad : 
            self.result[0] += 1

        elif disB < Rad : 
            self.result[1] += 1

        else :
            self.result[2] += 1

    def callback(self, data):
        try:
            # listen image topic
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            cv2.imshow('Image',image) # 가져온 프레임 보여주기.
            cv2.waitKey(1)
            

            # prepare rotate_cmd msg
            # DO NOT DELETE THE BELOW THREE LINES!
            msg = Header()
            msg = data.header
            msg.frame_id = '0'  # default: STOP

            # 여기서 시작.
            self.result = np.array([0, 0, 0])
            resize_img = cv2.resize(image, (300, 500)) # 이미지 크기 확인.(해야됨)
            for i in range(300) :
                for j in range(500) :
                    self.distance(resize_img[i, j]) # 함수 실행 어케함?

            max = np.max(self.result)
            if max == self.result[0] : 
                msg.frame_id = '-1'
            elif max == self.result[1] :
                msg.frame_id = '+1'
            else : 
                msg.frame_id = '0'

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

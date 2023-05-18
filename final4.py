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

    def callback(self, data):
        try:
            # listen image topic
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            # cv2.imshow('Image',image)
            # cv2.waitKey(1)
            
            '''
            length = len(image)
            width = len(image[0])
            rect = (0,0, length, width)
            cv2.grabCut(image,mask,rect,bgdModel,fgdModel, 3,cv2.GC_INIT_WITH_RECT) # 3 : 반복횟수
            # Step 2
            mask_2 = np.where((mask==2) | (mask==0), 0, 1).astype('uint8')
            image = image*mask_2[:,:,np.newaxis]
            '''

            # prepare rotate_cmd msg
            # DO NOT DELETE THE BELOW THREE LINES!
            msg = Header()
            msg = data.header
            msg.frame_id = '0'  # default: STOP
        
            hsv=cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hist, _ = np.histogram(hsv[:,:,0], bins=180, range=[0, 180])
            common_color=np.argmax(hist)
            
            if 165<=common_color <=180 or 0<= common_color <=14:
                msg.frame_id ='-1'
            elif 90<=common_color <=135:
                msg.frame_id ='+1'
            else:
                msg.frame_id = '0'
            
            self.color_pub.publish(msg)
            
        except CvBridgeError as e:
            print(e)


    def rospy_shutdown(self, signal, frame):
        rospy.signal_shutdown("shut down")
        sys.exit(0)

if __name__ == '__main__':
    rospy.init_node('CompressedImages1', anonymous=False)
    detector = DetermineColor()
    rospy.spin()
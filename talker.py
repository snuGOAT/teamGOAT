from std_msgs.msg import String
import rospy
import subprocess
import time


def talker():
    pub = rospy.Publisher('chatter', String, queue_size=20)
    rospy.init_node('talker', anonymous=True)
    rate=rospy.Rate(10)
    time.sleep(0.1)

    for i in range(10):
        hello='hello world %s'% rospy.get_time()
        pub.publish(hello)
        rate.sleep()
        

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

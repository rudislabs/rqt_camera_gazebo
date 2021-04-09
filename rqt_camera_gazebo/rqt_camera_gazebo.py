#!/usr/bin/env python3
import os
import sys
import copy
import re
import importlib
import numpy as np
import rclpy
from rclpy.qos import qos_profile_sensor_data
from rclpy.node import Node
from rclpy.exceptions import ParameterNotDeclaredException
from rcl_interfaces.msg import Parameter
from rcl_interfaces.msg import ParameterType
from rcl_interfaces.msg import ParameterDescriptor
import sensor_msgs.msg
from cv_bridge import CvBridge
from rclpy.qos import QoSProfile
import cv2
if cv2.__version__ < "4.0.0":
    raise ImportError("Requires opencv >= 4.0, "
                      "but found {:s}".format(cv2.__version__))

class RQTCameraGazebo(Node):

    def __init__(self):

        super().__init__("rqt_camera_gazebo")

        # Get paramaters or defaults
        camera_image_subscription_topic_descriptor = ParameterDescriptor(
            type=ParameterType.PARAMETER_STRING,
            description='Camera image subscription topic.')
        
        camera_image_publish_topic_descriptor = ParameterDescriptor(
            type=ParameterType.PARAMETER_STRING,
            description='Camera image publish topic.')

        camera_image_format_descriptor = ParameterDescriptor(
            type=ParameterType.PARAMETER_STRING,
            description='Camera image format.')

        
        self.declare_parameter("camera_sub", "rgb_cam", 
            camera_image_subscription_topic_descriptor)
        
        self.declare_parameter("camera_pub", "rqt_rgb_cam", 
            camera_image_publish_topic_descriptor)

        self.declare_parameter("camera_format", "bgr8", 
            camera_image_publish_topic_descriptor)

        self.cameraImageSubTopic = self.get_parameter("camera_sub").value

        self.cameraImagePubTopic = self.get_parameter("camera_pub").value

        self.cameraImageFormat = self.get_parameter("camera_format").value


        #setup CvBridge
        self.bridge = CvBridge()

        
        #Subscribers
        self.imageSub = self.create_subscription(sensor_msgs.msg.Image, 
            '/{:s}'.format(self.cameraImageSubTopic), 
            self.imageCallback, 
            qos_profile_sensor_data)

        #Publishers
        self.imagePub = self.create_publisher(sensor_msgs.msg.Image,
            '/{:s}'.format(self.cameraImagePubTopic), 0)

    
    def imageCallback(self, data):
        
        # Scene from subscription callback
        scene = self.bridge.imgmsg_to_cv2(data, self.cameraImageFormat)
        msg = self.bridge.cv2_to_imgmsg(scene, self.cameraImageFormat)
        msg.header.stamp = data.header.stamp
        self.imagePub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = RQTCameraGazebo()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

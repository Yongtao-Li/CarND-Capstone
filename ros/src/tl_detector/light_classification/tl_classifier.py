import rospy
import cv2
import tensorflow as tf
import numpy as np
from styx_msgs.msg import TrafficLight
import time

class TLClassifier(object):
    def __init__(self):
        #TODO load classifier
        self.SSD_SIM_FILE = './ssd_mobilenet_v1_coco_11_06_2017/frozen_inference_graph.pb'
        self.detection_graph = self.load_graph(self.SSD_SIM_FILE)
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.tf_session = tf.Session(graph=self.detection_graph)
    
    def load_graph(self, graph_file):
        """Loads a frozen inference graph"""
        graph = tf.Graph()
        with graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(graph_file, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        return graph

    def filter_boxes(self, min_score, boxes, scores, classes):
        """Return boxes with a confidence >= `min_score`"""
        n = len(classes)
        idxs = []
        for i in range(n):
            if scores[i] >= min_score:
                idxs.append(i)
        
        filtered_boxes = boxes[idxs, ...]
        filtered_scores = scores[idxs, ...]
        filtered_classes = classes[idxs, ...]
        return filtered_boxes, filtered_scores, filtered_classes
    
    # the input is an Numpy array
    # the output is the class and score
    def pipeline(self, img):
        # draw_img = Image.fromarray(img)
        boxes, scores, classes = self.tf_session.run([self.detection_boxes, self.detection_scores, self.detection_classes], feed_dict={self.image_tensor: np.expand_dims(img, 0)})
        # Remove unnecessary dimensions
        boxes = np.squeeze(boxes)
        scores = np.squeeze(scores)
        classes = np.squeeze(classes)
    
        confidence_cutoff = 0.8
        # Filter boxes with a confidence score less than `confidence_cutoff`
        boxes, scores, classes = self.filter_boxes(confidence_cutoff, boxes, scores, classes)
    
        # The current box coordinates are normalized to a range between 0 and 1.
        # This converts the coordinates actual location on the image.
        # width, height = draw_img.size
        # box_coords = to_image_coords(boxes, height, width)
    
        # Each class with be represented by a differently colored box
        # draw_boxes(draw_img, box_coords, classes)
        return scores, classes

    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #TODO implement light color prediction
        #imgfile = str(rospy.Time.now().to_sec()) + '.jpg'
        #cv2.imwrite(imgfile, image)
        tlScore, tlClass = self.pipeline(image)
        rospy.logwarn("score = {0}".format(tlScore))
        rospy.logwarn("class = {0}".format(tlClass))
        #rospy.logwarn("classifier time = {0}".format(time.time()))
        if (tlClass.size == 0 or tlScore.size == 0):
            #rospy.logwarn("light state = UNKNOWN")
            return TrafficLight.UNKNOWN
        elif (tlClass[np.argmax(tlScore)] == 2):
            #rospy.logwarn("light state = RED")
            return TrafficLight.RED
        elif (tlClass[np.argmax(tlScore)] == 1):
            #rospy.logwarn("light state = GREEN")
            return TrafficLight.GREEN
        elif (tlClass[np.argmax(tlScore)] == 3):
            #rospy.logwarn("light state = YELLOW")
            return TrafficLight.YELLOW
        else:
            #rospy.logwarn("light state = UNKNOWN")
            return TrafficLight.UNKNOWN
        #return TrafficLight.RED

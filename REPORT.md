# **Programming a Real Self-Driving Car**

## Yongtao Li

---

The goals of this project are the following:

* Integrate core functionality of the autonomous vehicle system, including traffic light detection, control and waypoint following
* The submitted code must work successfully to navigate Carla around the test track

## Rubric Points
### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/1969/view) individually and describe how I addressed each point in my implementation.

---

#### 1. Result in Simulator

As you could see from the following video, the car could drive around the track. The car could properly stop at red light and launch again when the light comes to green.

<a href="https://youtu.be/DCMg_5fCsBM
" target="_blank"><img src="http://img.youtube.com/vi/DCMg_5fCsBM/0.jpg" 
alt="High Way Driving" width="240" height="180" border="10" /></a>

#### 2. Compilation

All the source code compile and run successfully on my local machine (i5-8250 1.60GHz; No GPU). I started using the Virtual Machine and Ubuntu image from Udacity. However the simulator runs really slow and the car would go off road when the camera is on. Since I'm using Windows10, I finally chose to setup the environment to run Ubuntu Bash on Windows and run simulator in Windows. The steps are as following. The usage of the project repo could just follow the repo instruction.

* Install Ubuntu 16.04 from Windows Store. If you don't have access to Windows Store, you could always manually install it [here](https://docs.microsoft.com/en-us/windows/wsl/install-manual)
* Install [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu)
* Download [DBW package](https://github.com/vishal-kvn/CarND-Capstone/tree/docker/ros/src/dbw_mkz_msgs) instead of install [Dataspeed DBW](https://bitbucket.org/DataspeedInc/dbw_mkz_ros). The reason is discussed [here](https://knowledge.udacity.com/questions/42237)

#### 3. Reflection

##### 3.1 Workflow

I followed the project walkthough, to develop waypoint updater partialy without traffic light information first. Then I add DBW node so that the car could drive around the track ignoring the traffic lights. Next is adding traffic light detection using light state directly from simulator and finishing waypoint udpater using the traffic light information. At this point the car is navagitaing the track meeting the requirement. The last step is using computer vision to detect and classify traffic light state.

##### 3.2 Traffic Light Classifier

###### 3.2.1 SSD Model Training

I refrenced [this repo](https://github.com/alex-lechner/Traffic-Light-Classification) for setting up SSD model training on AWS. I chose a different model (ssd_mobilenet_v1_coco_11_06_2017) because I found this one could identify image pretty fast and accurate on my computer, considering my computer doesn't have GPU. The key files for training could be found [here](https://github.com/Yongtao-Li/CarND-Object-Detection-Lab), including data file, lable file and mobilenet model.

###### 3.2.2 SSD Model Testing

Please see my [traffic light classifier notebook](https://github.com/Yongtao-Li/CarND-Object-Detection-Lab/blob/master/tlDetector.ipynb) for more details. The frozen model could identify the red light pretty well from the simulator image.

###### 3.2.2 SSD Model Integration
Even though the mobilenet model is fast, I still have to slow down the image processing frequency. I think the image comes in from simulator at 10 Hz, but I only process every 5th image, otherwise the car wouldn't stop properly or stay on road. I think it would perform even better with higher performance computer.



# TennisBallCollector
Tennis ball collector is a robot which detects tennis balls on the ground and collects them.

Abstract:

Tennis players can easily do exercise together, but tennis could be a bit hard to exercise individually. Since tennis is a two-player game, when we decide to play individually, we may need some extra tools. For instance, a tennis ball thrower machine. In this project, we design a tennis ball collector robot which will be very helpful for tennis players and tennis courts. The tennis ball collector machine is an assistant robot for tennis players which helps collect tennis balls automatically and sort them according to their colours. The robot has a camera to detect the balls using image processing techniques, and a tracking system to get closer to the balls. Also, there is a sorting function in the robot. All of these functionalities are done using proper software and hardware parts such as image processing algorithms on raspberry-pi with openCV. Overall, this project is designed to support tennis sports and tennis players.

SYSTEM DESIGN:

1. Hardware System Design:

Throwing mechanism consists of two drone motors (brushless DC motor)

![image](https://user-images.githubusercontent.com/37505916/142758339-9f68be74-f2ac-49d6-8ef1-6c090c926413.png)

![Picture1](https://user-images.githubusercontent.com/37505916/142758468-77a719fe-5d63-4fbd-b067-3ae02fc44553.gif)

Other parts of mechanism: 2 electronic speed controller(ESC), 1 lipo battery, raspberry-pi, camera module, 1 motor driver circuit for mover wheels, 2 car wheel, 2 ball casters (sarhoş tekerlek) 1 for front 1 for rear, basket for ball collecting.

![image](https://user-images.githubusercontent.com/37505916/142758648-070097c0-8770-4370-a8ef-4923ffdb065f.png)

![image](https://user-images.githubusercontent.com/37505916/142758656-8b446f18-fd73-4a23-9304-45abb87ea74e.png)

2. Software System Design:

In the software part of this project, the python programming language is used for programming. Ball detection algorithm is programmed using OpenCV computer vision library. Ball tracking algorithm [2] implemented using following techniques: 

![image](https://user-images.githubusercontent.com/37505916/142758762-5298030a-7b93-4cca-b532-474f473589cc.png)

Robot performs some actions according to the location of detected balls on the camera. To track the balls in an appropriate manner, balls have to be found in an obtainable position. Following figures show some performing actions according to ball location. 

In this figure the ball is found in the left side of the obtained frame so the robot will perform a turning left action: 

![image](https://user-images.githubusercontent.com/37505916/142758813-ef752584-fb43-4de8-bb48-3c6fb8c67ece.png)

In this figure the ball is found in the middle of the obtained frame so the robot will perform going forward action:

![image](https://user-images.githubusercontent.com/37505916/142758860-47f32315-0d2c-441f-8a5b-e8619d9adb63.png)

In this figure the ball is found in the right side of the obtained frame so the robot will perform a turning right action: 

![image](https://user-images.githubusercontent.com/37505916/142758877-50f84bba-51ab-415d-a6ca-5545c3b9c121.png)

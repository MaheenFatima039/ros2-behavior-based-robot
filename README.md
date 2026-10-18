## Behavior-Based Robot Simulation Using ROS2 and Gazebo
## About my project
I built this robot simulation using Python, ROS2 and Gazebo to explore how sensor information can guide a robot's behavior. I connected LiDAR-based perception with three behaviors: search, follow and stop.
I worked independently on the robot model, simulation setup, perception node and behavior controller. This project is part of my interest in robotics and real-time AI systems, where a system needs to interpret incoming data and respond promptly.
## What I implemented
- I used LiDAR scan data to estimate the distance to the nearest valid return in front of the robot.
- I separated perception and control into two ROS2 nodes that communicate through topics.
- I implemented SEARCH, FOLLOW and STOP behaviors based on target detection, distance and movement-clearance signals.
- I published velocity commands on /cmd_vel to connect the controller to the robot's movement interface.
- I tested the robot's behavior in Gazebo as part of the project.
I treat the nearest valid LiDAR return within the front sector as a target. My perception code does not classify objects or identify a particular person. I implemented the behavior controller using rules and proportional control.
## Files I have included
File	What I use it for
perception_node.py	I process /scan and publish /target_distance, /target_detected and /safe_to_move.
follow_stop_node.py	I select the robot's behavior and publish Twist velocity commands on /cmd_vel.
gazebo.launch.py	I start Gazebo Sim, publish the robot description, request robot spawning and launch both nodes using the installed my_diffbot package.


## The main challenge
I found coordinating the robot's behaviors and publishing the appropriate velocity commands the most challenging part. I needed perception, behavior selection and movement commands to work together consistently.
I approached this by checking the sensor input, testing each behavior and working through the command-publishing path. Repeated simulation runs helped me observe the robot's response and adjust the controller. I kept the controller simple and reactive so I could focus on understanding and validating its behavior.
## Tools I used
I used Python, ROS2 (rclpy), Gazebo Sim, LiDAR scan messages, ROS2 topics and geometry_msgs/msg/Twist. My launch file also uses robot_state_publisher and ros_gz_sim.
## Current repository scope
I have included the two Python nodes and the Gazebo launch file in this repository. Reproducing my complete simulation also requires the ROS2 package setup and the supporting robot and world assets, including:
- package.xml and the package's build/install configuration
- urdf/diffbot.urdf
- worlds/follow_world.sdf
- Any required sensor, drive-controller or ROS-Gazebo bridge configuration

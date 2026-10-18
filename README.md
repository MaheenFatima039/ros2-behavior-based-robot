## Behavior-Based Robot Simulation Using ROS2 and Gazebo

A mobile robot simulation built using Python, ROS2 and Gazebo.
The project combines LiDAR-based perception with search, follow
and stop behaviors.

## Features

- LiDAR-based target detection and distance estimation
- Search, follow and stop behavior control
- Robot movement through velocity commands published to cmd_vel
- Testing in a Gazebo simulation environment

## Project Files

- perception_node.py
- follow_stop_node.py
- gazebo.launch.py

## Development Challenges

The main challenge was coordinating perception, behavior
transitions and velocity-command publishing so the robot
responded consistently.

## Project Status

The current repository contains three Python scripts.
Additional ROS2 package, robot model, world and configuration
files may be needed to reproduce the full simulation.

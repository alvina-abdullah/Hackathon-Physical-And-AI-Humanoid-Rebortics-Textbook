---
title: ROS 2 Communication Primitives
sidebar_label: "Chapter 2: Communication Primitives"
description: Understanding ROS 2 communication primitives - nodes, topics, services, and their applications in humanoid robot control
---

# ROS 2 Communication Primitives

## ROS 2 Nodes: Purpose and Lifecycle

ROS 2 Nodes are the fundamental execution units in the ROS 2 system. Each node is an independent process that performs a specific function within the robot system. Nodes encapsulate functionality and provide a way to organize robot software into modular, reusable components.

### Node Purpose
- Encapsulate specific functionality (e.g., sensor driver, controller, algorithm)
- Provide a communication context for topics, services, and parameters
- Enable distributed computing across multiple processes and machines
- Facilitate independent development and testing of robot components

### Node Lifecycle
ROS 2 nodes follow a well-defined lifecycle with several states:
- **Unconfigured**: Initial state after node creation
- **Inactive**: Configured but not yet activated
- **Active**: Running and participating in communication
- **Finalized**: Shutting down and cleaning up resources

## Topics: Publish/Subscribe Communication

Topics enable asynchronous, many-to-many communication in ROS 2. They use a publish/subscribe pattern where publishers send messages to a topic and subscribers receive messages from the topic without direct knowledge of each other.

### Topic Characteristics
- **Asynchronous**: Publishers and subscribers don't need to run simultaneously
- **Many-to-many**: Multiple publishers can send to a topic, multiple subscribers can receive
- **Typed messages**: All messages on a topic must conform to a specific message type
- **Decoupled**: Publishers and subscribers are independent of each other

### Practical Use in Humanoid Robots
- Joint state information (published by hardware interface, subscribed by controllers)
- Sensor data streams (IMU, cameras, LiDAR)
- Robot state information (battery level, temperature, operational status)

## Services: Request/Response Interactions

Services provide synchronous, one-to-one communication for request/response interactions. Unlike topics, services require a direct connection between client and server, and the interaction is blocking until a response is received.

### Service Characteristics
- **Synchronous**: Client waits for response from server
- **One-to-one**: Direct communication between client and server
- **Request/Response**: Defined message types for both request and response
- **Blocking**: Client is blocked until response is received or timeout occurs

### Practical Use in Humanoid Robots
- Calibration procedures (request calibration, receive confirmation)
- Action execution (request specific action, receive success/failure)
- Configuration changes (request parameter update, receive acknowledgment)

## Practical Mental Models for Humanoid Robot Control Flows

### Control Hierarchy Model
```
High-Level Planner (Path Planning, Task Planning)
    ↓ (Commands/Tasks)
Low-Level Controllers (Joint, Trajectory, Impedance Controllers)
    ↓ (Commands)
Hardware Interface (Motor Drivers, Sensor Interfaces)
    ↑ (Feedback: Joint States, Sensor Data)
```

### Communication Patterns in Control
1. **Continuous Data Flow**: Topics for sensor data and joint states
2. **Command Execution**: Services for discrete actions and configuration
3. **Feedback Integration**: Topics for continuous monitoring and adjustment

## Real-World Examples

### Joint Control Example
- **Topic**: `/joint_states` - Published by hardware interface, subscribed by controllers
- **Topic**: `/joint_commands` - Published by controllers, subscribed by hardware interface
- **Service**: `/calibrate_joint` - Request calibration, receive success/failure response

### Sensor Feedback Example
- **Topic**: `/imu/data` - Continuous stream of inertial measurement data
- **Topic**: `/camera/image_raw` - Image stream from robot's camera
- **Service**: `/set_camera_params` - Configure camera parameters on demand

## Diagram: Communication Primitives Overview

```
[Node A] ---- publishes to ----> [Topic] <---- subscribes from ---- [Node B]
    |                              |                               |
    |                              |                               |
    |---- requests from ----> [Service] <---- provides to ---- [Node C]
```
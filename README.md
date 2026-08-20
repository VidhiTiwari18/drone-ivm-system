# AI-Based Drone Inventory Management System

## Project Demonstration Video

🎥 [Watch Complete Project Demo](https://www.linkedin.com/posts/vidhi-tiwari-a8b882290_machinelearning-dronetech-ai-ugcPost-7455598492288397312-kLQN/)

## Overview

This project is an AI-based Drone Inventory Management System developed as my major project.

The project combines a custom-assembled drone, computer vision, and a web-based inventory management system to assist with inventory monitoring and item identification.

The drone hardware was assembled and integrated using components such as Pixhawk 2.4.8, GPS, Raspberry Pi, camera module, brushless motors, ESCs, propellers, battery, and Wi-Fi module.

On the software side, the system uses YOLOv5 and OpenCV for computer vision and barcode/QR detection. The detected information is connected with a Flask backend and SQLite database for inventory management.

## Hardware Used

- Drone Frame
- Pixhawk 2.4.8 Flight Controller
- GPS Module
- Raspberry Pi
- Camera Module
- Brushless DC Motors
- ESC (Electronic Speed Controller)
- Propellers
- Battery
- Wi-Fi Module

## Features

- Custom drone hardware assembly
- Drone-assisted inventory scanning
- Object detection using YOLOv5
- Barcode and QR code detection using camera input
- Real-time inventory tracking
- Automated item identification
- Inventory database management
- Web-based inventory dashboard

## Technologies Used

### Hardware

- Pixhawk 2.4.8
- Raspberry Pi
- GPS Module
- Camera Module
- Brushless DC Motors
- ESC
- Wi-Fi Module

### Software

- Python
- OpenCV
- YOLOv5
- Flask
- SQLite
- HTML
- CSS
- JavaScript

## Project Structure

backend/
    Backend application and database

scanner.py
    QR/Barcode scanner

yolo_barcode_integration.py
    YOLO and barcode integration

test_camera.py
    Camera testing module

## How It Works

1. The drone hardware is assembled and the required components are integrated.
2. Pixhawk 2.4.8 and the GPS module are used as part of the drone system.
3. Raspberry Pi and the camera module provide the computing and image input.
4. YOLOv5 and OpenCV process the camera input.
5. Objects and barcode/QR information are detected.
6. The detected information is handled by the backend.
7. Inventory information is stored in SQLite.
8. The inventory can be viewed and managed through the web interface.

## Future Scope

1. Autonomous drone navigation
2. Warehouse automation
3. Cloud-based monitoring dashboard
4. Improved object detection
5. Real-time telemetry monitoring

## Author

**Vidhi Tiwari**

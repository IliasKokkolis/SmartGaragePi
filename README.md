# SmartGaragePi
An IoT implementation of a Smart Garage using Raspberry Pi

This project was done for my Thesis @ University of Piraeus , Department of Digital Systems

Raspberry Pi 3 was used for the testing and Flask for the Web App

It's a simple IoT implementation utilizing the power of PI's GPIO pins and modules , where the user has the ability to remotely control multiple Raspberry Pi sensors inside his garage.

The project includes:

* An alarm system consisting of a camera , motion sensor and a buzzer.
* A humidity and temperature sensor.
* LED controllable lights.
* Live video feed from the garage with the Raspberry Pi camera module.

Pushbullet API was also used to push a notification ( including an image of the intruder ) whenever the alarm system detects movement.

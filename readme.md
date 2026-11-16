#My Project

This project involves 2 robot hands which play Super Mario Brothers 1985. I am using ultrasonic sensors connected to an STM32F407 Discovery board, since the thumbs of the robotic hands are not able to bring enough energy to push a button. Additionally they slip when they touch the button due to the PET material being used to manufacture the thumbs. The STM32 is connected to the PC as an HMI-Compliant Keyboard with one ultrasonic sensor input being mapped to an arbritary button for jump and the other for move forward or run.

The fingers are controlled by servo motors which are connected to a Raspberry-Pi. The Pi is connected to a camera, which takes pictures and sends to the Pi at every 200 milliseconds, and the Pi runs a YOLOv5 detection model, trained on about 1000 images of the first level of Super Mario Bros. 1985.

The ultrasonic sensors are unfortunately extremely sensitive to external disturbance and I had to reset them after a while, since they would just stop sending information to the microcontroller.

Here's a video showcasing my project

[https://drive.google.com/file/d/1ZuYar5z8jymCCTQ8Jl2b4bx6na2mwOWn/view?usp=sharing](https://drive.google.com/file/d/1ZuYar5z8jymCCTQ8Jl2b4bx6na2mwOWn/view?usp=sharing)

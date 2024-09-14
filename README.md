**Project Overview**

This project involves using a Raspberry Pi Pico W to build a simple echo sounder with the Airmar DT800 transducer. The goal is to:

1. Display Depth Data: Read depth data transmitted via an RS485 cable and display it on a small LCD screen.
2. Store Data: Save the depth data in real-time to an SD card.
3. Export Data: Output the depth data to a serial port through a DB9 connector for integration with computer programs such as Hypack, HydroPro, or Hydromagic.

**Wiring Diagram**

![alt text](https://github.com/pbroboto/Pico-Echo-Sounder/blob/main/airmar-d800-pico-w-_bb-scaled.jpg?raw=true)

![alt text](https://github.com/pbroboto/Pico-Echo-Sounder/blob/main/IMG_20240714_165123-scaled.jpg?raw=true)

**Testing Procedure**

For testing, I used the Airmar DT800 transducer, which was connected to a 4-cell 11.1V LiPo battery. During charging, the battery voltage measured 13.2V, which is acceptable since the transducer operates within a range of 10V to 25V. I connected the A and B data cables to a 2.5mm jack and inserted it into the male jack. A corresponding female jack of the same size was used to receive the signal and pass it to the RS485 to TTL circuit.

The circuit board was powered using a USB power bank connected via a USB cable. I then placed the transducer in a home water tank and monitored the depth readings on the LCD screen. Although the water level in the tank remained constant, the depth reading fluctuated by approximately ±3 cm. I also varied the depth by moving the cable up and down, and the LCD screen continued to show acceptable results.

![alt text](https://github.com/pbroboto/Pico-Echo-Sounder/blob/main/IMG_20240720_140323-1024x461.jpg?raw=true)


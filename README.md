**Project Overview**

This project involves using a Raspberry Pi Pico W to build a simple echo sounder with the Airmar DT800 transducer. The goal is to:

1. Display Depth Data: Read depth data transmitted via an RS485 cable and display it on a small LCD screen.
2. Store Data: Save the depth data in real-time to an SD card.
3. Export Data: Output the depth data to a serial port through a DB9 connector for integration with computer programs such as Hypack, HydroPro, or Hydromagic.

**Wiring Diagram**

![alt text](https://github.com/pbroboto/Pico-Echo-Sounder/blob/main/airmar-d800-pico-w-_bb-scaled.jpg?raw=true)

**Devices in Use:**

1. Airmar DT800 Transducer (x1)
2. Raspberry Pi Pico Wireless Microcontroller (x1)
3. 1602 LCD Display with IIC/I2C Interface (x1)
4. Micro SD/SDHC Card Adapter Module (SPI) (x1)
5. RS485 to TTL Converter (MAX485) (x1)
6. RS232 to TTL Converter (MAX3232) (x1)
7. Dupont Connectors (assorted)
8. Breadboard/Protoboard (x1)

![alt text](https://github.com/pbroboto/Pico-Echo-Sounder/blob/main/IMG_20240714_165123-scaled.jpg?raw=true)

**Testing Procedure**

For testing, I used the Airmar DT800 transducer, which was connected to a 4-cell 11.1V LiPo battery. During charging, the battery voltage measured 13.2V, which is acceptable since the transducer operates within a range of 10V to 25V. I connected the A and B data cables to a 2.5mm jack and inserted it into the male jack. A corresponding female jack of the same size was used to receive the signal and pass it to the RS485 to TTL circuit.

The circuit board was powered using a USB power bank connected via a USB cable. I then placed the transducer in a home water tank and monitored the depth readings on the LCD screen. Although the water level in the tank remained constant, the depth reading fluctuated by approximately ±3 cm. I also varied the depth by moving the cable up and down, and the LCD screen continued to show acceptable results.

![alt text](https://github.com/pbroboto/Pico-Echo-Sounder/blob/main/IMG_20240720_140323-1024x461.jpg?raw=true)

**Testing with Hypack**

I tested the Pico Echo Sounder with Hypack software on a Windows desktop. To do this, I opened the Hypack program on my laptop and configured it to work with the Pico Echo Sounder by selecting the nmea.dll driver in the depth selection dialog box and choosing $SDDBT. I set the port parameters to 4800 baud, 8 data bits, no parity, and 1 stop bit, using a USB-to-serial adapter. The test was successful, with the $SDDBT string appearing periodically in accordance with the baud rate settings. It’s important to note that the depth displayed is from the transducer head, not the water surface. To obtain the depth from the water surface, you will need to account for the draft value.

**Conclusion**

One limitation of the Airmar DT800 transducer is the lack of an API to adjust the draft sound velocity in water. As a result, this experimental echo sounder is best suited for shallow water applications, with a maximum depth of around 25 meters. Due to this constraint, it is not recommended for high-resolution or survey-grade purposes.

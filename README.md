# EMG_Prototype
A simple two electrode EMG from scratch
I designed this as a challenge to myself. I am a student of Biochemistry and I want to study 
brain computer interfaces. As a resut learning the circuitry and many varied tools that 
are involved in circuit design and electronics is up to me at the present.

This project was a study of operational amplifiers as well as the nature of myo-electric signals. 
It utilizes an Instrumental Amp for signal aquisition and a dual op-amp for a first order band pass filter 
at about 10Hz to 500Hz.

I am currently working on more software that can add application and utility to signal processing.


Connections:
This project is intended for use with an Arduino over a Serial connection at present. 
Though the pin pairs of labeled intention is that 

Power: 
Power would supply a 5V potential across the two pins from an external power supply.

Electrodes:
The center four pins are intended to be used with three electrodes with the last pin being
a ground for the purpose of shielding in the wires. 

Voltage Read:
Last the Voltage read pins will go into the Arduino GND and A0

Suggestions are welcome and feel free to contact me at 

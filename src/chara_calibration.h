#ifndef CHARA_CALIBRATION_H
#define CHARA_CALIBRATION_H

// Function to calibrate and convert raw ADC value to actual voltage
float calibrateVoltage(int raw);

// Function to calibrate ADC value to angle in degrees
float calibrateAngle(int raw);

#endif // CHARA_CALIBRATION_H


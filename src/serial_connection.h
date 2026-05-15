#ifndef SERIAL_CONNECTION_H
#define SERIAL_CONNECTION_H

#include <Arduino.h>

void initSerial(unsigned long baudRate = 115200);
void printMeasuredData(int adcPin, int raw, float voltage, float angle);

#endif // SERIAL_CONNECTION_H

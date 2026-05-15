#include <Arduino.h>
#include "chara_calibration.h"
#include "serial_connection.h"

const int adcPin = 15; // Use a valid ADC pin on the ESP32 (ADC1 channel 6)

void setup() {
  initSerial(115200);

  analogReadResolution(12);      // 12-bit ADC (0-4095)
  analogSetPinAttenuation(adcPin, ADC_11db); // Full-scale range up to ~3.3V
}

void loop() {
  // Average 10 readings for better precision
  long sum = 0;
  const int numSamples = 10;
  for (int i = 0; i < numSamples; i++) {
    sum += analogRead(adcPin);
    delay(1); // Small delay between readings
  }
  int raw = sum / numSamples;

  float voltage = calibrateVoltage(raw); // Use calibrated voltage calculation
  float angle = calibrateAngle(raw);     // Use calibrated angle calculation

  printMeasuredData(adcPin, raw, voltage, angle);

  delay(100);
}


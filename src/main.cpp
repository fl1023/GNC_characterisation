#include <Arduino.h>
#include "chara_calibration.h"
#include "serial_connection.h"

const int adcPin = 15; // Use a valid ADC pin on the ESP32 (ADC1 channel 6)

void setup() {
  initSerial(230400);

  analogReadResolution(12);      // 12-bit ADC (0-4095)
  analogSetPinAttenuation(adcPin, ADC_11db); // Full-scale range up to ~3.3V
}

void loop() {
  // Average a few readings for better precision while keeping the loop fast.
  long sum = 0;
  const int numSamples = 4;
  for (int i = 0; i < numSamples; i++) {
    sum += analogRead(adcPin);
  }
  int raw = sum / numSamples;

  float voltage = calibrateVoltage(raw); // Use calibrated voltage calculation
  float angle = calibrateAngle(raw);     // Use calibrated angle calculation

  printMeasuredData(adcPin, raw, voltage, angle);

  // Target ~100 Hz loop rate.
  static unsigned long nextWake = 0;
  if (nextWake == 0) {
    nextWake = millis();
  }
  nextWake += 10;
  if (nextWake > millis()) {
    delay(nextWake - millis());
  }
}


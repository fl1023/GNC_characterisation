#include "serial_connection.h"

void initSerial(unsigned long baudRate) {
    Serial.begin(baudRate);
    delay(1000);

#if defined(ARDUINO_ARCH_AVR) || defined(ARDUINO_ARCH_SAMD) || defined(ARDUINO_ARCH_STM32)
    while (!Serial) {
        delay(10);
    }
#endif
}

void printMeasuredData(int adcPin, int raw, float voltage, float angle) {
    Serial.print("ADC pin ");
    Serial.print(adcPin);
    Serial.print(" raw = ");
    Serial.print(raw);
    Serial.print("  voltage = ");
    Serial.print(voltage, 3);
    Serial.print(" V");
    Serial.print("  angle = ");
    Serial.print(angle, 1);
    Serial.println(" deg");
}

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
    char buf[128];
    int len = snprintf(
        buf,
        sizeof(buf),
        "ADC pin %d raw = %d  voltage = %.3f V  angle = %.1f deg\n",
        adcPin,
        raw,
        voltage,
        angle);
    if (len > 0) {
        Serial.write(reinterpret_cast<const uint8_t *>(buf), len);
    }
}

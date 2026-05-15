#include "chara_calibration.h"

// Calibration data points: {ADC, Angle}
const int numPoints = 6;
const float adcPoints[numPoints] = {0.0f, 365.0f, 1136.0f, 1187.0f, 2285.0f, 4095.0f};
const float anglePoints[numPoints] = {0.0f, 45.0f, 90.0f, 135.0f, 180.0f, 360.0f};

// Calibrates the voltage based on ADC reading
// ADC measures up to 3.3V, but actual input is 4.6V
float calibrateVoltage(int raw) {
    // First, convert raw ADC to measured voltage (assuming 3.3V full scale)
    float measuredVoltage = raw * (3.3f / 4095.0f);
    
    // Scale to actual input voltage (4.6V)
    float actualVoltage = measuredVoltage * (4.60f / 3.3f);
    
    return actualVoltage;
}

// Calibrates ADC value to angle using piecewise linear interpolation
float calibrateAngle(int raw) {
    float rawF = (float)raw;
    
    // Clamp raw to valid range
    if (rawF <= adcPoints[0]) return anglePoints[0];
    if (rawF >= adcPoints[numPoints - 1]) return anglePoints[numPoints - 1];
    
    // Find the interval
    for (int i = 0; i < numPoints - 1; i++) {
        if (rawF >= adcPoints[i] && rawF <= adcPoints[i + 1]) {
            // Linear interpolation
            float adcDiff = adcPoints[i + 1] - adcPoints[i];
            float angleDiff = anglePoints[i + 1] - anglePoints[i];
            float ratio = (rawF - adcPoints[i]) / adcDiff;
            return anglePoints[i] + ratio * angleDiff;
        }
    }
    
    // Should not reach here
    return 0.0f;
}
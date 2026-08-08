#pragma once

#include <Arduino.h>

namespace StatusLed {

constexpr uint8_t RED_PIN = 25;
constexpr uint8_t GREEN_PIN = 26;
constexpr uint8_t BLUE_PIN = 27;

void begin();
void off();
void blue();
void green();
void yellow();

}  // namespace StatusLed


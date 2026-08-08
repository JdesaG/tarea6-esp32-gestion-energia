#pragma once

#include <Arduino.h>
#include <esp_sleep.h>

namespace PowerManager {

constexpr gpio_num_t WAKEUP_PIN = GPIO_NUM_33;
constexpr uint64_t MICROSECONDS_PER_SECOND = 1000000ULL;
constexpr uint32_t SLEEP_SECONDS = 10;

const char *wakeCauseLabel(esp_sleep_wakeup_cause_t cause);
void configureWakeupSources();
void enterDeepSleep();

}  // namespace PowerManager


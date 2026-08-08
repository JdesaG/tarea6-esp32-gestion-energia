#include <Arduino.h>
#include <driver/rtc_io.h>

#include "power_manager.h"
#include "status_led.h"

RTC_DATA_ATTR uint32_t bootCount = 0;
RTC_DATA_ATTR uint32_t timerWakeCount = 0;
RTC_DATA_ATTR uint32_t externalWakeCount = 0;

static void registerWakeup(const esp_sleep_wakeup_cause_t cause) {
  if (cause == ESP_SLEEP_WAKEUP_TIMER) {
    ++timerWakeCount;
  } else if (cause == ESP_SLEEP_WAKEUP_EXT0) {
    ++externalWakeCount;
  }
}

static void printStartupReport(const esp_sleep_wakeup_cause_t cause) {
  Serial.println();
  Serial.println("========================================");
  Serial.println(" TAREA 6 - GESTION DE ENERGIA ESP32");
  Serial.println("========================================");
  Serial.printf("BOOT=%u\n", bootCount);
  Serial.printf("CAUSA=%s\n", PowerManager::wakeCauseLabel(cause));
  Serial.printf("CONTADORES timer=%u, ext0=%u\n", timerWakeCount,
                externalWakeCount);
}

static void runActiveTask() {
  Serial.println("ESTADO=ACTIVO | LED verde | Tarea de 5 segundos.");
  for (uint8_t second = 1; second <= 5; ++second) {
    StatusLed::green();
    Serial.printf("TAREA_ACTIVA=%u/5\n", second);
    delay(700);
    StatusLed::off();
    delay(300);
  }
  Serial.println("TAREA_COMPLETADA");
}

static void prepareForSleep() {
  StatusLed::yellow();
  Serial.println("ESTADO=PREPARANDO_SLEEP | LED amarillo.");
  PowerManager::configureWakeupSources();
  delay(1000);
  StatusLed::off();
}

void setup() {
  Serial.begin(115200);
  delay(250);

  const esp_sleep_wakeup_cause_t wakeCause = esp_sleep_get_wakeup_cause();
  if (wakeCause == ESP_SLEEP_WAKEUP_EXT0) {
    rtc_gpio_deinit(PowerManager::WAKEUP_PIN);
  }

  StatusLed::begin();
  ++bootCount;
  registerWakeup(wakeCause);
  printStartupReport(wakeCause);

  StatusLed::blue();
  Serial.println("ESTADO=DESPIERTO | LED azul.");
  delay(1000);

  runActiveTask();
  prepareForSleep();
  PowerManager::enterDeepSleep();
}

void loop() {
  // Deep sleep reinicia la ejecucion desde setup(), por eso loop no se usa.
}


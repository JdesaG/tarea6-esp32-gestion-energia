#include "power_manager.h"

#include <driver/rtc_io.h>

namespace PowerManager {

const char *wakeCauseLabel(const esp_sleep_wakeup_cause_t cause) {
  switch (cause) {
    case ESP_SLEEP_WAKEUP_EXT0:
      return "pin externo EXT0 (GPIO33)";
    case ESP_SLEEP_WAKEUP_TIMER:
      return "temporizador RTC";
    case ESP_SLEEP_WAKEUP_UNDEFINED:
      return "encendido o reinicio, no deep sleep";
    default:
      return "otra fuente de despertar";
  }
}

static void requireEspOk(const esp_err_t result, const char *operation) {
  if (result == ESP_OK) {
    return;
  }

  Serial.printf("ERROR: %s fallo (codigo %d).\n", operation, result);
  Serial.flush();
  while (true) {
    delay(1000);
  }
}

static void waitForButtonRelease() {
  bool warningPrinted = false;
  while (digitalRead(WAKEUP_PIN) == LOW) {
    if (!warningPrinted) {
      Serial.println("Suelte el pulsador para evitar un despertar inmediato.");
      warningPrinted = true;
    }
    delay(20);
  }
}

void configureWakeupSources() {
  pinMode(WAKEUP_PIN, INPUT_PULLUP);
  waitForButtonRelease();

  requireEspOk(
      esp_sleep_enable_timer_wakeup(SLEEP_SECONDS * MICROSECONDS_PER_SECOND),
      "configurar el temporizador RTC");
  requireEspOk(esp_sleep_enable_ext0_wakeup(WAKEUP_PIN, LOW),
               "configurar EXT0");

  // EXT0 usa el dominio RTC; el pull-up mantiene un nivel estable en reposo.
  rtc_gpio_pullup_en(WAKEUP_PIN);
  rtc_gpio_pulldown_dis(WAKEUP_PIN);

  Serial.printf("Despertar configurado: TIMER=%us o EXT0=GPIO%d en LOW.\n",
                SLEEP_SECONDS, WAKEUP_PIN);
}

void enterDeepSleep() {
  Serial.println("ESTADO=SLEEP | Entrando en deep sleep.");
  Serial.flush();
  esp_deep_sleep_start();
}

}  // namespace PowerManager


#include <Arduino.h>
#include <driver/rtc_io.h>
#include <esp_sleep.h>

constexpr gpio_num_t WAKEUP_PIN = GPIO_NUM_33;
constexpr uint8_t RED_PIN = 25;
constexpr uint8_t GREEN_PIN = 26;
constexpr uint8_t BLUE_PIN = 27;
constexpr uint32_t SLEEP_SECONDS = 10;
constexpr uint64_t MICROSECONDS_PER_SECOND = 1000000ULL;

RTC_DATA_ATTR uint32_t bootCount = 0;
RTC_DATA_ATTR uint32_t timerWakeCount = 0;
RTC_DATA_ATTR uint32_t externalWakeCount = 0;

void setLed(bool red, bool green, bool blue) {
  digitalWrite(RED_PIN, red ? HIGH : LOW);
  digitalWrite(GREEN_PIN, green ? HIGH : LOW);
  digitalWrite(BLUE_PIN, blue ? HIGH : LOW);
}

const char *wakeCauseLabel(esp_sleep_wakeup_cause_t cause) {
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

void configureWakeupSources() {
  pinMode(WAKEUP_PIN, INPUT_PULLUP);
  while (digitalRead(WAKEUP_PIN) == LOW) {
    Serial.println("Suelte el pulsador para evitar un despertar inmediato.");
    delay(100);
  }

  esp_sleep_enable_timer_wakeup(SLEEP_SECONDS * MICROSECONDS_PER_SECOND);
  esp_sleep_enable_ext0_wakeup(WAKEUP_PIN, LOW);
  rtc_gpio_pullup_en(WAKEUP_PIN);
  rtc_gpio_pulldown_dis(WAKEUP_PIN);
  Serial.printf("Despertar configurado: TIMER=%us o EXT0=GPIO%d en LOW.\n",
                SLEEP_SECONDS, WAKEUP_PIN);
}

void runActiveTask() {
  Serial.println("ESTADO=ACTIVO | LED verde | Tarea de 5 segundos.");
  for (uint8_t second = 1; second <= 5; ++second) {
    setLed(false, true, false);
    Serial.printf("TAREA_ACTIVA=%u/5\n", second);
    delay(700);
    setLed(false, false, false);
    delay(300);
  }
  Serial.println("TAREA_COMPLETADA");
}

void setup() {
  Serial.begin(115200);
  delay(250);

  const esp_sleep_wakeup_cause_t cause = esp_sleep_get_wakeup_cause();
  if (cause == ESP_SLEEP_WAKEUP_EXT0) {
    rtc_gpio_deinit(WAKEUP_PIN);
    ++externalWakeCount;
  } else if (cause == ESP_SLEEP_WAKEUP_TIMER) {
    ++timerWakeCount;
  }

  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  ++bootCount;

  Serial.println("========================================");
  Serial.println(" TAREA 6 - GESTION DE ENERGIA ESP32");
  Serial.println("========================================");
  Serial.printf("BOOT=%u\n", bootCount);
  Serial.printf("CAUSA=%s\n", wakeCauseLabel(cause));
  Serial.printf("CONTADORES timer=%u, ext0=%u\n", timerWakeCount,
                externalWakeCount);

  setLed(false, false, true);
  Serial.println("ESTADO=DESPIERTO | LED azul.");
  delay(1000);
  runActiveTask();

  setLed(true, true, false);
  Serial.println("ESTADO=PREPARANDO_SLEEP | LED amarillo.");
  configureWakeupSources();
  delay(1000);
  setLed(false, false, false);

  Serial.println("ESTADO=SLEEP | Entrando en deep sleep.");
  Serial.flush();
  esp_deep_sleep_start();
}

void loop() {}


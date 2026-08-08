#include "status_led.h"

namespace StatusLed {

static void set(const bool red, const bool green, const bool blue) {
  digitalWrite(RED_PIN, red ? HIGH : LOW);
  digitalWrite(GREEN_PIN, green ? HIGH : LOW);
  digitalWrite(BLUE_PIN, blue ? HIGH : LOW);
}

void begin() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  off();
}

void off() { set(false, false, false); }
void blue() { set(false, false, true); }
void green() { set(false, true, false); }
void yellow() { set(true, true, false); }

}  // namespace StatusLed


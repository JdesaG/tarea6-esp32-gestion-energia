#!/usr/bin/env python3
"""Validacion reproducible de la coherencia entre firmware y circuito Wokwi."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[OK] {message}")


diagram = json.loads((ROOT / "diagram.json").read_text())
main = (ROOT / "src/main.cpp").read_text()
power = (ROOT / "src/power_manager.cpp").read_text()
header = (ROOT / "include/power_manager.h").read_text()
web_sketch = (ROOT / "wokwi-web/sketch.ino").read_text()
wokwi_config = (ROOT / "wokwi.toml").read_text()
readme = (ROOT / "README.md").read_text()

part_ids = {part["id"] for part in diagram["parts"]}
require(
    {"esp", "rgb1", "btnWake", "rRed", "rGreen", "rBlue", "rPullup"}
    <= part_ids,
    "el diagrama contiene ESP32, RGB, pulsador y cuatro resistencias",
)

connections = {frozenset(connection[:2]) for connection in diagram["connections"]}
expected_connections = [
    ("esp:D25", "rRed:1"),
    ("esp:D26", "rGreen:1"),
    ("esp:D27", "rBlue:1"),
    ("esp:D33", "btnWake:1.l"),
    ("btnWake:2.l", "esp:GND.2"),
    ("esp:3V3", "rPullup:1"),
    ("rPullup:2", "esp:D33"),
]
for endpoints in expected_connections:
    require(
        frozenset(endpoints) in connections,
        f"conexion presente: {endpoints[0]} <-> {endpoints[1]}",
    )

require("GPIO_NUM_33" in header, "EXT0 usa el GPIO33 con capacidad RTC")
require(
    "esp_sleep_enable_timer_wakeup" in power,
    "el firmware configura el despertar por temporizador",
)
require(
    "esp_sleep_enable_ext0_wakeup" in power,
    "el firmware configura el despertar externo EXT0",
)
require(
    "esp_deep_sleep_start" in power,
    "el firmware entra explicitamente en deep sleep",
)
require("RTC_DATA_ATTR" in main, "los contadores se conservan en memoria RTC")
require("SLEEP_SECONDS = 10" in header, "el reposo temporizado dura 10 segundos")

for api in (
    "esp_sleep_enable_timer_wakeup",
    "esp_sleep_enable_ext0_wakeup",
    "esp_deep_sleep_start",
):
    require(api in web_sketch, f"la variante Wokwi Online incluye {api}")

require(
    '.pio/build/esp32dev/firmware.bin' in wokwi_config,
    "wokwi.toml apunta al firmware PlatformIO",
)
require(
    "https://wokwi.com/projects/471748304593999873" in readme,
    "README contiene el enlace publico de Wokwi",
)
require(
    "https://github.com/JdesaG/tarea6-esp32-gestion-energia" in readme,
    "README contiene el enlace del repositorio GitHub",
)

print("\nVALIDACION COMPLETADA: todas las comprobaciones pasaron.")


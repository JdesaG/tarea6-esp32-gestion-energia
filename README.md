# Tarea 6 - Gestion de energia con ESP32

Proyecto PlatformIO/Arduino que ejecuta una tarea activa durante cinco segundos,
entra automaticamente en `deep sleep` y despierta por la primera fuente que se
active:

- Temporizador RTC: 10 segundos.
- Pulsador externo: GPIO33 a nivel bajo mediante `ext0`.

## Enlaces del proyecto

- **Simulacion Wokwi Online:** https://wokwi.com/projects/471748304593999873
- **Repositorio GitHub:** https://github.com/JdesaG/tarea6-esp32-gestion-energia

El contador de arranques y los contadores por causa se guardan en memoria RTC.
El monitor serial informa cada transicion y un LED RGB muestra el estado:

| Color | Estado |
|---|---|
| Azul | Arranque o despertar |
| Verde intermitente | Tarea activa |
| Amarillo | Preparacion para deep sleep |
| Apagado | Deep sleep |

## Circuito

- ESP32 DevKit v1.
- LED RGB de catodo comun.
- GPIO25 -> 220 ohm -> rojo.
- GPIO26 -> 220 ohm -> verde.
- GPIO27 -> 220 ohm -> azul.
- GPIO33 con resistencia pull-up de 10 kohm a 3.3 V.
- Pulsador entre GPIO33 y GND. En Wokwi tambien responde a la tecla `B`.

El circuito completo esta descrito en `diagram.json` y la configuracion de
simulacion en `wokwi.toml`.

## Compilacion

1. Instalar Visual Studio Code con PlatformIO IDE.
2. Abrir esta carpeta como proyecto.
3. Ejecutar **PlatformIO: Build** o, desde una terminal:

   ```bash
   pio run
   ```

## Simulacion en Wokwi

La forma mas rapida es abrir el enlace de Wokwi Online anterior y pulsar el
boton verde de inicio. La variante web equivalente esta en
`wokwi-web/sketch.ino`.

Para simular directamente el firmware compilado por PlatformIO:

1. Instalar la extension **Wokwi Simulator** en Visual Studio Code.
2. Compilar primero con `pio run`.
3. Presionar `F1` y ejecutar **Wokwi: Start Simulator**.
4. Abrir el monitor serial a 115200 baudios.
5. Para probar el temporizador, no tocar el pulsador: despertara tras 10 s.
6. Para probar `ext0`, pulsar el boton azul (o mantener `B`) mientras el LED
   esta apagado y el monitor muestra `ESTADO=SLEEP`.

## Pruebas automatizadas Wokwi CI

Los escenarios estan en `tests/timer-wakeup.yaml` y
`tests/ext0-wakeup.yaml`. Con un token gratuito de Wokwi CI:

```bash
export WOKWI_CLI_TOKEN="..."
wokwi-cli . --scenario tests/timer-wakeup.yaml --timeout 30000
wokwi-cli . --scenario tests/ext0-wakeup.yaml --timeout 30000
```

La coherencia local entre firmware, pines y diagrama se comprueba sin servicios
externos con:

```bash
python3 tests/validate_project.py
```

## Comportamiento esperado

Al despertar de `deep sleep`, el ESP32 reinicia desde `setup()`. La variable
`bootCount`, marcada con `RTC_DATA_ATTR`, se conserva. El monitor debe mostrar
`CAUSA=temporizador RTC` o `CAUSA=pin externo EXT0 (GPIO33)`, segun el evento
que haya ocurrido primero.

Wokwi permite validar la logica, el cableado virtual y la secuencia temporal,
pero no reproduce con precision el consumo electrico de la placa. Para medir
microamperios se necesita hardware real, retirar o aislar cargas y usar un
instrumento de corriente adecuado.

## Estructura

```text
include/              Cabeceras de los modulos
src/                  Firmware Arduino
tests/                Escenarios de simulacion Wokwi CI
diagram.json          Circuito Wokwi
wokwi.toml            Firmware que carga Wokwi
platformio.ini        Configuracion PlatformIO
```

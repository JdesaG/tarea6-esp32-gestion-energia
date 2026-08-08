#!/usr/bin/env python3
"""Genera el informe PDF de la Tarea 6 con evidencias reproducibles."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/pdf/Informe_Tarea_6_Gestion_Energia_ESP32.pdf"
EVIDENCE = ROOT / "evidencias/generadas"

NAVY = colors.HexColor("#17324D")
TEAL = colors.HexColor("#087E8B")
GREEN = colors.HexColor("#1B7F5A")
YELLOW = colors.HexColor("#F2B134")
RED = colors.HexColor("#C44536")
INK = colors.HexColor("#1D2733")
MUTED = colors.HexColor("#5D6B78")
PALE = colors.HexColor("#EEF4F6")
LINE = colors.HexColor("#C8D3DB")
WHITE = colors.white


def register_fonts() -> None:
    font_dir = Path("/System/Library/Fonts/Supplemental")
    pdfmetrics.registerFont(TTFont("Arial", font_dir / "Arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", font_dir / "Arial Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Courier-New", font_dir / "Courier New.ttf"))


register_fonts()

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="BodyArial",
        parent=styles["BodyText"],
        fontName="Arial",
        fontSize=9.4,
        leading=13.3,
        textColor=INK,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="SmallArial",
        parent=styles["BodyText"],
        fontName="Arial",
        fontSize=8,
        leading=10.5,
        textColor=MUTED,
    )
)
styles.add(
    ParagraphStyle(
        name="TitleArial",
        parent=styles["Title"],
        fontName="Arial-Bold",
        fontSize=27,
        leading=31,
        alignment=TA_LEFT,
        textColor=NAVY,
        spaceAfter=12,
    )
)
styles.add(
    ParagraphStyle(
        name="SubtitleArial",
        parent=styles["Heading2"],
        fontName="Arial",
        fontSize=14,
        leading=19,
        textColor=TEAL,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="H1Arial",
        parent=styles["Heading1"],
        fontName="Arial-Bold",
        fontSize=18,
        leading=22,
        textColor=NAVY,
        spaceBefore=2,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="H2Arial",
        parent=styles["Heading2"],
        fontName="Arial-Bold",
        fontSize=11.5,
        leading=14,
        textColor=TEAL,
        spaceBefore=7,
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="LabelArial",
        parent=styles["BodyText"],
        fontName="Arial-Bold",
        fontSize=8,
        leading=10,
        textColor=MUTED,
        uppercase=True,
    )
)
styles.add(
    ParagraphStyle(
        name="CalloutArial",
        parent=styles["BodyText"],
        fontName="Arial-Bold",
        fontSize=9,
        leading=12.5,
        textColor=NAVY,
    )
)
styles.add(
    ParagraphStyle(
        name="TableArial",
        parent=styles["BodyText"],
        fontName="Arial",
        fontSize=8.2,
        leading=10.5,
        textColor=INK,
    )
)
styles.add(
    ParagraphStyle(
        name="TableHeadArial",
        parent=styles["BodyText"],
        fontName="Arial-Bold",
        fontSize=8.2,
        leading=10,
        textColor=WHITE,
    )
)
styles.add(
    ParagraphStyle(
        name="CodeArial",
        parent=styles["Code"],
        fontName="Courier-New",
        fontSize=7.3,
        leading=9.4,
        textColor=INK,
    )
)


def P(text: str, style: str = "BodyArial") -> Paragraph:
    return Paragraph(text, styles[style])


def heading(number: str, title: str) -> Paragraph:
    return P(f"{number}. {title}", "H1Arial")


def bullet(text: str) -> Paragraph:
    return Paragraph(
        f"<font color='#087E8B'>■</font>&nbsp;&nbsp;{text}",
        styles["BodyArial"],
    )


def make_table(rows, widths, header=True, aligns=None) -> Table:
    converted = []
    for row_index, row in enumerate(rows):
        converted.append(
            [
                cell
                if hasattr(cell, "wrap")
                else P(str(cell), "TableHeadArial" if header and row_index == 0 else "TableArial")
                for cell in row
            ]
        )
    table = Table(converted, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
    ]
    if header:
        commands += [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
        ]
    else:
        commands.append(("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, PALE]))
    if aligns:
        for col, align in enumerate(aligns):
            commands.append(("ALIGN", (col, 0), (col, -1), align))
    table.setStyle(TableStyle(commands))
    return table


def callout(title: str, text: str, color=TEAL) -> Table:
    box = Table(
        [[P(title, "CalloutArial"), P(text, "BodyArial")]],
        colWidths=[38 * mm, 132 * mm],
    )
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE),
                ("BOX", (0, 0), (-1, -1), 0.8, color),
                ("LINEBEFORE", (0, 0), (0, -1), 4, color),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return box


def code_block(text: str) -> Table:
    pre = Preformatted(text.strip(), styles["CodeArial"])
    box = Table([[pre]], colWidths=[170 * mm])
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F7F8")),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return box


def header_footer(canvas, doc) -> None:
    canvas.saveState()
    width, height = A4
    if doc.page > 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, height - 15 * mm, width, 15 * mm, fill=1, stroke=0)
        canvas.setFillColor(WHITE)
        canvas.setFont("Arial-Bold", 8.5)
        canvas.drawString(20 * mm, height - 9.6 * mm, "SISTEMAS EMBEBIDOS | TAREA 6")
        canvas.setFont("Arial", 8)
        canvas.drawRightString(width - 20 * mm, height - 9.6 * mm, "Gestión de energía - ESP32")
    canvas.setStrokeColor(LINE)
    canvas.line(20 * mm, 14 * mm, width - 20 * mm, 14 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Arial", 7.5)
    canvas.drawString(20 * mm, 9.5 * mm, "Proyecto PlatformIO + Wokwi | 07 de agosto de 2026")
    canvas.drawRightString(width - 20 * mm, 9.5 * mm, f"Página {doc.page}")
    canvas.restoreState()


def build_story():
    story = []

    # Cover
    story += [
        Spacer(1, 24 * mm),
        P("SISTEMAS EMBEBIDOS", "LabelArial"),
        Spacer(1, 3 * mm),
        P("Tarea 6", "TitleArial"),
        P("Gestión de energía y modos de ahorro en el ESP32", "SubtitleArial"),
        HRFlowable(width="100%", thickness=3, color=TEAL, spaceAfter=14 * mm),
        callout(
            "SOLUCIÓN",
            "Sistema con tarea activa, señalización mediante LED RGB, entrada automática a <b>deep sleep</b> y despertar por temporizador RTC o pulsador externo EXT0.",
            GREEN,
        ),
        Spacer(1, 18 * mm),
        make_table(
            [
                [P("Asignatura", "TableArial"), P("Sistemas Embebidos", "TableArial")],
                [P("Framework", "TableArial"), P("Arduino sobre PlatformIO", "TableArial")],
                [P("Microcontrolador", "TableArial"), P("ESP32 DevKit v1", "TableArial")],
                [P("Simulación", "TableArial"), P("Wokwi Online y Wokwi para VS Code", "TableArial")],
                [P("Repositorio", "TableArial"), P("github.com/JdesaG/tarea6-esp32-gestion-energia", "TableArial")],
                [P("Fecha", "TableArial"), P("07 de agosto de 2026", "TableArial")],
            ],
            [40 * mm, 130 * mm],
            header=False,
        ),
        Spacer(1, 28 * mm),
        P("Autor / estudiante: JdesaG", "BodyArial"),
        P("Documento de implementación, análisis y evidencias", "SmallArial"),
        PageBreak(),
    ]

    # Summary and requirements
    story += [
        heading("1", "Descripción del ejercicio"),
        P(
            "Se desarrolló un sistema embebido que alterna de forma cíclica entre actividad y bajo consumo. Tras cada arranque o despertar, el ESP32 informa la causa por el puerto serial, indica su estado con un LED RGB, ejecuta una tarea activa de cinco segundos y configura dos fuentes de despertar antes de entrar en deep sleep.",
        ),
        P(
            "La primera fuente que ocurra despierta al microcontrolador: el temporizador RTC después de 10 segundos o un nivel bajo en GPIO33 producido por el pulsador. El despertar desde deep sleep provoca un nuevo arranque desde <font name='Courier-New'>setup()</font>; por ello los contadores se almacenan en memoria RTC con <font name='Courier-New'>RTC_DATA_ATTR</font>.",
        ),
        P("Objetivo de diseño", "H2Arial"),
        bullet("Reducir el tiempo de CPU activa cuando el sistema no tiene una tarea útil que ejecutar."),
        bullet("Combinar un despertar periódico y un evento externo en una implementación verificable."),
        bullet("Separar la lógica de energía, la señalización y el flujo principal en módulos claros."),
        P("Cumplimiento de requisitos", "H2Arial"),
        make_table(
            [
                ["Requisito", "Implementación", "Estado"],
                ["Tarea activa temporizada", "Cinco iteraciones de 1 s con telemetría serial.", "Cumple"],
                ["Modo de ahorro explícito", "Deep sleep mediante esp_deep_sleep_start().", "Cumple"],
                ["Despertar por temporizador", "esp_sleep_enable_timer_wakeup(10 s).", "Cumple"],
                ["Despertar externo", "esp_sleep_enable_ext0_wakeup(GPIO33, LOW).", "Cumple"],
                ["Estados visibles", "LED RGB y mensajes seriales estructurados.", "Cumple"],
                ["Código estructurado", "Módulos power_manager, status_led y main.", "Cumple"],
                ["Simulación Wokwi", "Circuito publicado y archivos VS Code incluidos.", "Cumple"],
            ],
            [50 * mm, 92 * mm, 28 * mm],
        ),
        Spacer(1, 5 * mm),
        callout(
            "DECISIÓN",
            "Se eligió deep sleep porque apaga CPU y periféricos digitales, permite conservar datos RTC y admite el temporizador RTC y EXT0 solicitados.",
            TEAL,
        ),
        PageBreak(),
    ]

    # Circuit
    image_path = EVIDENCE / "wokwi-circuito.png"
    story += [
        heading("2", "Circuito en Wokwi"),
        P(
            "El circuito fue creado y publicado en Wokwi Online. La siguiente imagen es la captura generada por Wokwi para el proyecto público y muestra el cableado almacenado en <font name='Courier-New'>diagram.json</font>.",
        ),
        Spacer(1, 2 * mm),
        Image(str(image_path), width=170 * mm, height=89.25 * mm),
        Spacer(1, 2 * mm),
        P("Figura 1. ESP32, LED RGB, resistencias limitadoras y pulsador EXT0 en Wokwi.", "SmallArial"),
        P("Enlace directo", "H2Arial"),
        P(
            "<link href='https://wokwi.com/projects/471748304593999873' color='#087E8B'><u>https://wokwi.com/projects/471748304593999873</u></link>",
        ),
        P("Conexiones", "H2Arial"),
        make_table(
            [
                ["Señal", "GPIO / conexión", "Función"],
                ["Rojo", "GPIO25 -> 220 ohm -> R", "Preparación para reposo"],
                ["Verde", "GPIO26 -> 220 ohm -> G", "Tarea activa"],
                ["Azul", "GPIO27 -> 220 ohm -> B", "Arranque o despertar"],
                ["Común RGB", "COM -> GND", "LED de cátodo común"],
                ["Wake EXT0", "GPIO33 -> pulsador -> GND", "Despertar al nivel LOW"],
                ["Pull-up", "3.3 V -> 10 kohm -> GPIO33", "Evita entrada flotante"],
            ],
            [34 * mm, 64 * mm, 72 * mm],
        ),
        Spacer(1, 4 * mm),
        callout(
            "INTERACCIÓN",
            "Durante el reposo, se puede hacer clic en el pulsador azul o mantener la tecla <b>B</b>. Si no se pulsa, el temporizador despierta al ESP32 automáticamente.",
            YELLOW,
        ),
        PageBreak(),
    ]

    # Operation
    story += [
        heading("3", "Funcionamiento del sistema"),
        P("Secuencia de estados", "H2Arial"),
        make_table(
            [
                ["Orden", "Estado", "LED", "Duración / salida"],
                ["1", "DESPIERTO", "Azul", "1 s; causa y contadores por serial"],
                ["2", "ACTIVO", "Verde intermitente", "5 s; TAREA_ACTIVA=1/5 ... 5/5"],
                ["3", "PREPARANDO_SLEEP", "Amarillo", "1 s; configura TIMER y EXT0"],
                ["4", "SLEEP", "Apagado", "Hasta 10 s o pulsación externa"],
                ["5", "NUEVO ARRANQUE", "Azul", "Vuelve a setup() y registra la causa"],
            ],
            [18 * mm, 44 * mm, 43 * mm, 65 * mm],
        ),
        P("Causas de despertar", "H2Arial"),
        bullet("<b>Temporizador:</b> el controlador RTC genera el evento después de 10 segundos de reposo."),
        bullet("<b>EXT0:</b> GPIO33 es un GPIO RTC. El pulsador lo lleva a LOW y despierta el chip."),
        bullet("<b>Primer arranque:</b> la causa es indefinida porque todavía no se ha producido deep sleep."),
        P("Tratamiento del pulsador", "H2Arial"),
        P(
            "Antes de dormir, el firmware espera que el pulsador esté liberado. Esto evita entrar al modo de reposo con la condición EXT0 ya activa y despertar inmediatamente. El pull-up externo de 10 kohm y el pull-up RTC mantienen GPIO33 estable durante el reposo.",
        ),
        P("Persistencia RTC", "H2Arial"),
        P(
            "Se mantienen tres variables: número total de arranques, despertares por temporizador y despertares por EXT0. Esta información permite verificar el comportamiento después de cada reinicio provocado por deep sleep.",
        ),
        code_block(
            "RTC_DATA_ATTR uint32_t bootCount = 0;\n"
            "RTC_DATA_ATTR uint32_t timerWakeCount = 0;\n"
            "RTC_DATA_ATTR uint32_t externalWakeCount = 0;\n\n"
            "esp_sleep_enable_timer_wakeup(10ULL * 1000000ULL);\n"
            "esp_sleep_enable_ext0_wakeup(GPIO_NUM_33, LOW);\n"
            "esp_deep_sleep_start();"
        ),
        PageBreak(),
    ]

    # Firmware architecture
    story += [
        heading("4", "Código y estructura"),
        make_table(
            [
                ["Archivo", "Responsabilidad"],
                ["src/main.cpp", "Secuencia principal, tarea activa, reporte y contadores RTC."],
                ["src/power_manager.cpp", "Causas, validación de errores, fuentes de despertar y deep sleep."],
                ["src/status_led.cpp", "Abstracción de los cuatro estados visuales del LED RGB."],
                ["diagram.json", "Partes, posiciones, atributos y conexiones del circuito Wokwi."],
                ["wokwi.toml", "Rutas al firmware BIN y ELF generado por PlatformIO."],
                ["wokwi-web/sketch.ino", "Variante monolítica equivalente publicada en Wokwi Online."],
                ["tests/*.yaml", "Escenarios para TIMER y pulsador EXT0 en Wokwi CI."],
                ["tests/validate_project.py", "20 comprobaciones de coherencia sin servicios externos."],
            ],
            [55 * mm, 115 * mm],
        ),
        P("Fragmento principal", "H2Arial"),
        code_block(
            "void setup() {\n"
            "  const auto cause = esp_sleep_get_wakeup_cause();\n"
            "  registerWakeup(cause);\n"
            "  printStartupReport(cause);\n\n"
            "  StatusLed::blue();\n"
            "  runActiveTask();\n"
            "  prepareForSleep();\n"
            "  PowerManager::enterDeepSleep();\n"
            "}"
        ),
        P("Mensajes seriales", "H2Arial"),
        P(
            "Los mensajes tienen claves estables (<font name='Courier-New'>BOOT</font>, <font name='Courier-New'>CAUSA</font>, <font name='Courier-New'>ESTADO</font> y <font name='Courier-New'>CONTADORES</font>) para que una persona o un escenario automatizado pueda verificar el flujo sin depender únicamente del LED.",
        ),
        P("Repositorio", "H2Arial"),
        P(
            "<link href='https://github.com/JdesaG/tarea6-esp32-gestion-energia' color='#087E8B'><u>https://github.com/JdesaG/tarea6-esp32-gestion-energia</u></link>",
        ),
        callout(
            "REPRODUCIBLE",
            "El repositorio contiene código fuente, README, instrucciones, circuito Wokwi, configuración PlatformIO y escenarios de prueba.",
            GREEN,
        ),
        PageBreak(),
    ]

    # Evidence
    build_log = (EVIDENCE / "compilacion-platformio.txt").read_text()
    web_log = (EVIDENCE / "compilacion-wokwi-web.txt").read_text()
    checksum_log = (EVIDENCE / "checksums-firmware.txt").read_text()
    story += [
        heading("5", "Pruebas y evidencias"),
        make_table(
            [
                ["Prueba", "Resultado", "Evidencia"],
                ["Compilación PlatformIO modular", "APROBADA", "RAM 6.9%; flash 21.5%"],
                ["Compilación variante Wokwi web", "APROBADA", "Firmware BIN generado"],
                ["Validez JSON", "APROBADA", "diagram.json parseado"],
                ["Linter Wokwi CLI 0.26.1", "APROBADA", "0 errores; 1 nota informativa"],
                ["Coherencia firmware-circuito", "APROBADA", "20/20 comprobaciones"],
                ["Publicación Wokwi", "APROBADA", "HTTP 200 y captura pública"],
                ["Publicación GitHub", "APROBADA", "HTTP 200 y rama main"],
            ],
            [66 * mm, 34 * mm, 70 * mm],
        ),
        P("Salida de compilación principal", "H2Arial"),
        code_block("\n".join(build_log.strip().splitlines()[-8:])),
        P("Salida de compilación de la variante web", "H2Arial"),
        code_block("\n".join(web_log.strip().splitlines()[-9:])),
        P("Integridad del firmware", "H2Arial"),
        code_block(checksum_log),
        P(
            "Los hashes SHA-256 permiten confirmar que los binarios evaluados son exactamente los generados durante esta entrega.",
            "SmallArial",
        ),
        PageBreak(),
    ]

    # Test procedures
    story += [
        heading("6", "Procedimientos de simulación"),
        P("Prueba A - Despertar por temporizador", "H2Arial"),
        bullet("Abrir el enlace Wokwi, iniciar la simulación y no pulsar el botón."),
        bullet("Comprobar los estados azul, verde, amarillo y apagado."),
        bullet("Después de 10 s, verificar un nuevo arranque con CAUSA=temporizador RTC."),
        code_block(
            "BOOT=1\n"
            "CAUSA=encendido o reinicio, no deep sleep\n"
            "ESTADO=ACTIVO | LED verde | Tarea de 5 segundos.\n"
            "ESTADO=SLEEP | Entrando en deep sleep.\n"
            "BOOT=2\n"
            "CAUSA=temporizador RTC\n"
            "CONTADORES timer=1, ext0=0"
        ),
        P("Prueba B - Despertar externo EXT0", "H2Arial"),
        bullet("Reiniciar la simulación y esperar el mensaje ESTADO=SLEEP."),
        bullet("Pulsar el botón azul WAKE EXT0 o mantener la tecla B."),
        bullet("Verificar un nuevo arranque con CAUSA=pin externo EXT0 (GPIO33)."),
        code_block(
            "ESTADO=SLEEP | Entrando en deep sleep.\n"
            "BOOT=2\n"
            "CAUSA=pin externo EXT0 (GPIO33)\n"
            "CONTADORES timer=0, ext0=1"
        ),
        P("Automatización disponible", "H2Arial"),
        P(
            "Los archivos <font name='Courier-New'>tests/timer-wakeup.yaml</font> y <font name='Courier-New'>tests/ext0-wakeup.yaml</font> reproducen estas secuencias con Wokwi CLI. La ejecución remota por CLI requiere un token personal <font name='Courier-New'>WOKWI_CLI_TOKEN</font>; los escenarios se entregan listos, pero no se incluyó una credencial privada en el repositorio.",
        ),
        callout(
            "ALCANCE",
            "La captura demuestra el circuito publicado. Las compilaciones y validaciones fueron ejecutadas. Los bloques seriales anteriores definen la salida esperada por los escenarios; no se presentan como una medición física.",
            YELLOW,
        ),
        PageBreak(),
    ]

    # Analysis
    story += [
        heading("7", "Análisis del comportamiento"),
        P("Antes y después del reposo", "H2Arial"),
        P(
            "Antes de dormir se apaga el LED, se vacía el buffer UART y se habilitan las fuentes TIMER y EXT0. Durante deep sleep la CPU y los periféricos digitales se apagan. Al despertar, el chip reinicia el firmware desde setup(), pero conserva las variables ubicadas en memoria RTC.",
        ),
        P("Impacto energético", "H2Arial"),
        P(
            "El ahorro proviene de mantener el sistema activo únicamente durante la tarea y la preparación, y usar deep sleep durante la espera. El ciclo de demostración usa 10 s de reposo para que la prueba sea rápida. En una aplicación alimentada por batería conviene aumentar ese intervalo de acuerdo con la frecuencia real de muestreo o reporte.",
        ),
        P("Simulación frente a hardware real", "H2Arial"),
        make_table(
            [
                ["Aspecto", "Wokwi", "Hardware real"],
                ["Flujo y temporización", "Valida estados y mensajes.", "Confirma tiempos con tolerancias reales."],
                ["Cableado lógico", "Detecta conexiones y pines.", "Puede revelar ruido, rebote y falsos contactos."],
                ["Causa de despertar", "Permite TIMER y EXT0.", "Verifica nivel eléctrico y comportamiento RTC."],
                ["Consumo", "No es una medición energética.", "Debe medirse con amperímetro o analizador."],
                ["Placa DevKit", "Modelo funcional idealizado.", "Regulador, USB-UART y LED elevan el consumo."],
            ],
            [38 * mm, 64 * mm, 68 * mm],
        ),
        Spacer(1, 5 * mm),
        callout(
            "HARDWARE REAL",
            "No se fabricó ni midió un montaje físico en esta entrega. Por honestidad técnica, no se atribuyen valores de corriente a la simulación. La evidencia física opcional debe añadir fotografías, modelo de instrumento, tensión, corriente activa y corriente en reposo.",
            RED,
        ),
        P("Criterios para una medición posterior", "H2Arial"),
        bullet("Alimentar a tensión conocida y medir corriente en serie con resolución de microamperios."),
        bullet("Separar el consumo del módulo ESP32 del regulador, convertidor USB-UART y LED de la placa."),
        bullet("Repetir las mediciones en estado activo y deep sleep, documentando promedio y picos."),
        PageBreak(),
    ]

    # Conclusions and references
    story += [
        heading("8", "Conclusiones y recomendaciones"),
        P("Conclusiones", "H2Arial"),
        bullet("<b>1.</b> Deep sleep reduce la actividad del sistema de forma drástica y resulta adecuado cuando la aplicación puede reiniciar su flujo después de cada despertar."),
        bullet("<b>2.</b> Combinar TIMER y EXT0 permite atender tanto tareas periódicas como eventos externos; el evento que ocurre primero determina la causa del nuevo arranque."),
        bullet("<b>3.</b> La memoria RTC y los mensajes seriales estructurados facilitan demostrar que el sistema durmió, despertó y conservó información mínima entre ciclos."),
        P("Recomendaciones", "H2Arial"),
        bullet("<b>1.</b> Dimensionar el intervalo de reposo según la necesidad real de la aplicación y mantener apagadas las cargas externas que no sean necesarias."),
        bullet("<b>2.</b> Validar siempre el consumo en hardware real, incluyendo regulador, interfaz USB y resistencias de polarización, porque la simulación no representa todas las pérdidas de la placa."),
        P("Entregables", "H2Arial"),
        make_table(
            [
                ["Elemento", "Ubicación / enlace"],
                ["Código y README", "Repositorio GitHub público"],
                ["Circuito Wokwi", "Proyecto público 471748304593999873"],
                ["Firmware PlatformIO", ".pio/build/esp32dev (generado localmente)"],
                ["Informe", "output/pdf/Informe_Tarea_6_Gestion_Energia_ESP32.pdf"],
                ["Video YouTube", "No incluido; requiere grabación y narración del estudiante"],
            ],
            [55 * mm, 115 * mm],
        ),
        P("Referencias", "H2Arial"),
        P(
            "[1] Espressif Systems. <link href='https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/sleep_modes.html' color='#087E8B'><u>ESP-IDF: Sleep Modes - ESP32</u></link>. Consulta: 07-08-2026.",
            "SmallArial",
        ),
        P(
            "[2] Espressif Systems. <link href='https://docs.espressif.com/projects/arduino-esp32/en/latest/api/deepsleep.html' color='#087E8B'><u>Arduino ESP32: Deep Sleep</u></link>. Consulta: 07-08-2026.",
            "SmallArial",
        ),
        P(
            "[3] Wokwi. <link href='https://docs.wokwi.com/guides/esp32' color='#087E8B'><u>ESP32 Simulation</u></link>. Consulta: 07-08-2026.",
            "SmallArial",
        ),
        P(
            "[4] Wokwi. <link href='https://docs.wokwi.com/vscode/project-config' color='#087E8B'><u>Configuring Your Project (wokwi.toml)</u></link>. Consulta: 07-08-2026.",
            "SmallArial",
        ),
    ]
    return story


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=22 * mm,
        bottomMargin=20 * mm,
        title="Tarea 6 - Gestión de energía con ESP32",
        author="JdesaG",
        subject="Implementación PlatformIO y Wokwi de deep sleep con TIMER y EXT0",
    )
    document.build(build_story(), onFirstPage=header_footer, onLaterPages=header_footer)
    print(OUTPUT)


if __name__ == "__main__":
    main()


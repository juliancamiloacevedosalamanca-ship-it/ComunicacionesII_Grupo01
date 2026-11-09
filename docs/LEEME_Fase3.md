# Fase 3 — Implementación con HackRF One y USRP (Guía 3)

## Qué pedía la fase
- Llevar el enlace a hardware sin cambiar los parámetros de diseño.
- Configurar el bloque del radio (Osmocom Sink/Source o UHD), con captura y explicación de cada parámetro.
- Calcular la tasa en banda base y la tasa del radio.
- Dibujar el enlace físico de prueba (radios, cables, atenuadores y antenas).
- Registrar los errores y advertencias encontrados y su solución, y responder las preguntas de investigación.

## Qué se hizo
- **Tx:** PRBS → codificación diferencial → BPSK → RRC → amplitud digital → remuestreo (×125/16 en HackRF, ×125/32 en USRP) → desplazamiento del LO → Osmocom Sink / UHD Sink.
- **Rx:** Osmocom Source / UHD Source → corrección del LO → remuestreo a 256 kS/s → impulsos del proyecto → AGC → FLL de borde de banda → PFB Clock Sync (filtro acoplado RRC y reloj) → Costas de orden 2 → decisión → decodificación diferencial.
- **Parámetros del radio:**
  - fc = 960 MHz, con LO a fc ∓ 200 kHz.
  - Tasa del radio: 2 MS/s en HackRF, 1 MS/s en USRP.
  - Ganancias Tx: IF 20 dB, amplificador RF apagado.
  - Ganancias Rx: LNA 16 dB, VGA 20 dB.
  - Ancho de banda automático, Bias-T apagado y sin Throttle.

## Archivos
- `grc/Fase3_HackRF_TX_BPSK_Grupo1.grc`, `grc/Fase3_HackRF_RX_BPSK_Grupo1.grc`, `grc/Fase3_USRP_TX_BPSK_Grupo1.grc`, `grc/Fase3_USRP_RX_BPSK_Grupo1.grc`
- `capturas/bloque_osmocom_sink_TX_HackRF.png`, `capturas/bloque_osmocom_source_RX_HackRF.png`, `capturas/bloque_uhd_usrp_sink_TX.png`
- `capturas/diagrama_enlace_fisico.png`
- `capturas/flujograma_*.png`: diagramas de bloques de los cuatro flujogramas, generados directamente de los `.grc` con los parámetros de cada bloque.

La explicación de cada parámetro, la tabla de errores y las respuestas a las preguntas de investigación están en el informe (Fase 3 y anexos).

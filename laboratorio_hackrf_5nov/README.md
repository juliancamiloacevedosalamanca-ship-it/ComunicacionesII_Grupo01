# Práctica de laboratorio con antenas — 5 de noviembre de 2026 (Grupo 1)

Evidencia de la práctica guiada del docente con dos HackRF One.

- `grc_practica/LAB_TX_16QAM_HackRF_MEJORADO.grc` y `LAB_RX_16QAM_HackRF_MEJORADO.grc`: flujogramas del docente, tal como están en Moodle.
  - 16-QAM Gray, Rs = 8 ksym/s, Rb = 32 kb/s, SPS = 8, RRC β = 0.5, span 11.
  - fc = 960 MHz, radio a 2 MS/s (×125/4), LO desplazado 200 kHz.
  - Tx: IF 20 dB, amplitud digital 0.15. Rx: LNA 16 dB, VGA 20 dB.
- `capturas/`:
  - Tx: señal I/Q, envolvente, espectro y muestras RRC.
  - Rx: espectro y constelación con señal (10:28) y sin señal (10:30).
  - Consola del receptor al inicio y al final.
- `consola_rx_16qam.csv`: valores de la consola (tramas, % de tramas OK, BER y EVM acumuladas, rotación, CRC).

Resultado: la constelación 16-QAM se recupera con los 16 puntos separados. En total hubo 2601 tramas, 89.2 % OK, BER acumulada de 0.42 % y EVM de 8.5 %. Restando los acumulados, el tramo final (tramas 1951–2601) da BER ≈ 8·10⁻⁴, EVM ≈ 5.3 % y 95 % de tramas OK. Los errores que quedan coinciden con los saltos de rotación de fase (0/90/180/270°).

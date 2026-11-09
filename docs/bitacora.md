# Bitácora — Grupo 1, Comunicaciones II

| Fecha | Qué hicimos | Decisiones / problemas | Responsable |
|---|---|---|---|
| 8 oct 2026 | Lectura de la guía del proyecto. El docente nos asigna el escenario S1 (telemetría industrial con perturbaciones impulsivas). | | |
| 15 oct 2026 | Entrega de la ficha "Decisión Técnica Ciega" (PDF y JSON). | BPSK, GRC con AWGN, Rs=32 ksym/s, SPS=8, fs=256 kS/s, variable: amplitud del impulso. | |
| 24 oct 2026 | Revisión del Selector Guiado. Construcción de `Enlace_Beta_Impulsivo_Grupo1.grc`. | Impulsos con Vector Source (1 cada 256 muestras) y segundo Add después del AWGN. Valores: 0 / 0.3 / 0.6 / 1.0. | |
| 24 oct 2026 | Ejecución de las pruebas A–D en GNU Radio 3.10.12 y capturas (tiempo, PSD, constelación). | Los valores de los sliders se escriben con coma decimal (0,3) por la configuración regional de Windows. Al usar la rueda del mouse sobre la PSD se hace zoom; para bajar en la ventana usar la barra de desplazamiento. Resultado: los impulsos se ven claramente en tiempo y constelación, pero casi nada en la PSD. | |
| 5 nov 2026 | Práctica de laboratorio con antenas: enlace 16-QAM entre dos HackRF One a 960 MHz con los flujogramas del docente. | Se confirmó que los radios funcionan y que la frecuencia asignada al curso es 960 MHz. Las capturas se entregan aparte como evidencia. | |
| 6 nov 2026 | Fase 2: enlace completo con RRC (β = 0.35, span 11) y receptor propio (filtro acoplado, ojo, muestreo 1 de 8, decisión, BER por XOR). | El retardo Tx + Rx es de 88 muestras = 11 símbolos, así que se usa desfase 0 y la referencia se retrasa 11 bits. Con desfase 4 la BER sube a 0.25. En GRC 3.10.12 la fuente PRBS es `GLFSR Source` con tipo byte. | |
| 6 nov 2026 | Fase 2: capturas de GNU Radio de todas las pruebas (ideal, A–E y desfase 4). | BER medida: 0 en la prueba ideal y en A–E, 0.2498 con desfase 4. | |
| 6 nov 2026 | Fase 3: flujogramas TX/RX para HackRF One (Osmocom) y USRP (UHD). | fc = 960 MHz, 2 MS/s (HackRF) y 1 MS/s (USRP), remuestreo racional, LO desplazado 200 kHz, sin Throttle. Codificación diferencial por la ambigüedad de 180° del Costas. | |
| 6 nov 2026 | Fase 4: curvas BER medidas en GNU Radio (sin impulsos, A = 1, A = 5), 4 minutos cada una. | En GRC 3.10.12, e_BER_Curve (gr.sync_decimator) y e_BER_CSV (__file__) salían en rojo; se cambiaron a gr.decim_block y a un respaldo para __file__. Resultado: 7.30 / 7.38 / 9.17 dB a BER 1e-3. Los pocos errores a 14 dB vienen del salto 14→0 dB al reiniciar el barrido. | |
| 6 nov 2026 | Informe final en la plantilla IEEE del curso (Overleaf). Ya no se hace blog, por indicación del docente. | | |
| 8 nov 2026 | Revisión final del informe contra las guías 2, 3 y 4: prueba ideal, justificación de β y span, tabla de parámetros de los bloques de radio, diagrama del enlace físico, tabla de errores y respuestas a las preguntas de investigación. Limpieza del repositorio. | Queda pendiente medir la curva BER con los radios. | |

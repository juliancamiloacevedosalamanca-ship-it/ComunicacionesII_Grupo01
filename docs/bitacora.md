# Bitácora — Grupo 1, Comunicaciones II

| Fecha | Qué hicimos | Decisiones / problemas | Responsable |
|---|---|---|---|
| 8 oct 2026 | Lectura de la guía del proyecto. El docente nos asigna el escenario S1 (telemetría industrial con perturbaciones impulsivas). | | |
| 15 oct 2026 | Entrega de la ficha "Decisión Técnica Ciega" (PDF y JSON). | BPSK, GRC con AWGN, Rs=32 ksym/s, SPS=8, fs=256 kS/s, variable: amplitud del impulso. | |
| 24 oct 2026 | Revisión del Selector Guiado. Construcción de `Enlace_Beta_Impulsivo_Grupo1.grc`. | Impulsos con Vector Source (1 cada 256 muestras) y segundo Add después del AWGN. Valores: 0 / 0.3 / 0.6 / 1.0. | |
| 24 oct 2026 | Ejecución de las pruebas A–D en GNU Radio 3.10.12 y capturas (tiempo, PSD, constelación). | Los valores de los sliders se escriben con coma decimal (0,3) por la configuración regional de Windows. Al usar la rueda del mouse sobre la PSD se hace zoom; para bajar en la ventana usar la barra de desplazamiento. Resultado: los impulsos se ven claramente en tiempo y constelación, pero casi nada en la PSD. | |
| | Análisis de resultados e informe IEEE. | | |
| | Blog y video de socialización. | | |

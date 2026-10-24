# Guion del video de socialización (8–10 min) — Grupo 1

Sugerencia: grabar con OBS o Zoom compartiendo pantalla (blog + GNU Radio en vivo). Cada integrante presenta un bloque.

| Tiempo | Quién | Qué mostrar | Qué decir (idea, no leer) |
|---|---|---|---|
| 0:00–0:45 | Julian | Portada del blog | Presentación del grupo y pregunta guía: ¿qué le pasa a la señal de telemetría cuando un motor conmuta al lado? |
| 0:45–2:15 | Julian | Imagen del escenario | La planta, el Tx sobre la banda, el Rx en la sala, motores/contactores/VFD. Qué es el ruido impulsivo y en qué se diferencia del AWGN. Citar [1] y [2]. |
| 2:15–3:45 | Luigy | Diagrama técnico y tabla de parámetros | Por qué BPSK (robustez, separación de símbolos) y por qué no OOK ni QPSK/16QAM. Cálculos: k=1, Rb=32 kb/s, fs=Rs·SPS=256 kS/s, BW≈2Rs=64 kHz. |
| 3:45–5:30 | Luigy | GNU Radio Companion (GRC abierto) | Recorrido de bloques: qué se cambió (tabla BPSK, Vector Source [0j]*255+[A_imp], segundo Add, sinks). Por qué 256 muestras = 1 ms = 32 símbolos. |
| 5:30–7:30 | Juan Camilo | Ejecución en vivo moviendo A_imp 0 → 0.3 → 0.6 → 1.0 | Señal temporal: aparecen picos cada 1 ms. Constelación: puntos sueltos corridos +A_imp; en 1.0 caen en el umbral. PSD: casi igual. |
| 7:30–8:45 | Juan Camilo | Gráfica de síntesis de potencias | Por qué la PSD no cambia: potencia media A²/256 menor que el AWGN; la PSD promedia. Filtro acoplado: el impulso solo mueve la decisión A_imp/8. |
| 8:45–9:45 | Todos | Sección de reflexión del blog | Qué aprendimos, qué cambiaríamos (BER, impulsos aleatorios, BFSK). Uso de IA declarado. Invitar a comentar en el blog. |

Después de subirlo (YouTube no listado o Drive con acceso público), pegar el enlace en el README y en la sección Multimedia del blog.

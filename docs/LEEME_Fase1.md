# Fase 1 — Diseño conceptual y caracterización del canal

## Qué pedía la fase
- Elegir el escenario y justificar la decisión técnica (ficha de "decisión ciega").
- Elegir modulación y fijar Rs, SPS y fs.
- Modificar el flujograma base del curso para modelar la perturbación del escenario.
- Hacer una prueba de referencia y tres severidades (suave, media y fuerte), cambiando una sola variable.
- Capturar la señal en el tiempo, la constelación y la PSD de cada prueba, y analizarlas.

## Qué se hizo
- Escenario S1: un nodo de telemetría en una planta industrial con ruido impulsivo de motores, contactores y variadores.
- BPSK, tabla `(-1+0j, 1+0j)`, Rs = 32 ksym/s, SPS = 8, fs = 256 kS/s, Rb = 32 kb/s.
- Canal: AWGN fijo (`noise_amp = 0.10`) más un tren de impulsos reales de amplitud `A_imp`, uno cada 256 muestras (1 ms). Se agregaron un Vector Source y un segundo Add.
- Pruebas: A = 0 (referencia), B = 0.3, C = 0.6 y D = 1.0. Solo cambia `A_imp`.

## Archivos
- `grc/BASE_curso_Modulaciones_basadas_en_constelaciones_AWGN.grc`: archivo original del curso.
- `grc/Enlace_Beta_Impulsivo_Grupo1.grc`: flujograma de la fase.
- `capturas/flujograma_fase1.png` y `capturas/{tiempo,psd,constelacion}/*_A..D.png`.
- `ficha_decision/`: ficha enviada (PDF y JSON).
- `tabla_pruebas.csv`: tabla de pruebas con observaciones.

## Resultados
- El impulso se ve con claridad en el tiempo: picos de ≈1.3, 1.6 y 2 cada 1 ms, solo en la componente I.
- En la constelación aparecen puntos aislados desplazados +A_imp. Con A_imp = 1, los símbolos −1 caen en 0, justo en el umbral de decisión.
- La PSD casi no cambia, porque la potencia media del tren (A²/256 ≤ 0.004) es menor que la del AWGN (0.01).
- **Consecuencia para la Fase 2:** conformar con RRC y usar un filtro acoplado antes de decidir.

# Fase 2 — Diseño del sistema Tx–canal–Rx (Guía 2)

## Qué pedía la fase
- Construir el enlace completo con un receptor propio: filtro acoplado, diagrama de ojo, muestreo, decisión y recuperación de bits.
- Validar primero en condición ideal (sin ruido) y después con el canal del proyecto.
- Justificar Rs, SPS, β y span, y observar cómo cambia la PSD con β y span.
- Comparar los bits transmitidos con los recibidos y medir la BER.

## Qué se hizo
- Tx: PRBS-15 (GLFSR) → BPSK → RRC (β = 0.35, span 11, 89 coeficientes).
- Canal: AWGN 0.10 más impulsos A_imp.
- Rx: RRC acoplado (h/Σh²) → ojo → Keep 1 de 8 (desfase 0) → decisión por mínima distancia → bits.
- Validación: XOR con los bits Tx retrasados 11 bits y promedio móvil de 10⁵ bits, que da la BER.
- El retardo total Tx + Rx es de 88 muestras = 11 símbolos (calculado y verificado).
- Capturas automáticas de las 3 pestañas para cada prueba.

## Archivos
- `grc/Fase2_Enlace_BPSK_TxRx_Grupo1.grc`
- `capturas/flujograma_fase2.png`: flujograma.
- `capturas/<prueba>_1_transmisor_y_canal.png`: PSD, envolvente y plano I–Q.
- `capturas/<prueba>_2_receptor.png`: ojo, constelación recuperada y salida del filtro acoplado.
- `capturas/<prueba>_3_validacion_BER.png`: BER y bits Tx frente a Rx.
- `capturas/BER_medida_por_prueba.csv`: BER registrada en GNU Radio.
- `capturas/beta_span.png`: PSD al variar β y span (justificación de β = 0.35 y span = 11).

## Resultados (BER medida en GNU Radio, ventana de 10⁵ bits)
| Prueba | Ruido | A_imp | Desfase | BER |
|---|---|---|---|---|
| 0 ideal | 0 | 0 | 0 | 0 |
| A | 0.10 | 0 | 0 | 0 |
| B | 0.10 | 0.3 | 0 | 0 |
| C | 0.10 | 0.6 | 0 | 0 |
| D | 0.10 | 1.0 | 0 | 0 |
| E | 0.10 | 5.0 | 0 | 0 |
| F | 0.10 | 0 | 4 muestras | 0.2498 |

En los instantes de decisión, el filtro acoplado deja cada impulso en 0.100·A_imp. Por eso el ojo sigue abierto hasta A = 5 (margen de 0.40). Si se muestrea en el cruce del ojo, la BER sube a 0.25 aunque el canal no cambie.

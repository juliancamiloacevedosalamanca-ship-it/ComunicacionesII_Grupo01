# Fase 4 — Validación final con curvas BER (Guía 4)

## Qué pedía la fase
- Integrar el instrumento BER del curso (`e_EbN0_Sweep` y `e_BER_Curve`) en el flujograma del grupo.
- Fijar Rb, bb_rate, el rango de Eb/N0, los bits por punto, los bits de guarda y `delay_bits`.
- Alinear Tx y Rx (delay_bits) y comprobar BER ≈ 0 en condición limpia.
- Obtener la curva BER vs Eb/N0, guardar el CSV y compararla con la teoría (criterio: penalización ≤ 2 dB en BER = 1e-3).
- Explicar cualquier comportamiento inesperado.

## Qué se hizo
- `e_EbN0_Sweep` justo antes del filtro acoplado. `e_BER_Curve` recibe los bits PRBS (entrada 0) y los bits después del decodificador diferencial (entrada 1).
- Parámetros:
  - Rb = 32 000 y bb_rate = 256 000.
  - Eb/N0 de 0 a 14 dB, paso 1.
  - 100 000 bits por punto y 1000 de guarda.
  - delay_bits = 11, update_every = 1000.
- Bloque propio `e_Busca_Retardo`: confirmó delay_bits = 11 con correlación +1.000 y BER 0 en los puntos limpios.
- Tres condiciones: sin impulsos, A_imp = 1 y A_imp = 5. Cada una corrió 4 minutos, con unos 1.5·10⁶ bits por punto.
- Para que funcionaran en GNU Radio 3.10.12 se corrigieron dos bloques del kit: `e_BER_Curve` hereda ahora de `gr.decim_block`, y `e_BER_CSV` tiene un respaldo para `__file__`.

## Archivos
- `grc/simulacion/Fase4_BER_Simulado_BPSK_Grupo1.grc`, `grc/simulacion/Fase4_BER_Simulado_Impulsos_A1.grc`, `grc/simulacion/Fase4_BER_Simulado_Impulsos_A5.grc`
- `grc/hardware/Fase4_HackRF_RX_BER_BPSK_Grupo1.grc`, `grc/hardware/Fase4_USRP_RX_BER_BPSK_Grupo1.grc`: listos para medir con el radio.
- `capturas/flujograma_fase4.png` y `capturas/ventana_BER_*.png`: ventanas de GNU Radio.
- `capturas/curvas_BER_vs_teoria.png`
- `datos/curva_BER_sim_*.csv`: CSV escritos por el instrumento.

## Resultados (Eb/N0 para BER = 1e-3)
| Condición | Eb/N0 | Diferencia con la teoría DE-BPSK (7.33 dB) |
|---|---|---|
| Sin impulsos | 7.30 dB | −0.03 dB |
| A_imp = 1 | 7.38 dB | +0.05 dB |
| A_imp = 5 | 9.17 dB | +1.84 dB |

Los pocos errores a 14 dB en las curvas sin impulsos y con A = 1 vienen del salto 14 → 0 dB al reiniciar el barrido; no son del enlace.

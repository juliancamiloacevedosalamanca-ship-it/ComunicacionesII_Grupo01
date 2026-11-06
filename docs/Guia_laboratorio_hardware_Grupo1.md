# Guía de laboratorio — Fases 3 y 4 con HackRF One / USRP (Grupo 1, S1)

Esta guía explica cómo usar en el laboratorio los flujogramas de hardware del proyecto. Las pruebas con el radio físico **solo se pueden hacer con el equipo del laboratorio**. Todo lo demás (diseño del receptor y curva BER simulada de referencia) ya está hecho y documentado.

## 1. Archivos

| Archivo | Para qué |
|---|---|
| `grc/fase3_hardware/Fase3_HackRF_TX_BPSK_Grupo1.grc` | Transmisor del proyecto con HackRF (Osmocom Sink) |
| `grc/fase3_hardware/Fase3_HackRF_RX_BPSK_Grupo1.grc` | Receptor del proyecto con HackRF (Osmocom Source) |
| `grc/fase3_hardware/Fase3_USRP_TX_BPSK_Grupo1.grc` | Transmisor con USRP (UHD: USRP Sink) |
| `grc/fase3_hardware/Fase3_USRP_RX_BPSK_Grupo1.grc` | Receptor con USRP (UHD: USRP Source) |
| `grc/fase4_ber/hardware/Fase4_HackRF_RX_BER_BPSK_Grupo1.grc` | Receptor HackRF + instrumento BER (e_EbN0_Sweep, e_BER_Curve, CSV) |
| `grc/fase4_ber/hardware/Fase4_USRP_RX_BER_BPSK_Grupo1.grc` | Receptor USRP + instrumento BER |

El transmisor de la Fase 4 es el mismo de la Fase 3.

## 2. Parámetros de diseño (no cambian al pasar a hardware)

| Parámetro | Valor | Justificación |
|---|---|---|
| Modulación | BPSK con codificación diferencial | BPSK: máxima distancia entre símbolos. La codificación diferencial resuelve la ambigüedad de 180° del lazo de Costas en hardware. |
| Rs / Rb | 32 ksym/s / 32 kb/s | Telemetría lenta: holgura suficiente para tramas con cabecera y CRC. |
| SPS | 8 | |
| bb_rate | 256 kS/s | Rs · SPS |
| RRC | β = 0.35, span = 11 símbolos | BW ≈ (1+β)·Rs = 43.2 kHz |
| Secuencia de prueba | PRBS-15 (GLFSR, semilla 1) | Conocida y repetible en Tx y Rx, aunque estén en computadores distintos. |

## 3. Parámetros que aparecen solo con hardware

| Parámetro | HackRF One | USRP | Por qué |
|---|---|---|---|
| radio_rate | 2 MS/s | 1 MS/s | HackRF trabaja de 2 a 20 MS/s. 1 MS/s es una tasa válida en B2xx y N2xx (100 MHz / 100). |
| Adaptación de tasa (Tx) | interp 125 / decim 16 | interp 125 / decim 32 | 256 000 · 125/16 = 2 000 000 y 256 000 · 125/32 = 1 000 000. **Rs no se cambia.** |
| Adaptación de tasa (Rx) | interp 16 / decim 125 | interp 32 / decim 125 | Relación inversa, antes del receptor digital. |
| fc | 915 MHz | 915 MHz | Banda ISM 902–928 MHz (Región 2). **Confirmar con el docente** la frecuencia autorizada en el laboratorio (el ejemplo del curso usa 960 MHz). |
| lo_off | 200 kHz | 200 kHz | El LO del Tx se sintoniza en fc − lo_off y el del Rx en fc + lo_off; la señal se desplaza digitalmente. Así queda lejos de la espiga de DC del conversor. |
| Ganancia Tx | IF/VGA 20 dB, amplificador RF (gain0) en 0 | gain 20 dB | Empezar bajo, sobre todo por cable. |
| Ganancia Rx | LNA 16 dB, VGA 20 dB, amplificador RF en 0 | gain 30 dB | Subir de a poco hasta ver la señal sin saturar. |
| Ancho de banda RF (bw0) | 0 = automático | 0 = automático | El filtro analógico se elige según radio_rate. |
| Bias-T | apagado | — | Alimenta un LNA externo por el coaxial; activarlo sin saber qué hay conectado puede dañar equipos. |
| Antena / puerto | — | TX/RX para transmitir, RX2 para recibir | |
| Reloj | interno | internal | Con referencia externa (10 MHz/PPS) desaparecería casi todo el offset de frecuencia entre radios. |
| Throttle | **eliminado** | **eliminado** | El propio SDR fija el ritmo de muestras. |

## 4. Procedimiento en el laboratorio

### Fase 3 — configuración y prueba mínima
1. Conectar Tx y Rx **por cable coaxial con atenuación** (al menos 30–40 dB). Nunca conectar dos radios directo sin atenuador: el Tx puede quemar la entrada del Rx.
2. Verificar que el sistema detecta el radio: `hackrf_info` (HackRF) o `uhd_find_devices` / `uhd_usrp_probe` (USRP).
3. Abrir el archivo TX, revisar `fc`, `tx_amp` y la ganancia, y ejecutarlo. Captura obligatoria: el bloque **Osmocom Sink** (o **UHD: USRP Sink**) con sus parámetros.
4. Abrir el archivo RX en el otro computador (o en el mismo, si hay dos radios) y ejecutarlo. Revisar:
   - el **espectro recibido**: debe verse el lóbulo de la señal centrado en 0 Hz, de unos 43 kHz de ancho;
   - el **diagrama de ojo**;
   - la **constelación recuperada**: dos nubes en ±1.
5. Ajustar las ganancias: si la constelación se ve como un anillo o el espectro tiene "techo", hay saturación y hay que bajar la ganancia. Si las nubes están muy abiertas, subirla.
6. Anotar en la bitácora los errores reales: offset de frecuencia, nivel, DC, saturación, mensajes "U"/"O" (underflow/overflow) en la consola, etc.

### Fase 4 — curva BER experimental
1. Abrir `Fase4_<radio>_RX_BER_BPSK_Grupo1.grc`. El instrumento ya está integrado:
   `SDR → desplazamiento LO → adaptación a 256 kS/s → (impulsos del proyecto) → e_EbN0_Sweep → receptor → e_BER_Curve`.
2. Valores del instrumento: `Rb = 32000`, `bb_rate = samp_rate = 256000`, `EbN0_min = 0`, `EbN0_max = 14`, `EbN0_step = 1`, `bits_por_punto = 100000`, `bits_guardia = 1000`, `update_every = 1000`.
3. **Calibrar `delay_bits`:** ejecutar con el enlace limpio. El bloque `e_Busca_Retardo` imprime en la consola de GNU Radio algo como
   `[e_Busca_Retardo] delay_bits = 1234  correlacion = +1.000  BER en ese retardo = 0.000e+00`.
   Copiar ese número en la variable `delay_bits`, volver a ejecutar y comprobar que en los puntos de Eb/N0 altos la BER es ≈ 0. Si la correlación sale negativa, los bits están invertidos: revisar la decodificación diferencial.
4. Dejar correr el barrido hasta que la curva se estabilice (varias vueltas). El archivo **`curva_BER.csv`** se guarda solo en la misma carpeta del `.grc`. No editarlo a mano.
5. Subir `curva_BER.csv` a GitHub en `data/curvas_ber/`.
6. Comparar con la referencia simulada (`data/curvas_ber/curva_BER_sim_AWGN.csv`) en BER = 1e-3. El criterio del curso es una penalización experimental **≤ 2 dB**.
7. Opcional: repetir con `A_imp = 1.0` y `A_imp = 5.0` para ver el efecto del ruido impulsivo en el enlace real.

## 5. Respuestas a las preguntas de investigación (Guía 3)

1. **¿Por qué el Channel Model ya no representa el canal?** Porque ahora el canal es el medio físico real (cable o aire) entre los dos radios. Solo se conservan, de forma digital, las perturbaciones que el grupo decide inyectar a propósito (el tren de impulsos).
2. **¿Por qué el Throttle es innecesario?** El SDR consume o entrega muestras al ritmo de su reloj. Un Throttle adicional competiría con ese ritmo y produciría underflows u overflows.
3. **fc frente a banda base:** fc es la frecuencia del oscilador del radio. La señal de banda base ocupa ±21.6 kHz alrededor de 0 Hz (desplazada ±lo_off); en el aire aparece alrededor de fc.
4. **Si el Tx genera muestras más lento que el SDR:** el radio se queda sin datos (underflow, "U" en la consola) y transmite huecos, lo que rompe la sincronización del receptor.
5. **Amplitud digital frente a ganancia RF:** la amplitud digital usa el rango del DAC y, si |x| > 1, satura y genera distorsión. La ganancia RF amplifica la señal ya convertida y sube también el ruido de las etapas siguientes. Lo correcto es una amplitud digital moderada (pico < 1) y ajustar la potencia con la ganancia.
6. **¿Qué limita la tasa útil?** Todos: el conversor del SDR, el bus (USB 2.0 en HackRF, USB 3.0 en B2xx, Gigabit Ethernet en N2xx) y la capacidad del computador para ejecutar los bloques en tiempo real.
7. **Offset entre radios:** cada radio tiene su propio oscilador con una tolerancia de algunos ppm. A 915 MHz, 10 ppm ≈ 9 kHz de diferencia. Por eso el receptor lleva un FLL y un lazo de Costas.
8. **Qué se conserva y qué aparece:** se conservan modulación, Rs, Rb, SPS, β, span, mapeo y el receptor digital. Aparecen fc, radio_rate, remuestreo, ganancias, ancho de banda RF, antena/puerto, reloj, lo_off y la sincronización de portadora y reloj.
9. **Riesgo de conectar dos radios sin atenuación:** la potencia del Tx puede superar el nivel máximo de entrada del Rx (por ejemplo, unos −5 dBm en HackRF) y dañar el LNA.
10. **Cómo saber si el problema es de RF y no de la modulación:** si el mismo flujograma funciona en simulación pero en hardware el espectro aparece desplazado, saturado, con espiga de DC o con offset estimado por el FLL distinto de cero, el problema está en la configuración RF. Si el espectro es correcto pero la constelación no, el problema está en la sincronización o la decisión.

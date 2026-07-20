# Limpieza inicial
cat('\014')
rm(list = ls())

# Librerías necesarias
library(here)
library(lubridate)
library(plotly)
library(slider)
library(tidyverse)
library(tsibble)

# Lectura eficiente con enrutamiento dinamico
datos_clean <- read_delim(
  file = here('data', 'lluvia_2026_v2.csv'),
  delim = ";",
  show_col_types = FALSE
) %>%
  # Transmute() crea las variables nuevas y descarta las antiguas en un solo paso
  transmute(
    timestamp = as_datetime(as.Date(fecha, origin = "1899-12-30")) + hours(hora),
    lluvia_mm = as.numeric(lluvia_mm),
  ) %>%
  # Remove duplicate timestamps (keeps first occurrence)
  distinct(timestamp, .keep_all = TRUE)

head(datos_clean, 10)

# Visualizació de datos
plot(
  datos_clean$timestamp,
  datos_clean$lluvia_mm,
  type = 'p',
  main = 'Quilpué: Lluvia cada tres horas (mm)',
  xlab = 'Fecha',
  ylab = 'Lluvia (mm)'
)

# ==============================================================================
# 1. Transformación a Estructura de Serie de Tiempo (tsibble)
# ==============================================================================

# Para usar slider de forma segura, el dataset debe estar indexado temporalmente
datos_ts <- datos_clean %>% as_tsibble(index = timestamp)

# ==============================================================================
# 2. Cálculo Vectorizado de Medias Móviles (Hacia el pasado)
# ==============================================================================

# Definimos las horas requeridas y sus equivalencias en pasos (cada 3h)
# Ventana completa = .before + 1 (la observación actual)
datos_modelados <- datos_ts %>%
  mutate(
    media_movil_06h = slide_index_dbl(lluvia_mm, .i = timestamp, .f = mean, .before = hours(3)),
    media_movil_12h = slide_index_dbl(lluvia_mm, .i = timestamp, .f = mean, .before = hours(9)),
    media_movil_15h = slide_index_dbl(lluvia_mm, .i = timestamp, .f = mean, .before = hours(12)),
    media_movil_18h = slide_index_dbl(lluvia_mm, .i = timestamp, .f = mean, .before = hours(15)),
    media_movil_21h = slide_index_dbl(lluvia_mm, .i = timestamp, .f = mean, .before = hours(18)),
    media_movil_24h = slide_index_dbl(lluvia_mm, .i = timestamp, .f = mean, .before = hours(21))
  )

# ==============================================================================
# 3. Inspección del Output
# ==============================================================================
print("Estructura final con métricas de persistencia:")
glimpse(datos_modelados)

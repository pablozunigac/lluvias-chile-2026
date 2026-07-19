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
  file = here('data', 'lluvia_2026_v1.csv'),
  delim = ";",
  show_col_types = FALSE
) %>%
  # Transmute() crea las variables nuevas y descarta las antiguas en un solo paso
  transmute(
    timestamp = as_datetime(as.Date(fecha, origin = "1899-12-30")) + hours(hora),
    lluvia_mm = as.numeric(lluvia_mm),
  )
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

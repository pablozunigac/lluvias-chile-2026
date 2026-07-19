# Limpieza inicial
rm(list = ls())
gc()

# Librerías necesarias
# 'here'   -> Gestiona rutas relativas robustas basadas en la raíz del proyecto Git
# 'readr'  -> Lector de archivos planos ultra rápido e inteligente (Tidyverse)
library(here)
library(tidyverse)
library(tsibble)
library(slider)
library(plotly)

# Lectura de datos
# ruta_datos = here('data', 'lluvia_2026_v1.csv')
datos_raw = read_delim(here('data',
                            'lluvia_2026_v1.csv'),
                      delim = ';',
                      col_names = TRUE
                      )
datos_clean <- datos_raw %>%
  mutate(
    fecha_dt = as.Date(fecha, origin = '1899-12-30'),
    lluvia_mm = as.numeric(lluvia_mm),
    timestamp = as.POSIXct(paste(fecha_dt, sprintf("%02d:00:00", hora)), format = "%Y-%m-%d %H:%M:%S")
  ) %>% 
  select(timestamp, fecha_dt, hora, lluvia_mm)

glimpse(datos_clean)

datos_clean

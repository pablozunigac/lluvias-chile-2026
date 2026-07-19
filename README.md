# Modelo Estadístico para las Lluvias de 2026 en Chile

Este repositorio contiene la infraestructura de datos, el flujo ETL (Extracción, Transformación y Carga) y los modelos estadísticos diseñados para analizar las precipitaciones en Chile durante el año 2026. El objetivo principal es estructurar series de tiempo meteorológicas de forma limpia, portátil y reproducible.

## 📁 Arquitectura del Proyecto

El proyecto sigue una estructura modular para reducir la fricción en el manejo de datos y código:

```text
├── R/
│   └── 00-lectura-ETL.R      # Script principal de importación, limpieza y formateo cronológico
├── data/                     # Bases de datos locales (Archivos fuente protegidos por .gitignore)
│   ├── lluvia_2026_v1.csv : Lluvias entre jueves y martes
│   ├── lluvia_2026_v2.csv : Lluvias entre jueves y martes
├── output/                   # Resultados, gráficos y datasets procesados listos para exportación
├── .gitignore                # Reglas de exclusión para archivos temporales y datos pesados
└── README.md                 # Documentación técnica del repositorio

## Software

- **Entorno de Desarrollo:** Positron 
- **Lenguaje:** R 4.5.2
- **Librerías Core:** `tidyverse` (manipulación de datos), `lubridate` (gestión de zonas horarias y fechas), `here` (enrutamiento dinámico y portátil).

## Configuración y Reproducción

Para ejecutar este proyecto de forma local sin errores de rutas absolutas, asegúrate de clonar el repositorio dentro de tu entorno de trabajo:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/pablozunigac/lluvias-chile-2026.git](https://github.com/pablozunigac/lluvias-chile-2026.git)
# Modelo Estadístico para las Lluvias de 2026 en Chile

Este repositorio contiene la infraestructura de datos, el flujo ETL (_Extract_, _Transform_, _Load_) y los modelos estadísticos diseñados para analizar las precipitaciones en Chile durante el año 2026. El objetivo es estructurar visualizaciones de datos para las series de tiempo meteorológicas pronosticadas por Windy (ECMWF) para la Región de Valparaíso para julio de 2026.

## Arquitectura del Proyecto

El proyecto sigue una estructura modular para reducir la fricción en el manejo de datos y código:

* **`./R`** : Script principal de importación, limpieza y formateo cronológico
  * `00-lectura-ETL.R` : Script principal de importación, limpieza y formateo cronológico  
* **`./data`** : Archivos de datos sin procesar
  * `lluvia_2026_v1.csv` : Lluvias entre jueves 16 y sábado 17 de julio de 2026 (Actualización: jueves, 11am)
  * `lluvia_2026_v2.csv` : Lluvias entre jueves 16 y martes 21 de julio de 2026 (Actualización: domingo, 5am)  
* **`./output`** : Resultados, gráficos y datos procesados listos para exportación  
* **`Metadatos GitHub`**
  * `./README.md` : Documentación técnica del repositorio
  * `./.gitignore`: Reglas de exclusión para archivos temporales y datos pesados

## Entorno de Desarrollo
- **IDE:** Positron 2026.07.0 build 365
- **Lenguaje:** R 4.5.2
- **Librerías de R**
  - `here` : Resolucion de rutas absolutas basada en el anclaje raiz del proyecto
  - `lubridate` : Parseo, aritmetica y manipulacion eficiente de fechas y zonas horarias
  - `tidyverse` : Coleccion de paquetes para ciencia de datos y transformacion de estructuras
  - `plotly` : Gráficos interactivos y dinámicos para exploración de datos
  - `slider` : Cálculo eficiente de ventanas móviles y promedios acumulados
  - `tsibble` : Estructuras de datos y herramientas optimizadas para series de tiempo

## Configuración y Reproducción
Para ejecutar este proyecto de forma local sin errores de rutas absolutas, asegúrate de clonar el repositorio dentro de tu entorno de trabajo:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/pablozunigac/lluvias-chile-2026.git](https://github.com/pablozunigac/lluvias-chile-2026.git)

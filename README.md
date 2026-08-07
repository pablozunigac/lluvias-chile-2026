# Modelo Estadístico para las Lluvias de 2026 en Chile

Este repositorio contiene la infraestructura de datos, el flujo ETL (_Extract_, _Transform_, _Load_) y los modelos estadísticos diseñados para analizar las precipitaciones en Chile durante el año 2026. El objetivo es estructurar visualizaciones de datos para las series de tiempo meteorológicas pronosticadas por Windy (ECMWF) para la Región de Valparaíso para julio de 2026.

---

## Arquitectura del Proyecto

El proyecto implementa una estructura modular de producción para garantizar un desacoplamiento estricto entre el procesamiento de datos crudos, la persistencia en formatos vectorizados y la capa de visualización interactiva.

```text
lluvias-chile-2026/
├── .devcontainer/       # Configuración del entorno de desarrollo aislado (Docker/VS Code)
├── .github/             # Flujos de trabajo de CI/CD y plantillas del repositorio
├── data/                # Almacenamiento de datasets de precipitación
│   ├── raw/             # Archivos CSV crudos sin procesar
│   └── processed/       # Matrices serializadas en formato Parquet
├── output/              # Gráficos exportados, reportes y artefactos analíticos
├── R/                   # Scripts legados y análisis estadísticos complementarios en R
├── src/                 # Pipeline principal de producción en Python (ETL + DataViz)
├── .gitignore           # Reglas de exclusión para datos de control de versiones
└── README.md            # Documentación técnica del repositorio
```

---

## Metodología y Modelo Analítico

El flujo de trabajo aborda la saturación hídrica mediante el análisis de persistencia y concentración en múltiples ventanas de tiempo hacia atrás (backward rolling windows):
* **Análisis de Frecuencia Marginal**  
Registros discretos de precipitación (mm) agregados en intervalos de 3 horas.
* **Matriz de Saturación Multi-Ventana**  
Cálculo de acumulados y medias móviles vectorizadas para ventanas temporales de 6h y de entre 12h y 96h en intervalos de 12h.
* **Persistencia Columnar (`Parquet`)**  
Transformación de los tipos flotantes de Excel a marcas temporales absolutas y almacenamiento binario comprimido con Snappy.
* **Visualización de Concentración**  
Generación de un mapa de calor (Heatmap) en Plotly para identificar los picos máximos de saturación de suelo durante el evento crítico.

## Entorno de Desarrollo y Dependencias

Entorno Python (Pipeline Principal)
Intérprete: Python 3.11+  

`polars` – Procesamiento y cálculo de medias móviles vectorizadas a alta velocidad.  
`plotly` – Motor de renderizado interactivo para mapas térmicos.  
`pandas` – Utilidades complementarias de formateo de arreglos.  

---

## Entorno R (Análisis Estadístico Completo)

Lenguaje: R ≥ 4.5.2  
Paquetes: `tidyverse`, `lubridate`, `plotly`, `slider`, `tsibble`, `here`.

---

## Configuración y Reproducción

### Clonar el Repositorio
```bash
git clone [https://github.com/pablozunigac/lluvias-chile-2026.git](https://github.com/pablozunigac/lluvias-chile-2026.git)
cd lluvias-chile-2026
```

### Instalar Dependencias de Python
```bash
python3 -m pip install polars plotly pandas
```

### Ejecutar el Pipeline ETL y Visualización
```bash
python3 src/csv_to_parquet.py
```

### Ejecutar el Pipeline en R (Opcional)
```bash
source('R/00-lectura-ETL.R')
```

---

## Perfil Profesional y Contacto

**Perfil Profesional Extendido: [pablozunigac.github.io ↗](http://pablozunigac.github.io)  
Contacto: [pablo.zuniga.c@gmail.com](mailto:pablo.zuniga.c@gmail.com)**

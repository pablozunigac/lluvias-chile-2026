# Modelo Estadístico para las Lluvias de 2026 en Chile

Este repositorio implementa una infraestructura analítica avanzada para la evaluación de eventos de precipitación extrema y saturación hídrica progresiva. Su propósito central es modelar la persistencia temporal de los frentes de mal tiempo mediante matrices de acumulación multi-ventana temporal, caracterización de valores extremos y mapas de calor interactivos, permitiendo anticipar el riesgo hídrico en zonas con asentaminetos domilicialios y productivos.

Diseñado para traducir datos de precipitación en métricas accionables, el sistema evalúa la acumulación de lluvia sobre ventanas móviles de 6 a 96 horas para predecir situaciones críticas, el horario de posibles evacuaciones, escenarios de saturación de suelos, riesgo de aluviones e interrupción de infraestructura crítica.

---

## Contexto Climatológico e Histórico: Temporal de Chile (Julio 2026)

Este análisis se enmarca en el **Temporal de Chile de julio de 2026**, un evento meteorológico de magnitud extraordinaria caracterizado por la entrada de un río atmosférico de Categoría 5 y una dinámica de "*_tren de sistemas frontales_*" encadenados, potenciados por la fase cálida del ciclo ENOS, también conocido como «_El Niño_».

### Impacto Territorial y Récords Hidrometeorológicos

* **Mapeo de Afectación (Coquimbo a Ñuble):** Declaración de *Estado de Catástrofe* en la Región de Coquimbo y la Provincia de Huasco. Desbordes masivos de cauces (Río Elqui, Estero Tongoy, Estero Marga Marga y Estero Quilpué en la Región de Valparaíso), socavamiento de infraestructura vial en la Ruta 5 y aislamiento de localidades por bajadas de quebradas.
* **Magnitud del Desastre:** Saldo nacional preliminar de 15 fallecidos, 16 desaparecidos, más de 16.000 personas damnificadas y sobre 15.800 personas en estado de aislamiento por falla de conectividad crítica.
* **Anomalía de Precipitación y Récords:** Registro de acumulados continuos entre 200 mm y 350 mm en menos de 72 horas. Destacan los hitos históricos de la Estación La Florida (La Serena) con 200.2 mm (máximo histórico desde 1954), Combarbalá con 285.5 mm (récord absoluto registrado), Valparaíso con 173.6 mm en 48 horas (acumulado mensual de 327.3 mm) y Chillán con 312.2 mm.

---

## Origen y Estructura de los Datos

Los datos analizados provienen de registros de precipitación recopilados mediante _scraping_ estructurado e integración del modelo **ECMWF (European Centre for Medium-Range Weather Forecasts)** a través de la plataforma Windy.com.

* **Frecuencia de Muestreo:** Registros discretos agregados en intervalos de 3 horas.
* **Estructura Cruda (`data/raw/Lluvia_2026_v2.csv`):**
* **Variables del _scraping_:** `fecha`, `hora`, `lluvia_mm`

---

## Arquitectura del Repositorio

El proyecto mantiene un desacoplamiento estricto entre los datos primarios, la exploración interactiva, el código fuente modular de producción y los artefactos exportados.

lluvias-chile-2026/
├── .github/                    # _Pipelines_ de CI/CD para automatización y GitHub Pages
├── .vscode/                    # Gestión de datasets
├── data/                       # Gestión de datasets
│   ├── processed/              # Matrices serializadas en Parquet con tipos optimizados
│   └── raw/                    # Archivos CSV crudos (Lluvia_2026_v1.csv, Lluvia_2026_v2.csv)
├── notebooks/                  # Entorno de exploración, AED e hipótesis de modelado
│   └── 01_aed_lluvias.ipynb    
├── output/                     # Gráficos vectoriales, reportes y artefactos finales
├── R/                          # Scripts legados y procesamiento estadístico complementario
├── src/                        # Código fuente modular de producción en Python
│   ├── csv_to_parquet.py
├── .gitignore                  # Exclusión de archivos pesados y temporales
├── package-lock.json           #
├── package.json                # 
└── README.md                   # Documentación técnica del proyecto

---

## Pipeline ETL (Extract, Transform, Load)

El pipeline de datos está construido sobre **Polars** para garantizar máxima velocidad de procesamiento en memoria mediante ejecución vectorizada:

1. **Extract:** Lectura resuelta mediante `pathlib` dinámico para garantizar portabilidad entre SO, con esquema tipado explícito (`hora` -> `Int32`, `fecha` -> `Float64`, `lluvia_mm` -> `Float64`).
2. **Transform:**
   * Reconstrucción del sello temporal absoluto (`datetime`): Conversión de la fecha flotante de serial Excel a `Date` y posterior combinación vectorial con el entero de hora.
   * Ordenamiento cronológico garantizado (`sort("datetime")`).
3. **Load:** Exportación en formato columnar **Parquet** en `data/processed/lluvia_2026_matrix.parquet`, preservando metadatos de tipo y nulos de inicialización.

---

## Modelo Analítico y Caracterización Estadística

### 1. Matriz de Saturación Multi-Ventana (Backward Rolling Windows)
Para medir la persistencia del temporal, se calcula una matriz de medias móviles (MA) para ventanas de h en {6, 12, 24, 36, 48, 60, 72, 84, 96} horas:

MA_h(t) = (1 / k) * SUM(P(t - i))

Donde P(t) es la precipitación en el tiempo t y k = h / 3 representa el número de periodos de 3 horas contenidos en la ventana h.

### 2. Análisis Descriptivo y Métricas Climatológicas
* **Medidas de Tendencia Central y Dispersión:** Evaluación de la media móvil, acumulado total y varianza sobre la serie temporal para identificar el régimen de precipitación.
* **Ajuste a Distribuciones de Valores Extremos:** Modelación de los picos de intensidad mediante la **Distribución Gumbel** para la estimación de periodos de retorno (T) de eventos de h-horas:
  
F(x) = exp(-exp(-(x - mu) / beta))

* **Dataviz Matrix (Heatmap Temporal):** Representación bidimensional mediante `Plotly Express` donde el eje X representa la línea del tiempo, el eje Y las ventanas de acumulación (h) y el canal de color (Reds) la intensidad promedio en mm/h.

---

## Evaluación y Validación del Modelo

1. **Monotonicidad de la Suma Acumulada:** Se verifica formalmente que SUM(P(t)) >= SUM(P(t-1)), validando la ausencia de valores negativos o discontinuidades en los sensores.
2. **Efecto de Borde por Inicialización:** Documentación explícita de los valores `null` generados por el parámetro `min_samples = h // 3`. Representa la ventana de calentamiento necesaria para que la métrica de saturación hídrica sea estadísticamente válida.
3. **Sensibilidad de Saturación Operativa:** Identificación del punto de inflexión donde las ventanas de 24h y 48h superan los umbrales críticos de absorción del suelo, señalando el inicio del riesgo aluvial.

---

## Estrategia de Despliegue

El proyecto adopta un enfoque de despliegue progresivo de estándar industrial:

* **Fase Exploratoria (`notebooks/01_aed_lluvias.ipynb`):** Prototipado de _notebook_ Jupyter, lectura inicial y visualización de datos para validación conceptual.
* **Fase de Producción (`src/`):** Modularización del código del _notebook_ en funciones puras y scripts ejecutables (ej.: `src/csv_to_parquet.py`) listos para ser orquestados por tareas programadas.
* **Fase de Reportabilidad y Dashboarding (GitHub Pages):** Renderizado y publicación del reporte web interactivo accesible de forma pública mediante [GitHub Pages](https://pablozunigac.github.io/lluvias-chile-2026).

---

## Configuración y Reproducción

### 1 Clonar el Repositorio

``` Bash
git clone https://github.com/pablozunigac/lluvias-chile-2026.git
cd lluvias-chile-2026
```

### 2 Entorno y Dependencias
Se recomienda utilizar Python 3.11+. Para instalar las dependencias exactas del proyecto:

``` Bash
python3 -m pip install polars plotly pandas nbformat
```

### 3 Ejecución del Notebook Exploratorio
Para abrir y correr el análisis interactivo completo:

``` Bash
jupyter notebook notebooks/01_aed_lluvias.ipynb
```

### 4 Ejecución del Pipeline ETL a Parquet
Para ejecutar el procesamiento en lote y generar el archivo persistido:

``` Bash
python3 src/csv_to_parquet.py
```

---

## Perfil Profesional y Contacto

**Perfil Profesional & Reportes:** [pablozunigac.github.io ↗](https://pablozunigac.github.io)  
**Contacto Directo:** [pablo.zuniga.c@gmail.com](mailto:pablo.zuniga.c@gmail.com)
# Modelo Estadístico para las Lluvias de 2026 en Chile

Este repositorio implementa una infraestructura analítica avanzada para la evaluación de eventos de precipitación extrema y saturación hídrica. Su propósito central es modelar la persistencia temporal de los frentes de mal tiempo mediante matrices de acumulación multi-ventana y mapas de calor interactivos, permitiendo anticipar el riesgo sistémico en contextos urbanos y rurales. Diseñado para mitigar escenarios críticos como desbordes fluviales, anegamientos severos e interrupción de infraestructura crítica, el sistema traduce pronósticos meteorológicos complejos en métricas accionables para la gestión de crisis y la toma de decisiones operativas en tiempo real.

## 🏛️ Contexto Climatológico e Histórico: El Temporal de Chile (Julio 2026)

En julio de 2026, la zona centro-norte de Chile enfrentó un evento hidrometeorológico crítico originado por el ingreso de un **río atmosférico de Categoría 5** acoplado a un tren de sistemas frontales encadenados, fenómeno intensificado por la fase cálida de El Niño. El evento causó una emergencia de escala nacional entre las regiones de Coquimbo y Ñuble, impactando severamente asentamientos urbanos, cadenas productivas y conectividad vial.

### Impacto Territorial, Humanitario e Infraestructura

* **Estado de Catástrofe e Impacto Humanitario:** La magnitud del desastre motivó la declaración de *Estado de Catástrofe* en la Región de Coquimbo y la Provincia de Huasco. El saldo nacional registró **15 personas fallecidas, 16 desaparecidas**, más de 16.000 damnificados y sobre 15.800 personas aisladas por colapsos viales.
* **Infraestructura Critica y Cauces:** Se registraron socavamientos mayores en la Ruta 5 y vías costeras, daños en la infraestructura hospitalaria de Ovalle y desbordes de cauces principales como el río Elqui y el estero Tongoy en Coquimbo, además de evacuaciones masivas en la Región de Valparaíso por la crecida de los esteros Marga Marga y Quilpué.

### Registros Históricos y Dinámica de Saturación

El frente descargó acumulados continuos de **200 a 350 mm en menos de 72 horas**, alcanzando hitos no registrados en décadas:

* **La Serena (Estación La Florida):** 200,2 mm, el registro más alto para la zona desde 1954.
* **Combarbalá:** 285,5 mm, marcando un récord histórico absoluto.
* **Valparaíso:** 173,6 mm en 48 horas, acumulando un total mensual de 327,3 mm.
* **Chillán:** 312,2 mm acumulados durante el evento.

### Respuesta Analítica e Infraestructura de Datos

Frente a la rápida saturación de suelos y el riesgo aluvial, este repositorio despliega un **modelo estocástico y matricial** diseñado para procesar telemetría de precipitación y anticipar la saturación hídrica mediante ventanas móviles (6h a 96h). El sistema convierte registros complejos en métricas operativas directas para respaldar evacuaciones preventivas y la protección de infraestructura crítica.

## Arquitectura del Repositorio

El proyecto mantiene un desacoplamiento estricto entre los datos primarios, la exploración interactiva, el código fuente modular y los artefactos exportados.

lluvias-chile-2026/
├── \_site                      # 
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
├── web                         # 
├── .gitignore                  # Exclusión de archivos pesados y temporales
└── README.md                   # Documentación técnica del proyecto

## Origen y Estructura de los Datos

Los datos analizados provienen de registros de precipitación recopilados mediante _scraping_ estructurado e integración del modelo **ECMWF (European Centre for Medium-Range Weather Forecasts)** a través de la plataforma Windy.com.

* **Frecuencia de Muestreo:** Registros discretos agregados en intervalos de 3 horas.
* **Estructura Cruda (`data/raw/Lluvia_2026_v2.csv`):**
* **Variables del _scraping_:** `fecha`, `hora`, `lluvia_mm`

## Pipeline ETL (Extract, Transform, Load)

El pipeline de datos está construido sobre **Polars** para garantizar máxima velocidad de procesamiento en memoria mediante ejecución vectorizada:

1 **_Extract_:** Lectura resuelta mediante `pathlib` dinámico para garantizar portabilidad entre SO, con esquema tipado explícito (`hora` -> `Int32`, `fecha` -> `Float64`, `lluvia_mm` -> `Float64`).
2 **_Transform_:**
   * Reconstrucción del sello temporal absoluto (`datetime`): Conversión de la fecha flotante de serial Excel a `Date` y posterior combinación vectorial con el entero de hora.
   * Ordenamiento cronológico garantizado (`sort("datetime")`).
3 **_Load_:** Exportación en formato columnar **Parquet** en `data/processed/lluvia_2026_matrix.parquet`, preservando metadatos de tipo y nulos de inicialización.

## Modelo Analítico y Caracterización Estadística

### 1. Matriz de Saturación Multi-Ventana
Para medir la persistencia del temporal, se calcula una matriz de medias móviles (MA) para ventanas de h en {6, 12, 24, 36, 48, 60, 72, 84, 96} horas:

MA_h(t) = (1 / k) * SUM(P(t - i))

Donde P(t) es la precipitación en el tiempo t y k = h / 3 representa el número de periodos de 3 horas contenidos en la ventana h.

### 2. Análisis Descriptivo y Métricas Climatológicas
* **Medidas de Tendencia Central y Dispersión:** Evaluación de la media móvil, acumulado total y varianza sobre la serie temporal para identificar el régimen de precipitación.
* **Ajuste a Distribuciones de Valores Extremos:** Modelación de los picos de intensidad mediante la **Distribución Gumbel** para la estimación de periodos de retorno (T) de eventos de h-horas:
  
F(x) = exp(-exp(-(x - mu) / beta))

* **Dataviz Matrix (Heatmap Temporal):** Representación bidimensional mediante `Plotly Express` donde el eje X representa la línea del tiempo, el eje Y las ventanas de acumulación (h) y el canal de color (Reds) la intensidad promedio en mm/h.

## Evaluación y Validación del Modelo

1. **Monotonicidad de la Suma Acumulada:** Se verifica formalmente que SUM(P(t)) >= SUM(P(t-1)), validando la ausencia de valores negativos o discontinuidades en los sensores.
2. **Efecto de Borde por Inicialización:** Documentación explícita de los valores `null` generados por el parámetro `min_samples = h // 3`. Representa la ventana de calentamiento necesaria para que la métrica de saturación hídrica sea estadísticamente válida.
3. **Sensibilidad de Saturación Operativa:** Identificación del punto de inflexión donde las ventanas de 24h y 48h superan los umbrales críticos de absorción del suelo, señalando el inicio del riesgo aluvial.

## Estrategia de Despliegue

El proyecto adopta un enfoque de despliegue progresivo de estándar industrial:

* **Fase Exploratoria (`notebooks/01_aed_lluvias.ipynb`):** Prototipado de _notebook_ Jupyter, lectura inicial y visualización de datos para validación conceptual.
* **Fase de Producción (`src/`):** Modularización del código del _notebook_ en funciones puras y scripts ejecutables (ej.: `src/csv_to_parquet.py`) listos para ser orquestados por tareas programadas.
* **Fase de Reportabilidad y Dashboarding (GitHub Pages):** Renderizado y publicación del reporte web interactivo accesible de forma pública mediante [GitHub Pages](https://pablozunigac.github.io/lluvias-chile-2026).

## Configuración y Reproducción

### 1 Clonar el Repositorio

``` Bash
git clone https://github.com/pablozunigac/lluvias-chile-2026.git
cd lluvias-chile-2026
```

### 2 Entorno y Dependencias

## Entorno de Desarrollo y Dependencias

**Entorno Python**
Intérprete: Python 3.11+  

`polars` – Procesamiento y cálculo de medias móviles vectorizadas a alta velocidad.  
`plotly` – Motor de renderizado interactivo para mapas térmicos.  

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

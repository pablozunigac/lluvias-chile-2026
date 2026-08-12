# Modelo Estadístico para las Lluvias de 2026 en Chile

Este repositorio implementa una infraestructura analítica avanzada para la evaluación de eventos de precipitación extrema y saturación hídrica. Su propósito central es modelar la persistencia temporal de los frentes de mal tiempo mediante matrices de acumulación multi-ventana y mapas de calor interactivos, permitiendo anticipar el riesgo sistémico en contextos urbanos y rurales. Diseñado para mitigar escenarios críticos como desbordes fluviales, anegamientos severos e interrupción de infraestructura crítica, el sistema traduce pronósticos meteorológicos complejos en métricas accionables para la gestión de crisis y la toma de decisiones operativas en tiempo real.

---

## Contexto Histórico y Operativo: Temporal de Chile (Julio 2026)

El análisis de esta matriz se enmarca dentro del **Temporal de Chile de 2026**, un evento meteorológico extremo impulsado por un río atmosférico de categoría 5 y un "tren de sistemas frontales" continuo potenciado por el ciclo de El Niño. 

### Impacto y Métricas Clave del Evento

* **Afectación Territorial (Regiones de Coquimbo a Ñuble, excepto RM)**  
Las regiones comprendidas entre Coquimbo y Ñuble sufrieron estragos críticos, destacando la declaración de **_Estado de Catástrofe_** en la Región de Coquimbo y la Provincia de Huasco, daños severos en infraestructura hospitalaria (Ovalle), socavones viales en la Ruta 5 y vías costeras, y desbordes de ríos y esteros (como el río Elqui y el estero Tongoy). La Región de Valparaíso registró evacuaciones masivas por amenaza de desborde en esteros como el Marga Marga y Quilpué.

* **Víctimas y Emergencia:**  
A nivel nacional, el evento dejó un saldo preliminar de **15 fallecidos y 16 desaparecidos**, además de más de 16.000 personas damnificadas y cerca de 15.841 personas aisladas debido a la interrupción de rutas y bajadas de quebradas.

* **Intensidad, Concentración y Récords Históricos**  
El sistema presentó acumulados extremos de 200 a 350 mm entre Coquimbo y Ñuble bajo una dinámica ininterrumpida de frentes encadenados ("_tren de sistemas frontales_") desde el 14 de julio, generando saturación hídrica crítica, vientos destructivos y olas de hasta 5 metros. Esto marcó hitos en el top 5 histórico de julio, destacando La Serena (Estación La Florida) con 200,2 mm (máximo desde 1954), Combarbalá con 285,5 mm (récord absoluto), Valparaíso con 173,6 mm en 48 horas y un acumulado mensual de hasta 327,3 mm, y Chillán con 312,2 mm.

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

**Entorno Python**
Intérprete: Python 3.11+  

`polars` – Procesamiento y cálculo de medias móviles vectorizadas a alta velocidad.  
`plotly` – Motor de renderizado interactivo para mapas térmicos.  

---


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

### 1. Matriz de Saturación Multi-Ventana
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

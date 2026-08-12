# Modelo Estadístico para las Lluvias de 2026 en Chile

Este repositorio implementa una infraestructura analítica avanzada para la evaluación de eventos de precipitación extrema y saturación hídrica. Su propósito central es modelar la persistencia temporal de los frentes de mal tiempo mediante matrices de acumulación multi-ventana y mapas de calor interactivos, permitiendo anticipar el riesgo sistémico en contextos urbanos y rurales. Diseñado para mitigar escenarios críticos como desbordes fluviales, anegamientos severos e interrupción de infraestructura crítica, el sistema traduce pronósticos meteorológicos complejos en métricas accionables para la gestión de crisis y la toma de decisiones operativas en tiempo real.

![Mapa de Calor: Acumulación por ventanas de tiempo variables](web/assets/heatmap_01.png)

## Sección 1 – Contexto Climatológico Nacional: Chile, julio de 2026

En julio de 2026, la zona centro-norte de Chile enfrentó un evento hidrometeorológico crítico originado por el ingreso de un **río atmosférico de Categoría 5** acoplado a un tren de sistemas frontales encadenados, fenómeno intensificado por la fase cálida de El Niño. El evento causó una emergencia de escala nacional entre las regiones de Coquimbo y Ñuble, impactando severamente asentamientos urbanos, cadenas productivas y conectividad vial.

### Impacto Territorial, Humanitario e Infraestructura

* **Estado de Catástrofe e Impacto Humanitario**  
La magnitud del desastre motivó la declaración de *Estado de Catástrofe* en la Región de Coquimbo y la Provincia de Huasco. El saldo nacional registró **15 personas fallecidas, 16 desaparecidas**, más de 16.000 damnificados y sobre 15.800 personas aisladas por colapsos viales.
* **Infraestructura Critica y Cauces**  
Se registraron socavamientos mayores en la Ruta 5 y vías costeras, daños en la infraestructura hospitalaria de Ovalle y desbordes de cauces principales como el río Elqui y el estero Tongoy en Coquimbo, además de evacuaciones masivas en la Región de Valparaíso por la crecida de los esteros Marga Marga y Quilpué.

### Registros Históricos y Dinámica de Saturación

El frente descargó acumulados continuos de **200 a 350 mm en menos de 72 horas**, alcanzando hitos no registrados en décadas:

* **Valdivia (Estación Pichoy):** 683.3 mm, estableciendo un nuevo récord histórico absoluto para un mes de julio.  
* **Combarbalá (Región de Coquimbo):** 285.5 mm, alcanzando el primer lugar histórico para las mediciones de julio en la zona.  
* **Osorno (Estación Cañal Bajo):** 330.2 mm, ubicándose en el tercer lugar histórico de la estación.  
* **Rodelillo (Valparaíso):** 327.3 mm acumulados durante todo el mes, situándose en el quinto lugar histórico de su serie de mediciones.  
* **La Serena (Estación La Florida):** 200.2 mm, el registro más alto para un mes de julio desde que existen datos en el aeródromo.

### Respuesta Analítica e Infraestructura de Datos

Frente a la rápida saturación de suelos y el riesgo aluvial, este repositorio despliega un **modelo estocástico y matricial** diseñado para procesar telemetría de precipitación y anticipar la saturación hídrica mediante ventanas móviles (6h a 96h). El sistema convierte registros puntuales en métricas operativas directas para respaldar evacuaciones preventivas y la protección de infraestructura crítica así como un soporte para el análisis avanzado para las precipitaciones del pasado.

## Sección 2 – Arquitectura del Repositorio

El proyecto mantiene un desacoplamiento estricto entre los datos primarios, la exploración interactiva, el código fuente modular y los artefactos exportados.

```text
lluvias-chile-2026/
├── .github/
│   └── workflows/
│       └── deploy.yml           # Pipeline CI/CD para compilación y despliegue a GitHub Pages
├── .vscode/                     # Configuración de workspace local, linters y ajustes de editor
├── data/                        # Almacenamiento y gestión de datasets
│   ├── processed/               # Matrices serializadas en .parquet con tipos optimizados
│   └── raw/                     # Telemetría meteorológica cruda en .csv
├── notebooks/                   # Sandboxes .ipynb de exploración, AED e hipótesis de modelado
│   └── 01_aed_lluvias.ipynb    
├── output/                      # Artefactos analíticos y reportes finales
│   ├── data_exports/            # Resúmenes consolidados en .csv/.xlsx
│   └── reports/                 # Reportes estáticos exportados (.pdf/.html)
├── src/                         # Código fuente modular .py de producción en Python
│   └── csv_to_parquet.py
├── tests/                       # Pruebas unitarias e integración .py (pytest)
│   ├── test_etl.py              # Validación del pipeline Polars y esquema .parquet
│   └── test_model.py            # Tests de consistencia matemática
├── web/                         # Motor de documentación interactiva en Quarto
│   ├── assets/                  # Recursos gráficos finales (.png, .SVG, diagramas)
│   ├── _quarto.yml              # Configuración global del sitio interactivo
│   ├── aed.qmd                  # Documentación del pipeline de ingesta
│   ├── index.qmd                # Resumen ejecutivo e impacto operativo
│   └── modelo.qmd               # Modelación matemática EVT
├── .gitignore                   # Reglas de exclusión para archivos pesados y temporales
├── pyproject.toml               # Definición estándar del proyecto y dependencias (PEP 621)
└── README.md                    # Documentación técnica principal del repositorio
```

## Sección 3 – Origen y Estructura de los Datos

Los datos analizados provienen de registros de precipitación recopilados mediante _scraping_ estructurado e integración del modelo **ECMWF (_European Centre for Medium-Range Weather Forecasts_)** a través de la plataforma Windy.com.

* **Frecuencia de Muestreo:** Intervalos de 3 horas.
* **Estructura Cruda:** `data/raw/Lluvia_2026_v2.csv`
* **Variables del _scraping_:** `fecha`, `hora`, `lluvia_mm`

## Sección 4 – Pipeline ETL (Extract, Transform, Load)

El pipeline de datos está construido sobre **Polars** para garantizar máxima velocidad de procesamiento en memoria mediante ejecución vectorizada:

* **_Extract_:** Lectura resuelta mediante `pathlib` dinámico para garantizar portabilidad entre SO, con esquema tipado explícito (`hora` -> `Int32`, `fecha` -> `Float64`, `lluvia_mm` -> `Float64`).  
* **_Transform_:**
   * Reconstrucción del sello temporal absoluto (`datetime`): Conversión de la fecha flotante de serial Excel a `Date` y posterior combinación vectorial con el entero de hora.
   * Ordenamiento cronológico garantizado (`sort("datetime")`).  
* **_Load_:** Exportación en formato columnar **Parquet** en `data/processed/lluvia_2026_matrix.parquet`, preservando metadatos de tipo y nulos de inicialización.

## Sección 5 – Modelo Analítico y Caracterización Estadística

### Matriz de Saturación Multi-Ventana

Para medir la persistencia temporal, el modelo calcula una matriz de medias móviles ($\text{MA}$) sobre las ventanas temporales $h \in  6 \cup \{12, 24,\ldots, 96\}$ horas:

$$\text{MA}_h(t) = \frac{1}{k} \sum_{i=0}^{k-1} P(t - i)$$

Donde $P(t)$ representa la precipitación registrada en el tiempo $t$ y $k = \frac{h}{3}$ corresponde al número de periodos de 3 horas contenidos dentro de la ventana de acumulación $h$.

### Ajuste de Distribución de Valores Extremos (EVT)

Los picos de intensidad máxima se modelan mediante una **Distribución Gumbel** para estimar las probabilidades de excedencia y períodos de retorno ($T$) ante eventos hidrometeorológicos de $h$-horas:

$$F(x; \mu, \beta) = \exp\left(-\exp\left(-\frac{x - \mu}{\beta}\right)\right)$$

Donde $\mu$ es el parámetro de localización (centro de la distribución de picos) y $\beta$ es el parámetro de escala ($\beta > 0$).

## Sección 6 – Evaluación y Validación del Modelo

* **Monotonicidad de la Suma Acumulada:**  
Se verifica formalmente la condición de no negatividad y continuidad en las lecturas de los sensores, lo que garantiza la coherencia temporal y la ausencia de valores anómalos o discontinuidades:

$$\sum_{i=0}^{t} P(i) \ge \sum_{i=0}^{t-1} P(i) \quad , \forall t$$

* **Efecto de Borde por Inicialización**  
Documentación explícita de los valores `null` generados por el parámetro `min_samples = h/3`. Representa la ventana de calentamiento necesaria para que la métrica de saturación hídrica sea estadísticamente válida.

* **Sensibilidad de Saturación Operativa**  
Identificación del punto de inflexión donde las ventanas de 24h y 48h superan los umbrales críticos de absorción del suelo, señalando el inicio del riesgo aluvial.

## Sección 7 – Estrategia de Despliegue

El proyecto adopta un enfoque de despliegue progresivo de estándar industrial:

* **Fase Exploratoria:** `notebooks/01_aed_lluvias.ipynb`  
Prototipado de _notebook_ Jupyter, lectura inicial y visualización de datos para validación conceptual.
* **Fase de Producción:** `src/`   
Modularización del código del _notebook_ en funciones puras y scripts ejecutables listos para ser orquestados por tareas programadas.
* **Fase de Reportabilidad y Dashboarding (GitHub Pages)**  
Renderizado y publicación del reporte web interactivo accesible de forma pública mediante [GitHub Pages](https://pablozunigac.github.io/lluvias-chile-2026).

## Sección 8 – Configuración y Reproducción

### Clonación del Repositorio

``` Bash
git clone https://github.com/pablozunigac/lluvias-chile-2026.git
cd lluvias-chile-2026
```

### Entorno y Dependencias (Python 3.11+)

```Bash
uv add polars plotly
```

### Ejecución del _Notebook_ Exploratorio

``` Bash
jupyter notebook notebooks/01_aed_lluvias.ipynb
```

### Ejecución del Pipeline ETL a Parquet

``` Bash
python3 src/csv_to_parquet.py
```

## Sección 9 – Perfil Profesional y Contacto

**Perfil Profesional & Reportes:** [pablozunigac.github.io ↗](https://pablozunigac.github.io)  
**Contacto Directo:** [pablo.zuniga.c@gmail.com](mailto:pablo.zuniga.c@gmail.com)
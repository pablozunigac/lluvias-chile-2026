# Modelo Estadístico para las Lluvias de 2026 en Chile

Este repositorio implementa una infraestructura analítica avanzada para la evaluación de eventos de precipitación extrema, intensidad de tormenta y saturación hídrica progresiva. Su propósito central es modelar la persistencia temporal de los frentes de mal tiempo mediante matrices de acumulación multi-ventana, caracterización de valores extremos y mapas de calor interactivos, permitiendo anticipar el riesgo hídrico en entornos urbanos, agrícolas y mineros. 

Diseñado para traducir datos crudos de precipitación en métricas accionables de soporte a la decisión, el sistema evalúa la acumulación de lluvia sobre ventanas móviles de 6 a 96 horas para predecir escenarios de saturación de suelos, riesgo de aluviones e interrupción de infraestructura crítica.

---

## Contexto Climatológico e Histórico: Temporal de Chile (Julio 2026)

El análisis se enmarca en el **Temporal de Chile de julio de 2026**, un evento meteorológico de magnitud extraordinaria caracterizado por la entrada de un río atmosférico de Categoría 5 y una dinámica de "tren de sistemas frontales" encadenados, potenciados por la fase cálida del ciclo ENOS (El Niño).

### Impacto Territorial y Récords Hidrometeorológicos

* **Mapeo de Afectación (Coquimbo a Ñuble):** Declaración de *Estado de Catástrofe* en la Región de Coquimbo y la Provincia de Huasco. Desbordes masivos de cauces (Río Elqui, Estero Tongoy, Estero Marga Marga y Estero Quilpué en la Región de Valparaíso), socavamiento de infraestructura vial en la Ruta 5 y aislamiento de localidades por bajadas de quebradas.
* **Magintud del Desastre:** Saldo nacional preliminar de 15 fallecidos, 16 desaparecidos, más de 16.000 personas damnificadas y sobre 15.800 personas en estado de aislamiento por falla de conectividad crítica.
* **Anomalía de Precipitación y Récords:** Registro de acumulados continuos entre 200 mm y 350 mm en menos de 72 horas. Destacan los hitos históricos de la Estación La Florida (La Serena) con 200.2 mm (máximo histórico desde 1954), Combarbalá con 285.5 mm (récord absoluto registrado), Valparaíso con 173.6 mm en 48 horas (acumulado mensual de 327.3 mm) y Chillán con 312.2 mm.

---

## Origen y Estructura de los Datos

Los datos analizados provienen de registros de precipitación en tiempo casi real recopilados mediante *scraping* estructurado e integración del modelo **ECMWF (European Centre for Medium-Range Weather Forecasts)** a través de la plataforma Windy.

* **Frecuencia de Muestreo:** Registros discretos agregados en intervalos de 3 horas.
* **Estructura Cruda (`data/raw/Lluvia_2026_v2.csv`):**
  * `fecha`: Formato serial flotante (días transcurridos desde el origen cronológico 1899-12-30).
  * `hora`: Intervalos enteros de 0 a 21 horas (pasos de 3h).
  * `lluvia_mm`: Precipitación acumulada en el intervalo en milímetros (mm).

---

## Arquitectura del Repositorio

El proyecto mantiene un desacoplamiento estricto entre los datos primarios, la exploración interactiva, el código fuente modular de producción y los artefactos exportados.

```text
lluvias-chile-2026/
├── .devcontainer/       # Configuración de entorno aislado en Docker / VS Code
├── .github/             # Pipelines de CI/CD para automatización y GitHub Pages
├── data/                # Gestión de datasets
│   ├── processed/       # Matrices serializadas en Parquet con tipos optimizados
│   └── raw/             # Archivos CSV crudos (Lluvia_2026_v1.csv, Lluvia_2026_v2.csv)
├── node_modules/        # Dependencias de herramientas auxiliares JS
├── notebooks/           # Entorno de exploración, AED e hipótesis de modelado
│   └── 01_aed_lluvias.ipynb
├── output/              # Gráficos vectoriales, reportes HTML y artefactos finales
├── R/                   # Scripts legados y procesamiento estadístico complementario
├── src/                 # Código fuente modular de producción en Python
│   ├── csv_to_parquet.py
│   └── open_meteo.js
├── .gitignore           # Exclusión de archivos pesados y temporales
├── package-lock.json
├── package.json
└── README.md            # Documentación técnica del proyecto
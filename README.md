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
git clone https://github.com/pablozunigac/lluvias-chile-2026.git
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

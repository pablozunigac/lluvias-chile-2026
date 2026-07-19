# Modelo Estadístico para las Lluvias de 2026 en Chile

Este repositorio contiene la infraestructura de datos, el flujo ETL (_Extract_, _Transform_, _Load_) y los modelos estadísticos diseñados para analizar las precipitaciones en Chile durante el año 2026. El objetivo es estructurar visualizaciones de datos para las series de tiempo meteorológicas pronosticadas por Windy (ECMWF) para la Región de Valparaíso para julio de 2026.

---

## Arquitectura del Proyecto

El proyecto sigue una estructura modular para reducir la fricción en el manejo de datos y código:

* **`./R`** : Scripts ETL (incluye formateo temporal) y dataviz
  * `00-lectura-ETL.R` : Script principal de importación, limpieza y formateo temporal  
* **`./data`** : Archivos de datos sin procesar
  * `lluvia_2026_v1.csv` : Lluvias entre jueves 16 y sábado 17 de julio de 2026 (Actualización: jueves, 11am)
  * `lluvia_2026_v2.csv` : Lluvias entre jueves 16 y martes 21 de julio de 2026 (Actualización: domingo, 5am)  
* **`./output`** : Resultados, gráficos y datos procesados listos para exportación  
### `Metadatos GitHub`
  * `./README.md` : Documentación técnica del repositorio
  * `./.gitignore`: Reglas de exclusión para archivos temporales y datos pesados

---

## Metodología y Modelo Estocástico
Este repositorio implementa un modelo estocástico enfocado en la modelación paramétrica y el análisis de persistencia temporal de las precipitaciones pronosticadas. El flujo metodológico y analítico contempla:

* **Análisis de Frecuencia Marginal**  
Despliegue gráfico continuo de la cantidad marginal de lluvia en milímetros (mm) agregada en intervalos estricto de 3 horas.
* **Cálculo de Persistencia y Acumulación**  
Determinación de la suma acumulada móvil con ventana hacia el pasado para bloques críticos de 6, 12, 24, 36, 48, 60 y 72 horas (desarrollado mediante la librería `slider`).
* **Análisis de Distribución Puntual**  
Evaluación de la distribución probabilística de la lluvia pronosticada a partir de las observaciones fijas cada 3 horas, segmentadas de acuerdo a los momentos de actualización de cada conjunto de datos.
* **Ajuste Paramétrico**  
Ajuste de las observaciones a funciones de distribución de probabilidad para la estimación de periodos de retorno y cuantiles de eventos extremos.
* **Visualización Integrada**  
Consolidación de todos los componentes analíticos en un único metagráfico interactivo y unificado bajo una interfaz tipo tablero de control (desarrollado mediante `plotly`).

---

## Entorno de Desarrollo
- **IDE:** Positron 2026.07.0 build 365
- **Lenguaje:** R 4.5.2
- **Librerías de R**
  - `here` : Resolución de rutas absolutas basada en el anclaje raiz del proyecto
  - `lubridate` : Transformación y tratamoiento eficiente de fechas y zonas horarias
  - `plotly` : Gráficos interactivos y dinámicos para exploración de datos
  - `slider` : Cálculo eficiente de ventanas móviles y promedios acumulados
  - `tidyverse` : Colección de paquetes para ciencia de datos y transformación de estructuras
  - `tsibble` : Estructuras de datos y herramientas optimizadas para series de tiempo

---

## Configuración y Reproducción
Para ejecutar este proyecto de forma local sin errores de rutas absolutas, asegúrate de clonar el repositorio dentro de tu entorno de trabajo:

### 1. Requisitos Previos
* **Entorno:** Positron IDE (versión 2026.07.0 o superior) o RStudio.
* **Lenguaje:** R (versión >= 4.5.2).

### 2. Gestión de Dependencias
Asegúrate de contar con los siguientes paquetes instalados. Puedes ejecutarlos directamente en la consola de R:
   ```R
   install.packages(c( 'here', 'lubridate', 'plotly', 'slider', 'tidyverse', 'tsibble'))
   ```

### 3. Clonación e Inicio
Clona este repositorio en tu máquina local:
  ```bash
  git clone https://github.com/pablozunigac/lluvias-chile-2026.git
  ```

### 4. Ejecución de Código
Para procesar los datos crudos y ejecutar el modelo, ejecuta el _script_ principal desde la consola de R:
  ```R
  source('R/00-lectura-ETL.R')
  ```


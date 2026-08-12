# %% [1] Importación de librerías y rutas
from pathlib import Path
import plotly.express as px
import polars as pl

# %% [2] Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_CSV_PATH = BASE_DIR / "data" / "raw" / "Lluvia_2026_v2.csv"
PROCESSED_PARQUET_PATH = BASE_DIR / "data" / "processed" / "lluvia_2026.parquet"
ASSETS_DIR = BASE_DIR / "output" / "assets"


def process_rain_matrix_and_visualize() -> None:
    if not RAW_CSV_PATH.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {RAW_CSV_PATH}")

    print(f"Leyendo .csv: {RAW_CSV_PATH.name}")

    # Cargar .csv delimitado por punto y coma
    df_raw = pl.read_csv(
        RAW_CSV_PATH,
        separator=";",
        schema_overrides={
            "hora": pl.Int32,
            "fecha": pl.Float64,
            "lluvia_mm": pl.Float64,
        },
    )

    # Formatear marca temporal y ordenar matriz
    df_base = (
        df_raw.with_columns(
            fecha_date=pl.date(1899, 12, 30) + pl.duration(days=pl.col("fecha"))
        )
        .with_columns(
            datetime=pl.col("fecha_date").dt.combine(
                pl.time(hour=pl.col("hora"), minute=0, second=0)
            )
        )
        .sort("datetime")
    )

    # Definir ventanas de tiempo (6h, 12h,..., 96h de a 12h) -> 3h por registro
    target_hours = [6] + list(range(12, 97, 12))

    # Expresiones vectorizadas para medias móviles hacia atrás
    rolling_exprs = [
        pl.col("lluvia_mm")
        .rolling_mean(window_size=(h // 3), min_samples=(h // 3))
        .alias(f"ma_{h}h")
        for h in target_hours
    ]

    # Construir matriz completa con suma acumulada y medias móviles
    df_matrix = df_base.with_columns(
        [pl.col("lluvia_mm").cum_sum().alias("sum_acum")] + rolling_exprs
    )

    # Reordenar columnas para la matriz
    ma_cols = [f"ma_{h}h" for h in target_hours]
    final_cols = ["datetime", "fecha_date", "hora", "lluvia_mm", "sum_acum"] + ma_cols
    df_final = df_matrix.select(final_cols)

    # Almacenar Matriz de valores completos en .parquet
    PROCESSED_PARQUET_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_final.write_parquet(PROCESSED_PARQUET_PATH, compression="snappy")
    print(f"⚡ Matriz guardada en Parquet: {PROCESSED_PARQUET_PATH}")

    # Desplegar matriz calculada en pantalla
    print("\nDespliegue de la Matriz Calculada:")
    pl.Config.set_tbl_cols(len(final_cols))
    pl.Config.set_tbl_rows(20)
    print(df_final)

    # Generar Mapa de Calor Interactivo de la Matriz Completa (Plotly)
    print("\nGenerando Mapa de Calor de Concentración de Lluvia...")

    df_plot = df_final.with_columns(
        pl.col("datetime").dt.strftime("%Y-%m-%d %H:00").alias("datetime_str")
    )

    timestamps = df_plot["datetime_str"].to_list()
    matrix_values = df_plot.select(ma_cols).to_numpy().T

    fig = px.imshow(
        matrix_values,
        labels=dict(x="Tiempo", y="Ventana Temporal", color="Precipitación Prom. (mm)"),
        x=timestamps,
        y=[f"{h}h" for h in target_hours],
        color_continuous_scale="Reds",
        title="Matriz de Concentración Temporal de Lluvia (Medias Móviles)",
        aspect="auto",
    )

    fig.update_xaxes(side="bottom", tickangle=-45)
    fig.update_layout(
        xaxis_title="Tiempo (Fecha / Hora)",
        yaxis_title="Ventana Móvil Hacia Atrás",
        coloraxis_colorbar=dict(title="mm/h Promedio"),
    )

    # Exportación automática de imagen para el README.md
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    heatmap_path = ASSETS_DIR / "rain_heatmap.png"
    fig.write_image(heatmap_path, scale=2)
    print(f"📊 Artefacto estático exportado para README: {heatmap_path}")

    # Mostrar interactivo sólo si es ejecución local
    try:
        fig.show()
    except Exception:
        pass


if __name__ == "__main__":
    process_rain_matrix_and_visualize()
# %%
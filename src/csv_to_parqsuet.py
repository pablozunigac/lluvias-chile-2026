from pathlib import Path
import pandas as pd

# Rutas desde src/
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def convert_raw_csv_to_parquet():
    csv_files = list(RAW_DIR.glob("*.csv"))

    if not csv_files:
        print("⚠️ No hay CSVs en data/raw/")
        return

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    for file_path in csv_files:
        print(f"🔄 Procesando: {file_path.name}...")
        df = pd.read_csv(file_path)
        output_path = PROCESSED_DIR / f"{file_path.stem.lower()}.parquet"
        df.to_parquet(output_path, engine="pyarrow", compression="snappy")
        print(f"✅ Convertido: {output_path.name}")


if __name__ == "__main__":
    convert_raw_csv_to_parquet()
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

csv_file = Path("output/taxi_zone_lookup.csv")

if not csv_file.exists():
    raise FileNotFoundError(f"{csv_file} not found")

df = pd.read_csv(csv_file)

engine = create_engine(
    "postgresql://root:root@localhost:5432/ny_taxi"
)

df.to_sql(
    "zones",
    engine,
    if_exists="replace",
    index=False
)

print("Zones table loaded successfully!")
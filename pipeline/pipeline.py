import sys
from pathlib import Path

import pandas as pd

print("arguments:", sys.argv)

month = int(sys.argv[1])

df = pd.DataFrame({"day": [1, 2], "num_passengers": [3, 4]})
df["month"] = month
print(df.head())

Path("output").mkdir(parents=True, exist_ok=True)

df.to_parquet(f"output/{month}.parquet", engine="pyarrow", index=False)
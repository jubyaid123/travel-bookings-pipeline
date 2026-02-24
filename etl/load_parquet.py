import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

def write_parquet(df, output_dir):
    table = pa.Table.from_pandas(df)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    pq.write_to_dataset(
        table,
        root_path=output_dir,
        partition_cols=["arrival_date"]
    )

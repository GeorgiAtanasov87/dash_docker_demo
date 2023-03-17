import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy import select, text
import numpy as np

from read_files import config, transform_data_to_cet_eur

engine = create_engine("sqlite+pysqlite:///../../data/data.db", echo=False)
data_folder = config['data_folder']

with engine.begin() as conn:
    conn.execute(text(""" DROP TABLE IF EXISTS markets_data ;"""))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS markets_data (
        utc_timestamp int,
        country varchar(2),
        price_eur float,
        PRIMARY KEY (utc_timestamp, country));
    """)
    )
    all_files = os.listdir(data_folder)
    files_list = [f for f in sorted(all_files) if f.endswith(f".csv")]

    files = [ (transform_data_to_cet_eur(f"{data_folder}/{file_name}"), file_name ) for file_name in files_list]
    for df, file_name in files:
        country_name = file_name.replace("-DAM-PRICES-", " ")
        df = df.drop(columns=["cet_timestamp"])
        df["country"] = country_name[:2]
        df.index = df.index.astype(np.int64)
        try:
            df.to_sql("markets_data", if_exists="append", con=conn)
        except Exception as e:
            print(f"--------\n ERROR for file {file_name}\n--------")
            print(e)
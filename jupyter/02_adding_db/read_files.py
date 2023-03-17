import pandas as pd
import pendulum
import re
import os
import yaml
from sqlalchemy import create_engine
from sqlalchemy import select, text
import numpy as np

def read_file(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, na_values=["-"])
    df.dropna(thresh=3, inplace=True)
    return df
    

def parse_column_names(df: pd.DataFrame) -> dict[str]:
    """ Get metadata from column names """
    price_column = [x for x in df.columns if x.startswith('Day-ahead Price')][0]
    
    timestamp_column = [x for x in df.columns if x.startswith('MTU')][0]
    tz_name = tz_mapper[re.search(r"MTU \((.*?)\)", timestamp_column).group(1)]
    country = [x for x in df.columns if x.startswith('BZN|')][0].replace("BZN|","")
    return {"price_column": price_column, "timestamp_column": timestamp_column,
            "time_zone": tz_name, "country": country}


def parse_timestamp(value: str, source_tz: str, output_tz: str = "UTC") -> pendulum.DateTime:
    "Parse string to timezone aware datetime"
    tz_obj = pendulum.timezone(source_tz)
    date_str = f"{value.split(' - ')[0]}"
    return pendulum.from_format(date_str, 'DD.MM.YYYY HH:mm', tz=tz_obj).in_tz(output_tz)


def gen_utc_index(df: pd.DataFrame, timestamp_column: str, timezone: str) -> pd.DatetimeIndex:
    """Returns a datetime index for the data period. Fails if provided incomplete data"""
    start_timestamp = parse_timestamp(
        value=df[timestamp_column].iloc[0], 
        source_tz=timezone, 
        output_tz="UTC"
    )
    
    end_timestamp = parse_timestamp(
        value=df[timestamp_column].iloc[-1], 
        source_tz=timezone, 
        output_tz="UTC"
    )
    
    utc_index = pd.date_range(start=start_timestamp, end=end_timestamp, freq="h", name="utc_timestamp")
    if len(utc_index) == len(df[timestamp_column]):
        return utc_index
    else:
        raise Exception(f"Data has time gaps! Available {len(df[timestamp_column])} out of {len(utc_index)} values")
        

def price_to_eur(df: pd.DataFrame, price_column: str, currency_column: str) -> pd.Series:
    """ Return a series with price converted to EUR """
    return round(df[price_column] * df[currency_column].map(currency_mapper), 2)


def transform_data_to_cet_eur(path: str) -> pd.DataFrame:
    """ Transforms the input file to a dataframe with UTC
    and CET timestamps and price in EUR/MWh
    """
    df = read_file(path)
    metadata = parse_column_names(df)
    
    df.index = gen_utc_index(df, metadata['timestamp_column'], metadata["time_zone"]) 
    df["cet_timestamp"] = df.index.tz_convert("CET")
    df["price_eur"] = price_to_eur(df=df, price_column=metadata["price_column"], currency_column="Currency")
    return df[["cet_timestamp", "price_eur"]]


def read_config(path: str = "config.yml") -> dict:
    with open(path, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    return data_loaded
 

config = read_config()
tz_mapper = config["tz_mapper"]
currency_mapper = config["currency_mapper"]
data_folder = config["data_folder"]

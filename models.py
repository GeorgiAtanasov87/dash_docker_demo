import pandas as pd
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
import numpy as np
from zoneinfo import ZoneInfo
import re
import pendulum

tz_mapper = {"CET/CEST": "CET", "EET/EEST": "EET"}


class Currency(Enum):
    eur = "EUR"
    bgn = "BGN"


class Timezones(Enum):
    cet = "CET"
    eet = "EET"


class DayAheadMarket(BaseModel):
    utc_timestamp: int
    tz_timestamp: int
    price: int
    currency: Currency


class ENTSOEDAM:

    def parse_column_names(self, columns: list[str]):
        tz_name = tz_mapper[re.findall(r"MTU \((.*?)\)", columns[0])[0]]
        print("TIMEZONE NAME:", tz_name)
        currency = "EUR"
        return tz_name

    def parse_timestamp(self, value: str, source_tz: str, output_tz: str = "UTC"):
        "Parse srting to timezone aware datetime"
        date_str = f"{value.split(' - ')[0]}" 
        tz_obj = pendulum.timezone(source_tz)
        return pendulum.from_format(date_str, 'DD.MM.YYYY HH:mm', tz=tz_obj).in_tz(output_tz)

    def tz_to_utc(self, tz_aware_timestamp: datetime):
        # print("TIMESTAMP:", tz_aware_timestamp)
        return tz_aware_timestamp.astimezone(ZoneInfo("UTC")).replace(tzinfo=None)

    def from_csv(self, path: str) -> DayAheadMarket:
        df = pd.read_csv(path)
        time_zone = self.parse_column_names(df.columns)
        df["tz_timestamp"] = df[df.columns[0]].apply(
            self.parse_timestamp, args=[time_zone]
        )
        df["utc_timestamp"] = df["tz_timestamp"].apply(self.tz_to_utc)

        print(df.head())
        self.parse_column_names(df.columns)
        return df

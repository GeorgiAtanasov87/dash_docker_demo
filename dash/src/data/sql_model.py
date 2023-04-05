from sqlalchemy import String, Select, Connection
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import create_engine
from sqlalchemy import func
import datetime as dt
import pytz
from sqlalchemy.orm import Session

from sqlalchemy.ext.hybrid import hybrid_property
import pandas as pd


Base = declarative_base()


class DayAheadMarket(Base):
    """Represents table markets_data in sqllite db"""

    __tablename__ = "markets_data"
    utc_timestamp: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(2), primary_key=True)
    price_eur: Mapped[float]

    @hybrid_property
    def utc(self) -> dt.datetime:
        """return datetime object in UTC"""
        return dt.datetime.fromtimestamp(
            self.utc_timestamp / 1e9,
            tz=pytz.utc,
        )

    @hybrid_property
    def cet(self) -> dt.datetime:
        """return tz aware datetime object in CET"""
        return dt.datetime.fromtimestamp(
            self.utc_timestamp / 1e9, tz=pytz.utc
        ).astimezone(pytz.timezone("CET"))

    def _as_dataframe(self, stmt: Select | None, con: Connection) -> pd.DataFrame:
        """Read sqlalchemy Select statement as pandas DataFrame"""
        df = pd.read_sql_query(
            stmt,
            con=con,
            index_col="utc_timestamp",
            parse_dates={"utc_timestamp": "ns"},
            dtype={"country": "category", "price_eur": "float"},
        ).tz_localize("utc")
        df.insert(0, "cet", df.index.tz_convert("CET"))
        return df

    @classmethod
    def filter_by_country(
        cls, countries: list[str] | None, con: Connection
    ) -> pd.DataFrame:
        stmt = Select(cls).where(cls.country.in_(countries))
        return cls._as_dataframe(cls, stmt, con=con)

    @classmethod
    def all(cls, con: Connection) -> pd.DataFrame:
        return cls._as_dataframe(cls, Select(cls), con=con)

    @classmethod
    def countries(cls, con: Connection) -> list[str]:
        """Returns a list of all available countries"""
        stmt = Select(cls.country).distinct()
        return con.scalars(statement=stmt).all()

    @classmethod
    def data_range(
        cls, countries: list[str], con: Connection
    ) -> dict[str, dt.datetime]:
        """Retuns the min/max dates for a list of countries"""
        stmt = Select(
            func.min(cls.utc_timestamp),
            func.max(cls.utc_timestamp),
        ).where(cls.country.in_(countries))
        min, max = con.execute(stmt).one()

        def to_cet(utc_timestamp):
            """Convert utc epoch to datetime object in cet"""
            return dt.datetime.fromtimestamp(
                utc_timestamp / 1e9, tz=pytz.utc
            ).astimezone(pytz.timezone("CET"))

        return {"min_date": to_cet(min), "max_date": to_cet(max)}

    def __repr__(self) -> str:
        return f"DAM(country={self.country!r}, utc={self.utc.strftime('%Y-%m-%d %H:%M:%S')!r}, cet={self.cet.strftime('%Y-%m-%d %H:%M:%S')!r}, price={self.price_eur!r})"


if __name__ == "__main__":
    DB_PATH = "../../dam_data/data.db"
    engine = create_engine(f"sqlite:///{DB_PATH}")
    session = Session(engine)
    connection = session.connection()
    # df = DayAheadMarket.all(con=connection)
    # data = df.pivot_table(
    #     index=["cet"], columns=["country"], values="price_eur"
    # ).tz_localize(None)
    # data = data.groupby(pd.Grouper(freq="d")).mean().round(2)
    # print(df.tz_localize(None).head())
    # print(df.info())
    # print(df.pivot_table(index=['cet'], columns=['country'], values='price_eur').tz_localize(None))
    # print(df.iloc[:20])
    # print(data.head())

    print(DayAheadMarket.data_range(countries=["BG", "HU"], con=connection))

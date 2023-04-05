import i18n
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from . import ids
from ..data.sql_model import DayAheadMarket
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
import datetime as dt


def render(app: Dash, session: Session) -> html.Div:
    @app.callback(
        [
            Output(ids.DAM_DATE_PICKER, "min_date_allowed"),
            Output(ids.DAM_DATE_PICKER, "max_date_allowed"),
        ],
        [
            Input(ids.DAM_COUNTRIES_DROPDOWN, "value"),
        ],
    )
    def limit_period(countries: list[str]) -> dt.datetime:
        data_range = DayAheadMarket.data_range(
            countries=countries, con=session.connection()
        )
        return data_range["min_date"].replace(tzinfo=None), data_range[
            "max_date"
        ].replace(tzinfo=None)

    return html.Div(
        children=[
            html.H6(i18n.t("general.period")),
            dcc.DatePickerRange(
                id=ids.DAM_DATE_PICKER,
                display_format="YYYY-MM-DD",
                min_date_allowed=date(2020, 1, 1),
                max_date_allowed=date(2023, 3, 3),
                # initial_visible_month=date(2023, 2, 5),
                start_date=date(2023, 1, 1),
                end_date=dt.date.today() + dt.timedelta(days=1),
            ),
        ],
    )

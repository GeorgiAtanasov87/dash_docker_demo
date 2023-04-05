import i18n
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# from ..data.source import DataSource
from . import ids
from .dropdown_helper import to_dropdown_options
from ..data.sql_model import DayAheadMarket
from sqlalchemy.orm import Session


def render(app: Dash, session: Session) -> html.Div:
    @app.callback(
        Output(ids.DAM_COUNTRIES_DROPDOWN, "value"),
        [
            Input(ids.SELECT_ALL_COUNTRIES_BUTTON, "n_clicks"),
        ],
    )
    def select_all_countries(_: int) -> list[str]:
        return DayAheadMarket.countries(con=session.connection())

    return html.Div(
        children=[
            html.H6(i18n.t("general.country")),
            dcc.Dropdown(
                id=ids.DAM_COUNTRIES_DROPDOWN,
                options=to_dropdown_options(
                    DayAheadMarket.countries(con=session.connection())
                ),
                value=DayAheadMarket.countries(con=session.connection()),
                multi=True,
                placeholder=i18n.t("general.select"),
            ),
            html.Button(
                className="dropdown-button",
                children=[i18n.t("general.select_all")],
                id=ids.SELECT_ALL_COUNTRIES_BUTTON,
                n_clicks=0,
            ),
        ],
    )

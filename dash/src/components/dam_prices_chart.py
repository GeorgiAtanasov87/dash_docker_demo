import pandas as pd
from datetime import date
from sqlalchemy.orm import Session
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from ..data.sql_model import DayAheadMarket
from . import ids
import i18n


def render(app: Dash, session: Session):
    def transform_data(
        data: pd.DataFrame, aggregation: str, start_date: date, end_date: date
    ) -> pd.DataFrame:
        """Pivot and aggregate timeseries DataFrame"""
        pivot = data.pivot_table(
            index=["cet"], columns=["country"], values="price_eur"
        ).tz_localize(None)
        transformed_data = (
            pivot.loc[start_date:end_date]
            .groupby(pd.Grouper(freq=aggregation))
            .mean()
            .round(2)
        )
        return transformed_data

    @app.callback(
        Output(ids.DAM_PRICES_CHART, "children"),
        [
            Input(ids.DAM_COUNTRIES_DROPDOWN, "value"),
            Input(ids.DAM_AGGREGATION_DROPDOWN, "value"),
            Input(ids.DAM_DATE_PICKER, "start_date"),
            Input(ids.DAM_DATE_PICKER, "end_date"),
        ],
    )
    def plot_prices(
        countries: list[str], aggregation: str, start_date: date, end_date: date
    ) -> dcc.Graph:
        df = DayAheadMarket.filter_by_country(
            countries=countries, con=session.connection()
        )
        data = transform_data(
            data=df, aggregation=aggregation, start_date=start_date, end_date=end_date
        )
        with fig.batch_update():
            fig.data = []
            columns = countries
            [fig.add_scatter(y=data[col], x=data.index, name=col) for col in columns]

        return html.Div(dcc.Graph(figure=fig), id=ids.DAM_PRICES_CHART)

    fig = go.Figure()
    fig.update_layout(
        height=900,
        title_text=i18n.t("chart.title"),
        xaxis_title=i18n.t("chart.xaxis_title"),
        yaxis_title=i18n.t("chart.yaxis_title"),
        showlegend=True,
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        ),
    )

    return html.Div(id=ids.DAM_PRICES_CHART)

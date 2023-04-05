from dash import Dash, html, dcc
from src.components import (
    dam_prices_chart,
    dam_countries_dropdown,
    dam_aggregation_dropdown,
    dam_date_picker,
)

import src.components.ids as ids
from sqlalchemy.orm import Session


def create_layout(app: Dash, session: Session) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.Div(
                className="dropdown-container",
                children=[
                    html.H1(app.title),
                ],
            ),
            html.Hr(),
            dcc.Tabs(
                children=[
                    dcc.Tab(
                        label="Prices Graph",
                        children=[
                            html.Div(
                                className="app-div",
                                children=[
                                    html.Div(
                                        className="dropdown-container",
                                        children=[
                                            dam_date_picker.render(app, session),
                                            dam_countries_dropdown.render(app, session),
                                            dam_aggregation_dropdown.render(app),
                                        ],
                                    ),
                                    dam_prices_chart.render(app, session),
                                ],
                            )
                        ],
                    ),
                    dcc.Tab(
                        label="Tab2",
                        children=[
                            html.Div(
                                className="app-div",
                                children=[],
                            )
                        ],
                    ),
                    dcc.Tab(
                        label="Tab3",
                        children=[
                            html.Div(
                                className="app-div",
                                children=[],
                            )
                        ],
                    ),
                ]
            ),
        ],
    )

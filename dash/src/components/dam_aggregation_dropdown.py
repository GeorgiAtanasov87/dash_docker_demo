import i18n
from dash import Dash, dcc, html
from . import ids


def render(app: Dash) -> html.Div:
    return html.Div(
        children=[
            html.H6(i18n.t("general.aggregation")),
            dcc.Dropdown(
                id=ids.DAM_AGGREGATION_DROPDOWN,
                options=[
                    {"label": i18n.t("aggregation.hourly"), "value": "h"},
                    {"label": i18n.t("aggregation.daily"), "value": "d"},
                    {"label": i18n.t("aggregation.weekly"), "value": "w"},
                    {"label": i18n.t("aggregation.monthly"), "value": "m"},
                    {"label": i18n.t("aggregation.quarterly"), "value": "q"},
                    {"label": i18n.t("aggregation.yearly"), "value": "y"},
                ],
                value="d",
                placeholder=i18n.t("general.select"),
            ),
        ],
    )

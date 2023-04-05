import i18n
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

LOCALE = "en"
DAM_PATH = "./dam_data/data.db"


def main() -> None:
    # set the locale and load the translations
    i18n.set("locale", LOCALE)
    i18n.load_path.append("locale")

    # load dam data from sqlite db
    engine = create_engine(f"sqlite:///{DAM_PATH}")
    session = Session(engine)

    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = i18n.t("general.app_title")
    app.layout = create_layout(app, session)
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()

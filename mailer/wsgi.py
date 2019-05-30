import os

from mailer import create_app


app_config = os.environ.get("FLASK_ENV", "default")
app = create_app(app_config)

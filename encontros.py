from flask import render_template
from app import create_app
from flask_login import login_required
import logging


app = create_app("app.cfg")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
@login_required
def root(path):
    return render_template("index.html")


if __name__ == "__main__":
    if app.debug:
        # Make sure engine.echo is set to False
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

    app.run(debug=True)

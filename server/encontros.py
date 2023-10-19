from app import create_app
import logging


app = create_app()


if __name__ == "__main__":
    if app.debug:
        # Make sure engine.echo is set to False
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

    app.run(debug=True)

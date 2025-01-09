import os

import click
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        DATABASE=os.path.join(app.instance_path, "library.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        conf = app.config.from_pyfile("config.py", silent=True)
        if conf is True:
            click.echo("Config file loaded")
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    else:
        click.echo("Instance folder created")

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    from . import db, auth, book, member

    # initialize database
    db.init_db_command()

    # initialize app
    db.init_app(app)

    # register routes
    app.register_blueprint(auth.bp)
    app.register_blueprint(member.bp)
    app.register_blueprint(book.bp)
    return app

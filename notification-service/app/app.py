import os
from . import models as models
from flask import Flask
import traceback 

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    basedir = os.path.abspath(os.path.dirname(__file__))

    app.config.update(dict(
        SECRET_KEY="powerful secretkey",
        WTF_CSRF_SECRET_KEY="a csrf secret key",
        SQLALCHEMY_DATABASE_URI='postgresql://postgres:postgres@localhost/notification_db'
    ))

    models.init_app(app)
    models.create_tables(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response
        
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, Auction World!'


    from . import routes
    app.register_blueprint(routes.bp)

    return app

create_app()
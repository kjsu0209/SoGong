
from flask import Flask
from flask import render_template
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_url_path='/static')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

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

    # a simple page that says hello
    @app.route('/')
    def hello():
        return render_template('main.html')

    @app.route('/main', methods=('GET', 'POST'))
    def index():
        return render_template('main.html')

    from flaskr import db
    db.init_app(app)

    from flaskr import auth
    app.register_blueprint(auth.bp)
    
    from flaskr import user
    app.register_blueprint(user.bp)

    from flaskr import owner
    app.register_blueprint(owner.bp)

    from flaskr import parker
    app.register_blueprint(parker.bp)
    return app
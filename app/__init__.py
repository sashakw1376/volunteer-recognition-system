# Flask modules
from flask import Flask
from flask_migrate import Migrate


def create_app(debug: bool = False) -> Flask:
    # Initialize app
    app = Flask(__name__, template_folder='../templates', static_folder='../static', static_url_path='/')

    # Setup app configs
    app.config['DEBUG'] = debug
    app.config['SECRET_KEY'] = "YOUR-SECRET-KEY-HERE" # add something here?
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True



    # Initialize extensions
    from app.extensions import db, bcrypt, csrf, login_manager
    db.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    # Create database tables
    from app import models
    with app.app_context():
        db.create_all()

    # Register blueprints
    from app.routes import routes_bp
    app.register_blueprint(routes_bp)

    return app

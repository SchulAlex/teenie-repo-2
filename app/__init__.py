<<<<<<< HEAD
import os

from flask import Flask
from sqlalchemy import inspect, text
=======
from flask import Flask
>>>>>>> 2e30b332e272c2b4ba395f0b61e71434b00f2dfb
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from config import Config
from .models import db

migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

<<<<<<< HEAD
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    with app.app_context():
        db.create_all()
        _add_missing_image_columns()

    return app


def _add_missing_image_columns():
    """db.create_all() does not alter existing tables, so add the new
    image_filename column to databases created before the upload feature."""
    inspector = inspect(db.engine)
    for table in ('story', 'poll'):
        columns = [c['name'] for c in inspector.get_columns(table)]
        if 'image_filename' not in columns:
            with db.engine.begin() as conn:
                conn.execute(text(f'ALTER TABLE {table} ADD COLUMN image_filename VARCHAR(200)'))
=======
    with app.app_context():
        db.create_all()

    return app
>>>>>>> 2e30b332e272c2b4ba395f0b61e71434b00f2dfb

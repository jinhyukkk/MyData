# MyData/app/models/__init__.py
from flask_sqlalchemy import SQLAlchemy
import os
import importlib

db = SQLAlchemy()

def load_models(app):
    """애플리케이션과 함께 모델을 로드합니다."""
    models_dir = os.path.dirname(__file__)
    for filename in os.listdir(models_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f"app.models.{filename[:-3]}"
            importlib.import_module(module_name)

def init_app(app):
    """앱 초기화와 관련된 작업을 수행합니다."""
    db.init_app(app)
    load_models(app)

    basedir = os.path.abspath(os.path.dirname(__file__))
    if not os.path.exists(os.path.join(basedir, "instance", "MyData.db")):
        with app.app_context():
            db.create_all()

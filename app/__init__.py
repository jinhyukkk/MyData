from flask import Flask
from .models import db, init_app as init_models
from .views.publicStockView import public_stock_bp
from .views.myPortfolioView import my_portfolio_bp

def create_app(config_filename='config.py'):
    # Flask 애플리케이션 인스턴스 생성
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # 설정 로드
    app.config.from_pyfile(config_filename)
    # 데이터베이스 및 모델 초기화
    init_models(app)

    # 블루프린트 등록
    app.register_blueprint(public_stock_bp)
    app.register_blueprint(my_portfolio_bp)

    return app

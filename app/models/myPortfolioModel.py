# from app import db
from . import db  # .은 현재 모듈을 의미합니다.

class MyPortfolio(db.Model):
    idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nation = db.Column(db.String(20), nullable=False)
    stockName = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    averagePrice = db.Column(db.Numeric(10, 2), nullable=True)
    currentPrice = db.Column(db.Numeric(10, 2), nullable=True)
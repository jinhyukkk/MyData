# from app import db
from . import db  # .은 현재 모듈을 의미합니다.

class PublicStock(db.Model):
    idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stockName = db.Column(db.String(50), nullable=False)                # 종목명
    subDate = db.Column(db.Date, nullable=True)                         # 청약일
    refundDate = db.Column(db.Date, nullable=True)                      # 환불일
    openDate = db.Column(db.Date, nullable=True)                        # 상장일
    publicPrice = db.Column(db.Integer, nullable=True)                  # 공모가
    equalSubPrice = db.Column(db.Integer, nullable=True)                # 균등청약금액
    predictionRate = db.Column(db.String(20), nullable=True)            # 기관수요예측
    hostCompany = db.Column(db.String(50), nullable=True)               # 주관사
    commission = db.Column(db.String(50), nullable=True)                # 수수료
    quantity = db.Column(db.Integer, nullable=True)                     # 배정수량
    sellingPrice = db.Column(db.Integer, nullable=True)                 # 매도평단가
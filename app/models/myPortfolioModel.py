# from app import db
from . import db  # .은 현재 모듈을 의미합니다.
from sqlalchemy import Column, String, DECIMAL, Integer, Numeric, TIMESTAMP, UniqueConstraint
from sqlalchemy.sql import func

class MyPortfolio(db.Model):
    idx = Column(Integer, primary_key=True, autoincrement=True)
    nation = Column(String(20), nullable=False)
    stockName = Column(String(50), nullable=False)
    code = Column(String(20), nullable=False)
    quantity = Column(Integer, nullable=True)
    averagePrice = Column(Numeric(10, 2), nullable=True)
    currentPrice = Column(Numeric(10, 2), nullable=True)


class ExchangeRate(db.Model):
    __tablename__ = 'exchange_rates'

    idx = Column(Integer, primary_key=True, autoincrement=True)     # 인덱스
    baseCurrency = Column(String(3), nullable=False)               # 기준통화(예: USD)
    targetCurrency = Column(String(3), nullable=False)             # 대상통화(예: KRW)
    exchangeRate = Column(DECIMAL(16, 8), nullable=False)          # 기준 통화에서 대상 통화로의 환율
    lastUpdated = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())    # 업데이트된 시간

    __table_args__ = (UniqueConstraint('baseCurrency', 'targetCurrency', name='_currency_pair_uc'),)


class MyAccount(db.Model):
    __tablename__ = 'accounts'

    idx = Column(Integer, primary_key=True, autoincrement=True)     # 인덱스
    title = Column(String(30), nullable=False)                      # 계좌 제목
    currency = Column(String(3), nullable=False)                    # 계좌의 통화 (예: KRW)
    balance = Column(DECIMAL(16, 2), nullable=False)                # 계좌의 현재 잔액
    lastUpdated = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())    # 업데이트된 시간

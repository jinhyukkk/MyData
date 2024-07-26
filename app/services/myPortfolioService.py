from datetime import datetime

from flask import request, jsonify
from app import db
from app.models.myPortfolioModel import *
from app.common.helpers import *
from sqlalchemy import func, desc, literal_column, and_


def get_my_portfolio():
    # FROM
    queryResults = MyPortfolio.query

    # 국가별 조건
    nation = request.args.get('nation', '')
    exchangeRates = 1
    if nation:
        queryResults = queryResults.filter(MyPortfolio.nation == nation)
        currencyCode = country_to_currency.get(nation, '')
        exchangeRatesQuery = ExchangeRate.query.filter(
            and_(ExchangeRate.baseCurrency == 'KRW', ExchangeRate.targetCurrency == currencyCode)).limit(1).all()
        if exchangeRatesQuery:
            exchangeRates = exchangeRatesQuery[0].exchangeRate
        if nation == 'JP':
            exchangeRates /= 100

    # 정렬
    sort = request.args.get('sort', '')
    if sort:
        # MyPortfolio 모델의 유효한 속성인지 확인
        if hasattr(MyPortfolio, sort):
            if sort == 'stockName':
                queryResults = queryResults.order_by(getattr(MyPortfolio, sort).asc())
            else:
                queryResults = queryResults.order_by(getattr(MyPortfolio, sort).desc())

    # SELECT, ORDER BY
    queryResults = queryResults.with_entities(
        MyPortfolio.idx,
        MyPortfolio.stockName,
        MyPortfolio.nation,
        MyPortfolio.code,
        MyPortfolio.quantity,
        MyPortfolio.averagePrice,
        MyPortfolio.currentPrice,
        (MyPortfolio.quantity * MyPortfolio.averagePrice).label('purchaseAmount'),
        (MyPortfolio.quantity * MyPortfolio.currentPrice).label('valuationAmount'),
        ((MyPortfolio.quantity * MyPortfolio.currentPrice) - (MyPortfolio.quantity * MyPortfolio.averagePrice)).label('profitAndLoss'),
        ((MyPortfolio.currentPrice / MyPortfolio.averagePrice - 1) * 100).label('returnRatio'),
        ((MyPortfolio.quantity * MyPortfolio.currentPrice) / 100000000 * 100).label('evaluationRatio'),
    ).order_by(desc((MyPortfolio.quantity * MyPortfolio.currentPrice) / 100000000 * 100)).all()

    # 데이터 가공 및 포맷팅
    output = [
        {
            'idx': result.idx,
            'stockName': result.stockName,
            'nation': result.nation,
            'quantity': result.quantity,
            'averagePrice': format_currency_by_code(adjust_price(result.averagePrice, result.nation), result.nation),
            'currentPrice': format_currency_by_code(adjust_price(result.currentPrice, result.nation), result.nation),
            'purchaseAmount':
                format_currency_by_code(
                    adjust_price(
                        result.purchaseAmount * exchangeRates, 'KR'
                    ),
                    'KR'
                ),
            'valuationAmount':
                format_currency_by_code(
                    adjust_price(
                        result.valuationAmount * exchangeRates, 'KR'
                    ),
                    'KR'
                ),
            'profitAndLoss':
                format_currency_by_code(
                    adjust_price(
                        result.profitAndLoss * exchangeRates, 'KR'
                    ),
                    'KR'
                ),
            'returnRatio': format_percent(result.returnRatio),
            'evaluationRatio': format_percent(result.evaluationRatio)
        }
        for result in queryResults
    ]
    return output, nation


def add_my_portfolio():
    data = request.get_json()

    new_stock = MyPortfolio(
        nation=data['nation'],
        stockName=data['stockName'],
        code=data['code'],
        quantity=data['quantity'],
        averagePrice=data['averagePrice'].replace(",", ""),
        currentPrice=data['currentPrice'].replace(",", "")
    )
    db.session.add(new_stock)
    db.session.commit()
    return data['stockName']


def delete_my_portfolio():
    data = request.get_json()
    if 'idx' not in data:
        return jsonify({"message": "IDX not provided"}), 400

    idx_to_delete = int(data['idx'])
    try:
        # 레코드 찾기
        record = MyPortfolio.query.filter(MyPortfolio.idx == idx_to_delete).one_or_none()

        if record:
            # 레코드 삭제
            db.session.delete(record)
            db.session.commit()
            print(f"Record with ID {idx_to_delete} deleted successfully.")
        else:
            print(f"Record with ID {idx_to_delete} not found.")

    except Exception as e:
        # 오류 처리
        print(f"An error occurred: {e}")
        db.session.rollback()
    return "Deleted successfully"


def get_exchange_rates():
    exchange_rates = ExchangeRate.query.all()

    output = [
        {
            'idx': result.idx,
            'baseCurrency': result.baseCurrency,
            'targetCurrency': result.targetCurrency,
            'exchangeRate': format_currency_by_code(adjust_price(result.exchangeRate, 'US'), 'KR')
        }
        for result in exchange_rates
    ]

    return output

from flask import request, jsonify
from app import db
from app.models.myPortfolioModel import MyPortfolio
from app.common.helpers import format_currency_by_code, format_percent
from sqlalchemy import func, desc, literal_column


def get_my_portfolio():
    queryResults = MyPortfolio.query
    # 수익률 정렬
    # .order_by(
    #     desc((func.coalesce(MyPortfolio.currentPrice, 0) / func.coalesce(MyPortfolio.averagePrice, 1) - 1) * 100)))

    nation = request.args.get('nation', '')
    if nation:
        queryResults = queryResults.filter(MyPortfolio.nation == nation)

    sort = request.args.get('sort', '')
    if sort:
        # MyPortfolio 모델의 유효한 속성인지 확인
        if hasattr(MyPortfolio, sort):
            if sort == 'stockName':
                queryResults = queryResults.order_by(getattr(MyPortfolio, sort).asc())
            else:
                queryResults = queryResults.order_by(getattr(MyPortfolio, sort).desc())

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

    # 국가에 따른 포맷 변경 여부를 결정
    def adjust_price(value, nation):
        return int(value) if nation in ['KR', ''] else value

    # 데이터 가공 및 포맷팅
    output = [
        {
            'idx': result.idx,
            'stockName': result.stockName,
            'nation': result.nation,
            'quantity': result.quantity,
            'averagePrice': format_currency_by_code(adjust_price(result.averagePrice, result.nation), result.nation),
            'currentPrice': format_currency_by_code(adjust_price(result.currentPrice, result.nation), result.nation),
            'purchaseAmount': format_currency_by_code(adjust_price(result.purchaseAmount, result.nation), result.nation),
            'valuationAmount': format_currency_by_code(adjust_price(result.valuationAmount, result.nation), result.nation),
            'profitAndLoss': format_currency_by_code(adjust_price(result.profitAndLoss, result.nation), result.nation),
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
    data = request.get_json()
    if 'idx' not in data:
        return jsonify(
            {"message": "IDX not provided"}
        )

    idx_to_delete = int(data['idx'])
    return data
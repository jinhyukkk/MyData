from flask import request, jsonify
from app import db
from app.models.myPortfolioModel import MyPortfolio
from app.common.helpers import add_comma_pattern, format_currency_by_code, format_percent


def get_my_portfolio():
    searchText = request.args.get('searchText', '')
    searchPattern = "%%"
    if searchText:
        searchPattern = f"%{searchText}%"

    queryResults = (MyPortfolio
                    .query
                    .filter(MyPortfolio.stockName.like(searchPattern))
                    .order_by(MyPortfolio.nation.asc()))

    sort = request.args.get('sort', '')
    if sort:
        # MyPortfolio 모델의 유효한 속성인지 확인
        if hasattr(MyPortfolio, sort):
            if sort == 'stockName':
                queryResults = queryResults.order_by(getattr(MyPortfolio, sort).asc())
            else:
                queryResults = queryResults.order_by(getattr(MyPortfolio, sort).desc())

    queryResults = queryResults.all()

    output = []
    for result in queryResults:
        if result.nation == 'KR' or result.nation == '':
            result.averagePrice = int(result.averagePrice)
            result.currentPrice = int(result.currentPrice)
        result.purchaseAmount = result.quantity * result.averagePrice  # 매입금액
        result.valuationAmount = result.quantity * result.currentPrice  # 평가금액
        result.profitAndLoss = result.valuationAmount - result.purchaseAmount  # 평가손익
        result.returnRatio = (result.currentPrice / result.averagePrice - 1) * 100  # 수익률
        result.evaluationRatio = result.valuationAmount / 100000000 * 100  # 평가비중

        resultData = {
            'idx': result.idx,
            'stockName': result.stockName,
            'nation': result.nation,
            'quantity': result.quantity,
            'averagePrice': format_currency_by_code(result.averagePrice, result.nation),
            'currentPrice': format_currency_by_code(result.currentPrice, result.nation),
            'purchaseAmount': format_currency_by_code(result.purchaseAmount, result.nation),
            'valuationAmount': format_currency_by_code(result.valuationAmount, result.nation),
            'profitAndLoss': format_currency_by_code(result.profitAndLoss, result.nation),
            'returnRatio': format_percent(result.returnRatio),
            'evaluationRatio': format_percent(result.evaluationRatio)
        }
        output.append(resultData)
    return output


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
    ids_to_delete = data.get('ids', [])

    if not ids_to_delete:
        return jsonify({'message': 'No IDs provided'}), 400

    try:
        for place_id in ids_to_delete:
            place = MyPortfolio.query.get(place_id)
            if place:
                db.session.delete(place)
        db.session.commit()
        return jsonify({'message': 'Successfully deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

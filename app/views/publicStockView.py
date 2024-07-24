

from flask import Blueprint, render_template, jsonify
from app.services.publicStockService import get_public_stocks


# 블루프린트 정의
public_stock_bp = Blueprint('public_stock', __name__)


# 메인 페이지 라우팅
@public_stock_bp.route('/publicStock')
def publicStock():
    # data = get_public_stock_data()
    # return render_template('publicStock.html', data=data)
    return render_template('/publicStock.html')


@public_stock_bp.route('/api/publicStocks', methods=['GET'])
def get():
    try:
        result = get_public_stocks()
        return jsonify({'message': 'Success', 'result': result}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

#
# @public_stock_bp.route('/api/publicStocks', methods=['POST'])
# def post():
#     return addPublicStock()
#
#
# @public_stock_bp.route('/api/publicStocks', methods=['DELETE'])
# def delete():
#     return deletePublicStock()
#
#
# @public_stock_bp.route('/api/downloadExcel', methods=['GET'])
# def downloadExcel():
#     return downloadExcel()

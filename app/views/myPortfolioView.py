from flask import Blueprint, render_template, jsonify
from app.services.myPortfolioService import get_my_portfolio, add_my_portfolio


# 블루프린트 정의
my_portfolio_bp = Blueprint('my_portfolio', __name__)


# 메인 페이지 라우팅
@my_portfolio_bp.route('/')
def myPortfolio():
    return render_template('/myPortfolio.html')


@my_portfolio_bp.route('/api/myPortfolio', methods=['GET'])
def get():
    try:
        return jsonify({'message': 'Success', 'result': get_my_portfolio()}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@my_portfolio_bp.route('/api/myPortfolio', methods=['POST'])
def post():
    try:
        return jsonify({'message': 'Success', 'result': add_my_portfolio()}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
#
#
# @my_portfolio_bp.route('/api/myPortfolio', methods=['DELETE'])
# def delete():
#     return deletePublicStock()
#
#
# @my_portfolio_bp.route('/api/downloadExcel', methods=['GET'])
# def downloadExcel():
#     return downloadExcel()

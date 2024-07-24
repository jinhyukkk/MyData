import io
import re
import requests
import pandas as pd

from flask import request, jsonify, send_file
from app import db
from app.models.publicStockModel import PublicStock
from bs4 import BeautifulSoup
from datetime import datetime

# SSL 연결 설정 변경
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'


def add_public_stock():
    data = request.get_json()
    exists = PublicStock.query.filter_by(id=data['id']).first()
    if exists:
        return jsonify({'message': '이미 저장되어 있습니다.'})

    new_place = PublicStock(id=data['id'], placeName=data['placeName'], stars=data['stars'], reviews=data['reviews'])
    db.session.add(new_place)
    db.session.commit()
    return jsonify({'message': f"{data['placeName']} 저장 완료"})


def get_public_stock():
    searchText = request.args.get('searchText', '')
    searchPattern = "%%"
    if searchText:
        searchPattern = f"%{searchText}%"

    places = PublicStock.query.filter(PublicStock.placeName.like(searchPattern))

    sort = request.args.get('sort', '')
    if sort:
        # PublicStock 모델의 유효한 속성인지 확인
        if hasattr(PublicStock, sort):
            if sort == 'placeName':
                places = places.order_by(getattr(PublicStock, sort).asc())
            else:
                places = places.order_by(getattr(PublicStock, sort).desc())

    places = places.all()

    output = []
    for place in places:
        place_data = {
            'id': place.id,
            'placeName': place.placeName,
            'stars': place.stars,
            'reviews': place.reviews
        }
        output.append(place_data)
    return jsonify({'result': output})


def delete_public_stock():
    data = request.get_json()
    ids_to_delete = data.get('ids', [])

    if not ids_to_delete:
        return jsonify({'message': 'No IDs provided'}), 400

    try:
        for place_id in ids_to_delete:
            place = PublicStock.query.get(place_id)
            if place:
                db.session.delete(place)
        db.session.commit()
        return jsonify({'message': 'Successfully deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


def download_excel():
    searchText = request.args.get('searchText', '')
    searchPattern = "%"

    if searchText:
        searchPattern = f"%{searchText}%"

    places = PublicStock.query.filter(PublicStock.placeName.like(searchPattern))

    sort = request.args.get('sort', '')
    if sort:
        # PublicStock 모델의 유효한 속성인지 확인
        if hasattr(PublicStock, sort):
            if sort == 'placeName':
                places = places.order_by(getattr(PublicStock, sort).asc())
            else:
                places = places.order_by(getattr(PublicStock, sort).desc())

    places = places.all()

    data = []
    for place in places:
        data.append({
            '네이버플레이스 ID': place.id,
            '가게명': place.placeName,
            '별점': '-' if place.stars == '0' else place.stars,
            '리뷰수': '-' if place.reviews == '0' else place.reviews
        })

    df = pd.DataFrame(data)

    # Save the DataFrame to a BytesIO object
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='PublicStocks')
    output.seek(0)

    # Send the file to the client
    return send_file(output, download_name="PublicStockList.xlsx", as_attachment=True)


def get_public_stocks():
    urlList = get_url()
    result = []
    for url in urlList:
        gongmoList = get_detail(url)
        # 현재 날짜 가져오기
        currentDate = datetime.now()

        # 주어진 형식의 날짜 문자열을 날짜 객체로 변환
        dateStr = gongmoList['refundDate'].replace(" ", "")
        givenDate = datetime.strptime(dateStr, "%Y.%m.%d")
        if givenDate < currentDate:
            break
        result.append(gongmoList)
    return result


# URL 조회
def get_url():
    global urlList
    url = "https://www.38.co.kr/html/fund/?o=k"

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 모든 테이블 선택
        tables = soup.find_all('table')

        # "summary" 속성이 "공모주"인 테이블 선택
        for table in tables:
            summaryAttr = table.get('summary')
            if summaryAttr and '공모주 청약일정' in summaryAttr:
                # 테이블 내의 모든 <tr> 태그 선택
                rows = table.find_all('tr')
                # print(rows)
                urlList = []
                # 각 <tr> 요소에서 첫 번째 <a> 태그 선택
                for row in rows:
                    firstLink = row.find('a')

                    if firstLink:
                        tds = row.find_all('td')

                        gongmoDate = tds[1]
                        gongmoSplit = gongmoDate.text.strip().split('~')
                        gongmoYear = gongmoSplit[0].split('.')[0]
                        gongmoRndDate = gongmoYear + '.' + gongmoSplit[1]
                        gongmoRndDate = datetime.strptime(gongmoRndDate, "%Y.%m.%d")
                        # 현재 날짜 가져오기
                        currentDate = datetime.now()
                        if gongmoRndDate < currentDate:
                            break

                        name = firstLink.text
                        targetUrl = firstLink.get('href')
                        urlList.insert(0, targetUrl)
                        print(f"링크 URL: {targetUrl}, 텍스트: {name}")
                    else:
                        print("첫 번째 <a> 태그가 없습니다.")

        return urlList

    except Exception as e:
        print("대기 동안 오류 발생:", e)


# 상세 조회
def get_detail(url):
    # 기업개요  companyName
    # 공모정보  wishPrice, jugansa
    # 청약일정  subDate, refundDate, openDate, publicPrice, predictionRate
    global companyName, subDate, refundDate, openDate, publicPrice, predictionRate, wishPrice, jugansa

    response = requests.get('https://www.38.co.kr' + url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 모든 테이블 선택
    tables = soup.find_all('table')
    companyName, subDate, refundDate, openDate, publicPrice, predictionRate, wishPrice, jugansa = '', '', '', '', '', '', '', ''

    # "summary" 속성으로 테이블 선택
    for table in tables:
        summaryAttr = table.get('summary')
        if summaryAttr:
            tdTags = table.find_all('td')
            if summaryAttr == '기업개요':
                # 각 <td> 태그에 대해 처리
                for i in range(len(tdTags) - 1):
                    if tdTags[i].text.strip() == '종목명':
                        companyName = tdTags[i + 1].text.strip()
                print(companyName)
            elif summaryAttr == '공모정보':
                # 각 <td> 태그에 대해 처리
                for i in range(len(tdTags) - 1):
                    if tdTags[i].text.strip() == '희망공모가액':
                        wishPrice = tdTags[i + 1].text.strip()
                    elif tdTags[i].text.strip() == '주간사':
                        jugansa = tdTags[i + 1].text.strip()
            elif summaryAttr == '공모청약일정':
                # 각 <td> 태그에 대해 처리
                for i in range(len(tdTags) - 1):
                    if tdTags[i].text.strip() == '공모청약일':
                        dates = tdTags[i + 1].text.strip().split()
                        # 첫 번째 날짜 추출
                        subDate = dates[0]
                        if subDate:
                            subDate = change_date_format(subDate)
                    elif tdTags[i].text.strip() == '환불일':
                        refundDate = tdTags[i + 1].text.strip()
                        if refundDate:
                            refundDate = change_date_format(refundDate)
                    elif tdTags[i].text.strip() == '상장일':
                        openDate = tdTags[i + 1].text.strip()
                        if openDate:
                            openDate = change_date_format(openDate)
                    elif tdTags[i].text.strip() == '확정공모가':
                        publicPrice = tdTags[i + 1].text.strip()
                        numbers = re.findall(r'\d+', publicPrice)
                        publicPrice = ''.join(numbers)
                        if publicPrice == '':
                            wishPriceSplit = wishPrice.strip().split('~')
                            wishPrice = re.findall(r'\d+', wishPriceSplit[1])
                            publicPrice = ''.join(wishPrice)
                    elif tdTags[i].text.strip() == '기관경쟁률':
                        predictionRate = tdTags[i + 1].text.strip()

    return {'companyName': companyName, 'subDate': subDate, 'refundDate': refundDate, 'openDate': openDate,
            'publicPrice': publicPrice, 'predictionRate': predictionRate, 'jugansa': jugansa}


def change_date_format(date):
    return datetime.strptime(date, "%Y.%m.%d").strftime("%Y. %m. %d")


def find_data(table, findName):
    tdTags = table.find_all('td')

    isNextTd = False  # 플래그 변수
    resultData = ""  # 정보를 저장할 변수
    # 각 <td> 태그에 대해 처리
    for tdTag in tdTags:
        if isNextTd:
            # 정보 획득
            resultData = tdTag.text.strip()
            isNextTd = False

        if tdTag.text.strip() == findName:
            # 다음 <td> 태그에 있는 정보를 획득하기 위해 플래그 설정
            isNextTd = True
    return resultData

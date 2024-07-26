country_to_currency = {
    "KR": "KRW",  # South Korea
    "US": "USD",  # United States
    "JP": "JPY",  # Japan
    "GB": "GBP",  # United Kingdom
    "CN": "CNY",  # China
    "AU": "AUD",  # Australia
    "CA": "CAD",  # Canada
    "CH": "CHF",  # Switzerland
    "IN": "INR"   # India
}

currency_symbols = {
    "USD": "$",
    "EUR": "€",
    "JPY": "¥",
    "GBP": "£",
    "KRW": "₩",
    "CNY": "¥",
    "AUD": "$",
    "CAD": "$",
    "CHF": "CHF",
    "INR": "₹"
}

def format_percent(number):
    return f"{number:,.2f}%"


def format_currency_by_code(number, countryCode):
    """
    통화 코드에 따라 숫자를 포맷팅하는 함수

    :param number: 포맷팅할 숫자
    :param currency_code: 통화 코드 (예: 'USD', 'EUR', 'JPY')
    :return: 포맷팅된 통화 문자열
    """
    # 국가 코드로 통화 코드를 가져온다
    currencyCode = country_to_currency.get(countryCode, '')

    # 통화 코드로 통화 기호를 가져온다
    symbol = currency_symbols.get(currencyCode, '')

    # 숫자를 포맷팅한다
    formattedNumber = add_comma_pattern(number, currencyCode)

    # 통화 기호와 포맷팅된 숫자를 결합하여 반환한다
    return f"{symbol}{formattedNumber}"


def add_comma_pattern(number, currencyCode):
    """Format number with commas for thousands."""
    if currencyCode == 'KRW':
        return '{:,}'.format(number)
    else:
        return f"{number:,.2f}"

# 국가에 따른 포맷 변경 여부를 결정
def adjust_price(value, nation):
    return int(value) if nation in ['KR', ''] else value

def model_to_dict(instance):
    """모델 인스턴스를 딕셔너리로 변환하는 헬퍼 함수."""
    if instance is None:
        return {}
    return {
        column.name: getattr(instance, column.name)
        for column in instance.__table__.columns
    }
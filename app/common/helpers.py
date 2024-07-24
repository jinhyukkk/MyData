currency_symbols = {
    "KR": "₩",  # South Korea
    "US": "$",  # United States
    "JP": "¥",  # Japan
    "GB": "£",  # United Kingdom
    "CN": "¥",  # China
    "AU": "$",  # Australia
    "CA": "$",  # Canada
    "CH": "CHF",  # Switzerland
    "IN": "₹"  # India
}


def format_percent(number):
    return f"{number:,.2f}%"


def format_currency_by_code(number, currency_code):
    """
    통화 코드에 따라 숫자를 포맷팅하는 함수

    :param number: 포맷팅할 숫자
    :param currency_code: 통화 코드 (예: 'USD', 'EUR', 'JPY')
    :return: 포맷팅된 통화 문자열
    """
    # 통화 기호를 가져온다
    symbol = currency_symbols.get(currency_code, '')

    # 숫자를 포맷팅한다
    formatted_number = add_comma_pattern(number, currency_code)

    # 통화 기호와 포맷팅된 숫자를 결합하여 반환한다
    return f"{symbol}{formatted_number}"


def add_comma_pattern(number, currency_code):
    """Format number with commas for thousands."""
    if currency_code == 'KR':
        return '{:,}'.format(number)
    else:
        return f"{number:,.2f}"

# MyData

## 필요한 라이브러리 설치

    pip install Flask selenium webdriver_manager beautifulsoup4 Flask SQLAlchemy pandas openpyxl urllib3
   


## 실행 방법

1. 터미널을 열고 naverPlaceApp.py가 있는 디렉토리로 이동합니다.
2. 다음 명령어를 입력하여 Flask 서버를 실행합니다.
    `````
    python naverPlaceApp.py
4. 브라우저를 열고 http://127.0.0.1:5000/ 에 접속합니다.

## 구조

```
MyData/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── publicCrawlModel.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── publicCrawlView.py
│   └── services/
│       ├── __init__.py
│       └── publicCrawlService.py
│
├── instance/
│   └── test.db
│
├── static/
│   ├── css/
│   │   ├── reset.css
│   │   └── style.css
│   ├── js/
│   │   ├── main.js
│   └── images/
│       └── search_icon.svg
│
├── templates/
│   ├── main.html
│   ├── keyworsToolList.html
│   └── savedList.html
│
└── run.py
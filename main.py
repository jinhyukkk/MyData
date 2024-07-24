import os
from app import create_app

app = create_app()

def openBrowser():
    import webbrowser
    import time
    time.sleep(1)  # 서버가 시작되기를 기다리기 위해 잠시 대기
    webbrowser.open('http://127.0.0.1:5000/')

app = create_app()
if __name__ == '__main__':
    # if os.path.exists('instance/test.db'):
    #     os.remove('instance/test.db')
    # threading.Thread(target=openBrowser).start()
    app.run(debug=True)

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run():
    os.chdir(DIRECTORY)
    url = f"http://localhost:{PORT}/index.html"
    print("=" * 60)
    print("🎯 ADsP D-4 초단기 완성 마스터 웹앱 서버 시작")
    print(f"👉 로컬 웹서버 접속 주소: {url}")
    print("👉 필기본 PDF 파일: ADsP_D4_따라쓰기_필기본_워크북.pdf")
    print("=" * 60)
    
    # 웹 브라우저 자동 오픈
    webbrowser.open(url)
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"서버가 포트 {PORT}에서 정상 실행 중입니다. 종료하려면 Ctrl+C를 누르세요.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n서버를 종료합니다.")
            sys.exit(0)

if __name__ == "__main__":
    run()

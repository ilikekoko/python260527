# 선택한 블럭 주석 처리 : ctrl + /

	# <span class="category fixed" title="판매">판매</span>
	# 					<span class="subject_fixed" data-role="list-title-text" title="나이키 에어맥스DN 러닝화 265~270 방수 운동화">
	# 						나이키 에어맥스DN 러닝화 265~270 방수 운동화


# beautifulsoup4 라이브러리를 이용하여 웹 페이지의 요소를 선택하는 방법을 설명하는 코드입니다.
from bs4 import BeautifulSoup
# url 라이브러리를 이용하여 웹 페이지의 요소를 선택하는 방법을 설명하는 코드입니다.
import urllib.request
# re 추가
import re

# url https://www.clien.net/service/board/sold 변수처리
url = "https://www.clien.net/service/board/sold"
# url 열고 내용 읽어서 data 변수에 담기 헤더를 추가하여 웹 페이지를 열 때 브라우저에서 접속하는 것처럼 보이도록 설정하기
headers = {"User-Agent": "Mozilla/5.0"}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as response:
    data = response.read().decode("utf-8")

# data를 html.parser로 분석하기
soup = BeautifulSoup(data, "html.parser")
# 필터링 작업 수행 span 태그 중에서 class 속성이 data-role="list-title-text" 인 태그 검색
span_tags = soup.find_all("span", attrs={"data-role": "list-title-text"})
# 검색된 span 태그에서 텍스트만 추출하여 출력하기
for span in span_tags:
    # 정규표현식으로 텍스트에서 특수문자 제거하기
    text = re.sub(r'[^\w\s]', '', span.get_text(strip=True))
    print(text)


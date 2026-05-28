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


# 파일에 저장위해 파일열기 (write text) 인코딩추가하기  
file = open("output.txt", "w", encoding="utf-8")

# 반복 1 부터 10 까지 수행하기
for i in range(1,11):
    # url 변수에 저장하기
# url https://www.clien.net/service/board/sold?&od=T31&category=0&po= + i 값 추가변수처리  
    url = "https://www.todayhumor.co.kr/board/list.php?kind=total&table=total&page=" + str(i)
    # url 열고 내용 읽어서 data 변수에 담기 헤더를 추가하여 웹 페이지를 열 때 브라우저에서 접속하는 것처럼 보이도록 설정하기
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        data = response.read().decode("utf-8")

    # data를 html.parser로 분석하기
    soup = BeautifulSoup(data, "html.parser")
    # 필터링 작업 수행 td 태그 중에서 class="subject" 인 태그 검색하기 
    td_tags = soup.find_all("td", class_="subject")
    for td in td_tags:
        # td 태그 안에 있는 a 태그 검색하기
        atag = td.find("a")
        # 정규표현식으로 텍스트에서 특수문자 제거하기
        text = re.sub(r'[^\w\s]', '', atag.get_text(strip=True))
        # re를 사용하여 문자열 검색 (정규표현식으로 단백질 글자가 포함된 텍스트만 출력하기) 

        if re.search(r'단백질', text):
            print(text)
            # 파일에 저장하기
            file.write(text + "\n")

# 파일 닫기
file.close()





# beautifulsoup4 라이브러리를 이용하여 웹 페이지의 요소를 선택하는 방법을 설명하는 코드입니다.
from bs4 import BeautifulSoup
# 연습용 웹페이지 로딩하기 위해 page 변수에 담기
page = open("./crowl/Chap09_test.html", "rt", encoding="utf-8").read()

# 검색용 객체 생성
soup = BeautifulSoup(page, "html.parser")
# 전체페이지를 이쁘게 표시
# print(soup.prettify())

# p 태그 모두 검색
# p_tags = soup.find_all("p")
# for p in p_tags:
#    print(p)

# p 태그 중에서 class="outer-text"인 태그 검색
# p_outer_text = soup.find_all("p", class_="outer-text")
# for p in p_outer_text:
#     print(p)

# attr 속성으로 검색하기
# p 태그 중에서 class 속성이 outer-text인 태그 검색 
# print(soup.find_all("p", attrs={"class": "outer-text"}))

# p 태그를 문자열처리해줘 strip 사용해서
p_tags = soup.find_all("p")
for p in p_tags:
  print(p.get_text(strip=True))        

  
# web02.py
from bs4 import BeautifulSoup
doc = ['<html><head><title>Page title</title></head>', \
    '<body><p id="firstpara" align="center">This is paragraph <b>one</b></p>', \
    '<p id="secondpara" align="blah">This is a paragraph <b>two</b></p>', '</html>']

#soup = BeautifulSoup(''.join(doc), 'html.parser')
#태그를 정렬해서 보여주기
#print(soup.prettify())

#문자열 패턴을 손쉽게 정의할 수 있는 정규표현식 패턴을
#사용할 수 있는 re
import re
#tagsStartingWithB = soup.findAll(re.compile('^b'))
#print([tag.name for tag in tagsStartingWithB])

#리스트로 태그를 나열하면 해당 태그들을 검색합니다. 
#print(soup.find_all(['title', 'p']))

#람다함수를 정의해서 태그의 속성들이 2개인 경우만 검색합니다. 
#print(soup.find_all(lambda tag:len(tag.attrs) == 2))

#태그중에 align속성이 "center"인 경우만 검색합니다. 
#print(soup.find_all(align="center"))

#태그의 id속성이 para로 끝나는 경우만 검색합니다. 
#print(soup.find_all(id=re.compile("para$")))

#다시 간단한 HTML소스를 생성해서 class속성을 통해 검색합니다. 
soup =BeautifulSoup("""
    Bob's<b>Bold</b>Barbeque Sauce now available 
    <b class="hickory">Hickory</b> and <b class="lime">Lime</a>
    """, "html.parser")

#<b>태그 중에 class=lime이라고 되어 있는 태그를 검색합니다. 
print(soup.find("b", {"class":"lime"}))

#<b>태그 중에 class=hickory이라고 되어 있는 태그를 검색합니다. 
#print(soup.find("b", {"class":"hickory"}))


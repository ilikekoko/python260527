import requests
from bs4 import BeautifulSoup
import time
import urllib.parse

def naver_news_crawler(keyword, num_pages=1):
    """
    네이버 뉴스 검색결과를 크롤링합니다.
    
    Args:
        keyword (str): 검색할 키워드
        num_pages (int): 크롤링할 페이지 수 (기본값 1)
    """
    # 네이버는 크롤링 차단을 방지하기 위해 User-Agent 설정이 필수적입니다.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    results = []
    
    # 키워드를 URL 인코딩합니다.
    encoded_keyword = urllib.parse.quote(keyword)
    
    for page in range(1, num_pages + 1):
        # 시작 위치 계산 (페이지당 10개씩 노출되므로 1, 11, 21...)
        start = (page - 1) * 10 + 1
        url = f"https://search.naver.com/search.naver?where=news&query={encoded_keyword}&start={start}"
        
        try:
            print(f"[{page}페이지] 크롤링 중: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"오류: HTTP 상태 코드 {response.status_code}")
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 뉴스 목록을 감싸는 컨테이너를 찾습니다.
            list_container = soup.find('div', class_=lambda c: c and 'fds-news-item-list' in c)
            if not list_container:
                print("뉴스 목록 컨테이너를 찾을 수 없습니다. (구조 변경 가능성 있음)")
                break
                
            # 컨테이너 안에서 헤드라인(type-headline1) 스팬들을 모두 찾습니다.
            headline_spans = list_container.find_all('span', class_=lambda c: c and 'type-headline1' in c)
            
            if not headline_spans:
                print("검색 결과가 없거나 뉴스 기사를 찾을 수 없습니다.")
                break
                
            for idx, hl_span in enumerate(headline_spans, 1):
                # 각 기사 카드는 list_container의 직계 자식입니다.
                # 헤드라인 스팬에서 위로 거슬러 올라가 직계 자식 요소를 찾습니다.
                card = hl_span
                while card and card.parent != list_container:
                    card = card.parent
                
                if not card:
                    continue
                
                # 1. 제목 및 언론사 원문 링크 추출
                title = hl_span.get_text(strip=True)
                a_tag = hl_span.find_parent('a')
                article_url = a_tag.get('href', '') if a_tag else 'N/A'
                
                # 2. 언론사(출처) 추출
                press_span = card.find('span', class_=lambda c: c and 'profile-info-title-text' in c)
                press = press_span.get_text(strip=True) if press_span else 'N/A'
                
                # 3. 요약 설명(본문 일부) 추출
                desc_span = card.find('span', class_=lambda c: c and 'type-body1' in c)
                desc = desc_span.get_text(strip=True) if desc_span else 'N/A'
                
                # 4. 작성 시간/날짜 추출 (네이버 뉴스 전용 subtext 제외)
                subtext_spans = card.find_all('span', class_=lambda c: c and 'profile-info-subtext' in c)
                date = 'N/A'
                for span in subtext_spans:
                    text = span.get_text(strip=True)
                    if text and "네이버뉴스" not in text and "면" not in text:
                        date = text
                        break
                
                # 5. 네이버뉴스 내 링크 추출 (제공되는 경우에만)
                naver_news_a = card.find('a', href=lambda h: h and 'n.news.naver.com' in h)
                naver_news_url = naver_news_a.get('href', '') if naver_news_a else 'N/A'
                
                item = {
                    '번호': (page - 1) * 10 + idx,
                    '언론사': press,
                    '제목': title,
                    '링크': article_url,
                    '등록시간': date,
                    '요약': desc,
                    '네이버뉴스링크': naver_news_url
                }
                results.append(item)
                print(f"  {idx}. [{press}] {title}")
                
            # 다음 페이지 크롤링 전 매너 대기 (2초)
            if page < num_pages:
                time.sleep(2)
                
        except requests.exceptions.RequestException as e:
            print(f"요청 중 오류 발생: {e}")
            continue
            
    return results

def print_results(results):
    """크롤링 결과를 보기 좋게 포맷팅하여 출력합니다."""
    print("\n" + "="*80)
    print("                      ★ 크롤링 결과 출력 ★")
    print("="*80)
    
    for item in results:
        print(f"[{item['번호']}] {item['제목']}")
        print(f"  - 언론사  : {item['언론사']}")
        print(f"  - 등록시간: {item['등록시간']}")
        print(f"  - 기사링크: {item['링크']}")
        if item['네이버뉴스링크'] != 'N/A':
            print(f"  - 네이버뉴스링크: {item['네이버뉴스링크']}")
        print(f"  - 요약    : {item['요약']}")
        print("-" * 80)

if __name__ == "__main__":
    print("==================================================")
    print("              Naver 뉴스 크롤러 프로그램           ")
    print("==================================================")
    
    keyword = input("검색할 키워드를 입력하세요 (예: 반도체): ").strip()
    if not keyword:
        keyword = "반도체"
        print(f"입력값이 없어 기본 키워드 '{keyword}'로 진행합니다.")
        
    try:
        pages_input = input("크롤링할 페이지 수를 입력하세요 (기본값: 1): ").strip()
        num_pages = int(pages_input) if pages_input else 1
    except ValueError:
        num_pages = 1
        print("올바른 숫자가 아닙니다. 기본값인 1페이지로 진행합니다.")
        
    print(f"\n'{keyword}' 키워드로 {num_pages}페이지 크롤링을 시작합니다...\n")
    
    start_time = time.time()
    news_results = naver_news_crawler(keyword, num_pages)
    end_time = time.time()
    
    if news_results:
        print_results(news_results)
        print(f"\n성공적으로 완료되었습니다! (총 {len(news_results)}개 뉴스 크롤링 완료)")
        print(f"소요 시간: {end_time - start_time:.2f}초")
    else:
        print("\n크롤링된 결과가 없습니다. 키워드나 인터넷 연결 상태를 확인해주세요.")

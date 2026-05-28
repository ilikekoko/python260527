# -*- coding: utf-8 -*-
"""
네이버 통합검색(nexearch) 결과 페이지에서 뉴스 제목만 크롤링합니다.

사용 라이브러리: requests, beautifulsoup4
설치: pip install requests beautifulsoup4
"""

import sys
import requests
from bs4 import BeautifulSoup
import urllib.parse

# Windows 콘솔 한글 깨짐 방지
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def crawl_naver_news_titles(query: str) -> list:
    """
    네이버 통합검색 결과 페이지의 뉴스 섹션에서 제목 목록을 반환합니다.

    Args:
        query (str): 검색 키워드 (예: "반도체")

    Returns:
        list[str]: 뉴스 제목 리스트
    """
    encoded_query = urllib.parse.quote(query)
    url = (
        "https://search.naver.com/search.naver"
        f"?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query={encoded_query}"
    )

    headers = {
        # 브라우저처럼 보이도록 User-Agent 설정 (없으면 차단될 수 있음)
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ko-KR,ko;q=0.9",
        "Referer": "https://www.naver.com/",
    }

    print(f"[*] 요청 URL: {url}\n")

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()   # HTTP 오류 시 예외 발생
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    titles = []

    # -----------------------------------------------------------------------
    # 전략 1: 네이버 통합검색의 뉴스 카드 헤드라인 스팬 (class에 'type-headline' 포함)
    # -----------------------------------------------------------------------
    headline_spans = soup.find_all(
        "span",
        class_=lambda c: c and "type-headline" in c
    )
    if headline_spans:
        for span in headline_spans:
            text = span.get_text(strip=True)
            if text:
                titles.append(text)
        print(f"[전략 1] 헤드라인 스팬으로 {len(titles)}개 제목 추출 성공\n")
        return titles

    # -----------------------------------------------------------------------
    # 전략 2: 뉴스 관련 <a> 태그의 title 속성 (class에 'news_tit' 포함)
    # -----------------------------------------------------------------------
    news_tit_tags = soup.find_all("a", class_=lambda c: c and "news_tit" in c)
    if news_tit_tags:
        for a in news_tit_tags:
            text = a.get("title") or a.get_text(strip=True)
            if text:
                titles.append(text)
        print(f"[전략 2] news_tit 태그로 {len(titles)}개 제목 추출 성공\n")
        return titles

    # -----------------------------------------------------------------------
    # 전략 3: 뉴스 섹션 내부의 모든 <a> 태그 텍스트 (fallback)
    # -----------------------------------------------------------------------
    news_section = soup.find(
        "section", class_=lambda c: c and "news" in c.lower()
    ) or soup.find(
        "div", class_=lambda c: c and ("news" in c.lower() or "fds-news" in c)
    )
    if news_section:
        for a in news_section.find_all("a", href=True):
            text = a.get_text(strip=True)
            if text and len(text) > 10:  # 짧은 버튼 텍스트 제외
                titles.append(text)
        print(f"[전략 3] 뉴스 섹션 <a> 태그로 {len(titles)}개 제목 추출\n")
        return titles

    print("[!] 뉴스 제목을 찾지 못했습니다. 페이지 구조가 변경되었거나 차단되었을 수 있습니다.")
    return titles


def save_to_file(titles: list, query: str, filename: str = None):
    """결과를 텍스트 파일로 저장합니다."""
    if filename is None:
        safe_query = query.replace(" ", "_")
        filename = f"naver_news_{safe_query}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"[네이버 통합검색] '{query}' 뉴스 제목 목록\n")
        f.write("=" * 60 + "\n")
        for i, title in enumerate(titles, start=1):
            f.write(f"{i:>2}. {title}\n")
        f.write("=" * 60 + "\n")
        f.write(f"총 {len(titles)}개\n")

    print(f"[저장 완료] '{filename}' 파일에 저장되었습니다.")
    return filename


def main():
    print("=" * 60)
    print("   네이버 통합검색 뉴스 제목 크롤러")
    print("=" * 60)

    # 키워드를 직접 지정하거나 입력받으려면 아래 주석 해제
    # query = input("검색 키워드를 입력하세요 (기본값: 반도체): ").strip() or "반도체"

    query = "반도체"   # ← 여기서 검색어를 바꾸세요
    print(f"  검색 키워드: {query}\n")

    try:
        titles = crawl_naver_news_titles(query)
    except requests.exceptions.HTTPError as e:
        print(f"[HTTP 오류] {e}")
        return
    except requests.exceptions.RequestException as e:
        print(f"[네트워크 오류] {e}")
        return

    if not titles:
        print("크롤링된 뉴스 제목이 없습니다.")
        return

    # 콘솔 출력
    print("=" * 60)
    print(f"  총 {len(titles)}개의 뉴스 제목")
    print("=" * 60)
    for i, title in enumerate(titles, start=1):
        print(f"  {i:>2}. {title}")
    print("=" * 60)

    # 파일 저장 (한글 깨짐 없이 utf-8로 저장)
    save_to_file(titles, query)


if __name__ == "__main__":
    main()

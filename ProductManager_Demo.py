"""
SQLite 전자제품 데이터베이스 사용 예제
ProductManager 클래스의 다양한 메서드 활용법
"""

from ProductManager import ProductManager


def demo_basic_operations():
    """기본 CRUD 작업 예제"""
    print("\n" + "="*60)
    print("[예제 1] 기본 CRUD 작업")
    print("="*60)
    
    manager = ProductManager('MyProduct.db')
    
    # 1. INSERT - 단일 데이터 추가
    print("\n▶ INSERT 작업: 새로운 제품 추가")
    print("-" * 60)
    products_to_add = [
        ("애플 MacBook Pro M3", 3500000),
        ("ASUS ROG 게이밍노트북", 3200000),
        ("LG OLED 55인치 TV", 2800000),
    ]
    
    added_ids = []
    for name, price in products_to_add:
        product_id = manager.insert(name, price)
        if product_id:
            added_ids.append(product_id)
            print(f"  ✓ 추가됨: {name} (₩{price:,}) - ID: {product_id}")
    
    # 2. SELECT - 다양한 조회
    print("\n▶ SELECT 작업: 데이터 조회")
    print("-" * 60)
    
    # ID로 조회
    print(f"  ID {added_ids[0]}로 조회:")
    product = manager.select_by_id(added_ids[0])
    if product:
        print(f"    {product[1]} - ₩{product[2]:,}")
    
    # 이름으로 부분 검색
    print(f"\n  '노트북' 검색 결과:")
    results = manager.select_by_name("노트북")
    print(f"    총 {len(results)}개 제품 발견")
    for i, prod in enumerate(results[:3], 1):
        print(f"    {i}. {prod[1]} - ₩{prod[2]:,}")
    
    # 3. UPDATE - 데이터 수정
    print("\n▶ UPDATE 작업: 제품 정보 수정")
    print("-" * 60)
    print(f"  ID {added_ids[0]} 제품 가격 변경")
    old_product = manager.select_by_id(added_ids[0])
    if manager.update(added_ids[0], product_price=3800000):
        new_product = manager.select_by_id(added_ids[0])
        print(f"    변경 전: ₩{old_product[2]:,}")
        print(f"    변경 후: ₩{new_product[2]:,}")
    
    # 4. DELETE - 데이터 삭제
    print("\n▶ DELETE 작업: 제품 삭제")
    print("-" * 60)
    print(f"  ID {added_ids[-1]} 제품 삭제")
    if manager.delete(added_ids[-1]):
        print(f"    ✓ 삭제 완료")
    
    manager.close()


def demo_search_operations():
    """다양한 검색 작업 예제"""
    print("\n" + "="*60)
    print("[예제 2] 다양한 검색 작업")
    print("="*60)
    
    manager = ProductManager('MyProduct.db')
    
    # 1. 가격대별 검색
    print("\n▶ 가격대별 검색 (₩500,000 ~ ₩1,000,000)")
    print("-" * 60)
    products = manager.select_by_price_range(500000, 1000000)
    print(f"  검색 결과: {len(products)}개 제품")
    for i, prod in enumerate(products[:5], 1):
        print(f"  {i}. {prod[1]} - ₩{prod[2]:,}")
    if len(products) > 5:
        print(f"  ... 외 {len(products)-5}개")
    
    # 2. 제품명 부분 검색
    print("\n▶ 제품명 부분 검색 ('삼성' 검색)")
    print("-" * 60)
    samsung_products = manager.select_by_name("삼성")
    print(f"  검색 결과: {len(samsung_products)}개 제품")
    for i, prod in enumerate(samsung_products[:5], 1):
        print(f"  {i}. {prod[1]} - ₩{prod[2]:,}")
    if len(samsung_products) > 5:
        print(f"  ... 외 {len(samsung_products)-5}개")
    
    # 3. 가격 범위별 검색 - 고가제품
    print("\n▶ 고가 제품 검색 (₩4,000,000 이상)")
    print("-" * 60)
    expensive = manager.select_by_price_range(4000000, 10000000)
    print(f"  검색 결과: {len(expensive)}개 제품")
    for i, prod in enumerate(expensive[:5], 1):
        print(f"  {i}. {prod[1]} - ₩{prod[2]:,}")
    if len(expensive) > 5:
        print(f"  ... 외 {len(expensive)-5}개")
    
    manager.close()


def demo_statistics():
    """통계 조회 예제"""
    print("\n" + "="*60)
    print("[예제 3] 데이터베이스 통계")
    print("="*60)
    
    manager = ProductManager('MyProduct.db')
    
    stats = manager.get_statistics()
    if stats:
        print(f"\n  총 제품 개수: {stats['count']:,}개")
        print(f"  평균 가격: ₩{stats['average_price']:,.0f}")
        print(f"  최저 가격: ₩{stats['min_price']:,}")
        print(f"  최고 가격: ₩{stats['max_price']:,}")
        print(f"  가격 범위: ₩{stats['max_price'] - stats['min_price']:,}")
    
    manager.close()


def demo_batch_operations():
    """대량 데이터 작업 예제"""
    print("\n" + "="*60)
    print("[예제 4] 대량 데이터 작업")
    print("="*60)
    
    manager = ProductManager('MyProduct.db')
    
    # 추가 샘플 데이터 생성
    print("\n▶ 대량 데이터 추가")
    print("-" * 60)
    import random
    
    new_products = [
        ("소니 WH-1000XM5 이어폰", 450000),
        ("로지텍 MX Master 3 마우스", 120000),
        ("코르세어 K95 기계식 키보드", 350000),
        ("ASUS PA248QV 전문가용 모니터", 800000),
        ("캐논 EOS R6 카메라", 3500000),
    ]
    
    before_count = manager.get_count()
    manager.insert_many(new_products)
    after_count = manager.get_count()
    
    print(f"  추가 전: {before_count:,}개")
    print(f"  추가 후: {after_count:,}개")
    print(f"  추가된 제품: {after_count - before_count}개")
    
    manager.close()


def demo_error_handling():
    """예외 처리 예제"""
    print("\n" + "="*60)
    print("[예제 5] 예외 처리")
    print("="*60)
    
    manager = ProductManager('MyProduct.db')
    
    print("\n▶ 존재하지 않는 ID 삭제 시도")
    print("-" * 60)
    result = manager.delete(999999)
    if not result:
        print("  ✓ 적절히 처리되었습니다")
    
    print("\n▶ 존재하지 않는 ID 조회 시도")
    print("-" * 60)
    product = manager.select_by_id(999999)
    if product is None:
        print("  ✓ 결과 없음: None 반환")
    
    print("\n▶ 존재하지 않는 ID 수정 시도")
    print("-" * 60)
    result = manager.update(999999, product_price=1000000)
    if not result:
        print("  ✓ 적절히 처리되었습니다")
    
    manager.close()


def demo_custom_usage():
    """사용자 정의 활용 예제"""
    print("\n" + "="*60)
    print("[예제 6] 실제 활용 예제")
    print("="*60)
    
    manager = ProductManager('MyProduct.db')
    
    # 특정 가격대의 평균 가격 계산
    print("\n▶ 150만원~200만원대 제품의 평균 가격 계산")
    print("-" * 60)
    products = manager.select_by_price_range(1500000, 2000000)
    if products:
        avg_price = sum(p[2] for p in products) / len(products)
        print(f"  가격대: ₩1,500,000 ~ ₩2,000,000")
        print(f"  해당 제품 수: {len(products)}개")
        print(f"  평균 가격: ₩{avg_price:,.0f}")
    
    # 가장 비싼 제품 찾기
    print("\n▶ 가장 비싼 제품 TOP 5")
    print("-" * 60)
    all_products = manager.select_all()
    sorted_products = sorted(all_products, key=lambda x: x[2], reverse=True)
    for i, prod in enumerate(sorted_products[:5], 1):
        print(f"  {i}. {prod[1]} - ₩{prod[2]:,}")
    
    # 가장 저렴한 제품 찾기
    print("\n▶ 가장 저렴한 제품 TOP 5")
    print("-" * 60)
    sorted_products = sorted(all_products, key=lambda x: x[2])
    for i, prod in enumerate(sorted_products[:5], 1):
        print(f"  {i}. {prod[1]} - ₩{prod[2]:,}")
    
    manager.close()


if __name__ == "__main__":
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "  SQLite 전자제품 데이터베이스 - 사용 예제".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    # 모든 예제 실행
    demo_basic_operations()
    demo_search_operations()
    demo_statistics()
    demo_batch_operations()
    demo_error_handling()
    demo_custom_usage()
    
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "  모든 예제 실행 완료".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60 + "\n")

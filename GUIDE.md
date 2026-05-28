# SQLite 전자제품 데이터베이스 - 사용 설명서

## 📋 개요

이 프로젝트는 Python의 `sqlite3` 모듈을 사용하여 전자제품 데이터를 관리하는 데이터베이스 시스템입니다.

- **데이터베이스 파일**: `MyProduct.db`
- **테이블명**: `Products`
- **샘플 데이터**: 10,000개의 전자제품 데이터

---

## 📦 파일 구조

```
ProductManager.py           # 핵심 클래스 및 메인 프로그램
ProductManager_Demo.py      # 다양한 사용 예제
GUIDE.md                    # 사용 설명서 (이 문서)
MyProduct.db               # SQLite 데이터베이스 파일 (자동 생성)
```

---

## 🗂️ 데이터베이스 구조

### Products 테이블

| 컬럼명 | 데이터타입 | 설명 |
|--------|-----------|------|
| productID | INTEGER | 제품 ID (자동 증가 기본키) |
| productName | TEXT | 제품명 |
| productPrice | INTEGER | 제품 가격 |

---

## 🚀 빠른 시작

### 1. 기본 사용법

```python
from ProductManager import ProductManager

# 데이터베이스 매니저 생성 (자동으로 DB 파일과 테이블 생성)
manager = ProductManager('MyProduct.db')

# 데이터 추가 (INSERT)
product_id = manager.insert("삼성 노트북", 1500000)

# 데이터 조회 (SELECT)
product = manager.select_by_id(product_id)
print(product)  # (1, '삼성 노트북', 1500000)

# 데이터 수정 (UPDATE)
manager.update(product_id, product_price=1600000)

# 데이터 삭제 (DELETE)
manager.delete(product_id)

# 연결 종료
manager.close()
```

---

## 📚 클래스 메서드 상세 설명

### 연결 관련

#### `connect()`
- 데이터베이스에 연결합니다.
- 생성자에서 자동으로 호출됩니다.

```python
manager.connect()
```

#### `close()`
- 데이터베이스 연결을 종료합니다.
- 작업 완료 후 반드시 호출해야 합니다.

```python
manager.close()
```

---

### INSERT (데이터 추가)

#### `insert(product_name, product_price)`
- 단일 제품을 추가합니다.
- **반환값**: 추가된 제품의 ID (성공 시) 또는 None (실패 시)

```python
product_id = manager.insert("LG TV", 2500000)
if product_id:
    print(f"제품이 추가되었습니다 (ID: {product_id})")
```

#### `insert_many(data_list)`
- 여러 제품을 일괄 추가합니다.
- **매개변수**: 리스트 of (product_name, product_price) 튜플

```python
products = [
    ("삼성 모니터", 800000),
    ("LG 프린터", 600000),
    ("ASUS 마우스", 150000),
]
manager.insert_many(products)
```

---

### SELECT (데이터 조회)

#### `select_all()`
- 모든 제품을 조회합니다.
- **반환값**: 모든 제품의 리스트

```python
all_products = manager.select_all()
for product in all_products:
    print(f"ID: {product[0]}, 이름: {product[1]}, 가격: ₩{product[2]:,}")
```

#### `select_by_id(product_id)`
- 특정 ID의 제품을 조회합니다.
- **반환값**: 제품 정보 튜플 또는 None

```python
product = manager.select_by_id(5)
if product:
    print(f"{product[1]} - ₩{product[2]:,}")
```

#### `select_by_name(product_name)`
- 제품명으로 부분 검색합니다.
- **반환값**: 검색된 제품의 리스트

```python
samsung_products = manager.select_by_name("삼성")
print(f"삼성 제품: {len(samsung_products)}개")
```

#### `select_by_price_range(min_price, max_price)`
- 가격 범위로 제품을 검색합니다.
- **반환값**: 범위 내의 제품 리스트

```python
# 100만원 ~ 200만원대 제품 검색
products = manager.select_by_price_range(1000000, 2000000)
print(f"검색 결과: {len(products)}개")
```

---

### UPDATE (데이터 수정)

#### `update(product_id, product_name=None, product_price=None)`
- 제품 정보를 수정합니다.
- **매개변수**: product_id 필수, 수정할 필드 선택
- **반환값**: True (성공) 또는 False (실패)

```python
# 가격만 수정
manager.update(10, product_price=2000000)

# 이름만 수정
manager.update(10, product_name="새로운 제품명")

# 이름과 가격 모두 수정
manager.update(10, product_name="업데이트된 제품", product_price=2500000)
```

---

### DELETE (데이터 삭제)

#### `delete(product_id)`
- 특정 제품을 삭제합니다.
- **반환값**: True (성공) 또는 False (실패)

```python
if manager.delete(10):
    print("제품이 삭제되었습니다")
else:
    print("해당 ID의 제품을 찾을 수 없습니다")
```

#### `delete_all()`
- 모든 제품을 삭제합니다. ⚠️ 주의: 되돌릴 수 없습니다!
- **반환값**: True (성공) 또는 False (실패)

```python
manager.delete_all()
```

---

### 통계 및 정보

#### `get_count()`
- 전체 제품 개수를 반환합니다.
- **반환값**: 정수 (개수)

```python
total_count = manager.get_count()
print(f"총 제품: {total_count:,}개")
```

#### `get_statistics()`
- 데이터베이스 통계 정보를 반환합니다.
- **반환값**: 딕셔너리

```python
stats = manager.get_statistics()
print(f"총 개수: {stats['count']:,}개")
print(f"평균 가격: ₩{stats['average_price']:,.0f}")
print(f"최저 가격: ₩{stats['min_price']:,}")
print(f"최고 가격: ₩{stats['max_price']:,}")
```

---

## 💡 실제 사용 예제

### 예제 1: 특정 가격대 제품 검색 및 수정

```python
from ProductManager import ProductManager

manager = ProductManager('MyProduct.db')

# 100만원 ~ 150만원 제품 조회
products = manager.select_by_price_range(1000000, 1500000)

# 각 제품의 가격을 10% 인상
for product in products[:10]:  # 처음 10개만
    product_id = product[0]
    old_price = product[2]
    new_price = int(old_price * 1.1)
    manager.update(product_id, product_price=new_price)
    print(f"ID {product_id}: ₩{old_price:,} → ₩{new_price:,}")

manager.close()
```

### 예제 2: 제품명 통계

```python
from ProductManager import ProductManager
from collections import Counter

manager = ProductManager('MyProduct.db')

all_products = manager.select_all()

# 제품명에서 첫 번째 단어 추출 (브랜드)
brands = [product[1].split()[0] for product in all_products]
brand_counts = Counter(brands)

# 가장 많은 브랜드 TOP 5
print("브랜드별 제품 수 TOP 5")
for brand, count in brand_counts.most_common(5):
    print(f"  {brand}: {count}개")

manager.close()
```

### 예제 3: 가격대별 제품 분류

```python
from ProductManager import ProductManager

manager = ProductManager('MyProduct.db')

# 가격대별 분류
price_ranges = [
    (0, 500000, "50만원 이하"),
    (500000, 1000000, "50~100만원"),
    (1000000, 2000000, "100~200만원"),
    (2000000, 3000000, "200~300만원"),
    (3000000, 10000000, "300만원 이상"),
]

print("가격대별 제품 분포")
for min_p, max_p, label in price_ranges:
    products = manager.select_by_price_range(min_p, max_p)
    print(f"  {label}: {len(products):,}개")

manager.close()
```

---

## 🔧 데이터베이스 파일 관리

### 데이터베이스 파일 위치
```
c:\Users\student\Desktop\work\MyProduct.db
```

### 기존 데이터 초기화
```python
import os
from ProductManager import ProductManager

# 기존 파일 삭제
if os.path.exists('MyProduct.db'):
    os.remove('MyProduct.db')

# 새로운 데이터베이스 생성
manager = ProductManager('MyProduct.db')
# ... 초기 데이터 추가
manager.close()
```

---

## ⚠️ 주의사항

1. **여러 프로세스**: SQLite는 단일 파일 기반이므로 동시 접근 시 주의가 필요합니다.
2. **트랜잭션**: 자동 커밋이 설정되어 있으므로 각 작업이 즉시 반영됩니다.
3. **연결 종료**: 작업 완료 후 반드시 `close()`를 호출해야 합니다.
4. **데이터 백업**: 중요한 데이터는 정기적으로 백업하세요.

---

## 🐛 문제 해결

### 문제: "데이터베이스 잠금" 오류
**해결**: 다른 프로세스에서 데이터베이스를 사용 중인지 확인하세요.

### 문제: "테이블이 존재하지 않음" 오류
**해결**: `ProductManager()` 생성자가 자동으로 테이블을 생성하므로, 데이터베이스 파일을 삭제 후 다시 생성하세요.

### 문제: 데이터가 저장되지 않음
**해결**: `insert_many()` 또는 수정 후 `close()`를 호출했는지 확인하세요.

---

## 📊 성능 팁

1. **대량 데이터 추가**: `insert_many()` 사용 (단일 INSERT보다 빠름)
2. **인덱스**: 자주 검색하는 컬럼에 인덱스를 추가하면 조회 성능 향상
3. **배치 작업**: 여러 작업을 한 번에 처리하기

---

## 📞 지원

이 코드는 교육 목적으로 작성되었습니다.
문제가 발생하면 주석을 참고하거나 예제 파일(`ProductManager_Demo.py`)을 참고하세요.

---

## 📝 라이선스

자유롭게 사용, 수정, 배포할 수 있습니다.

---

**작성일**: 2024년  
**Python 버전**: 3.6+  
**필요 모듈**: sqlite3 (내장)

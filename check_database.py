import sqlite3

conn = sqlite3.connect('MyProduct.db')
cursor = conn.cursor()

# 제품 개수 조회
cursor.execute('SELECT COUNT(*) FROM Products')
product_count = cursor.fetchone()[0]

# 테이블 개수 조회
cursor.execute('SELECT COUNT(*) FROM sqlite_master WHERE type="table"')
table_count = cursor.fetchone()[0]

# 테이블 정보 조회
cursor.execute("PRAGMA table_info(Products)")
columns = cursor.fetchall()

print("\n" + "="*60)
print("✓ SQLite 데이터베이스 생성 완료")
print("="*60)
print(f"\n📊 데이터베이스 정보:")
print(f"  • 파일명: MyProduct.db")
print(f"  • 테이블 개수: {table_count}개")
print(f"  • 총 제품: {product_count:,}개")

print(f"\n📋 테이블 구조 (Products):")
for col in columns:
    col_id, col_name, col_type, notnull, default_val, pk = col
    pk_mark = " [PRIMARY KEY]" if pk else ""
    print(f"  • {col_name} ({col_type}){pk_mark}")

# 통계 조회
cursor.execute('SELECT AVG(productPrice), MIN(productPrice), MAX(productPrice) FROM Products')
avg_price, min_price, max_price = cursor.fetchone()

print(f"\n💰 가격 통계:")
print(f"  • 평균 가격: ₩{avg_price:,.0f}")
print(f"  • 최저 가격: ₩{min_price:,}")
print(f"  • 최고 가격: ₩{max_price:,}")

conn.close()

print("\n" + "="*60)
print("✓ 모든 설정이 완료되었습니다!")
print("="*60 + "\n")

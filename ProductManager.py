import sqlite3
import random
from datetime import datetime


class ProductManager:
    """SQLite를 사용하여 전자제품 데이터를 관리하는 클래스"""
    
    def __init__(self, db_name='MyProduct.db'):
        """데이터베이스 초기화 및 테이블 생성"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()
    
    def connect(self):
        """데이터베이스 연결"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"✓ 데이터베이스 '{self.db_name}' 연결 성공")
        except sqlite3.Error as e:
            print(f"✗ 데이터베이스 연결 실패: {e}")
    
    def create_table(self):
        """Products 테이블 생성"""
        try:
            create_table_sql = '''
            CREATE TABLE IF NOT EXISTS Products (
                productID INTEGER PRIMARY KEY AUTOINCREMENT,
                productName TEXT NOT NULL,
                productPrice INTEGER NOT NULL
            )
            '''
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            print("✓ Products 테이블이 준비되었습니다")
        except sqlite3.Error as e:
            print(f"✗ 테이블 생성 실패: {e}")
    
    def insert(self, product_name, product_price):
        """제품 데이터 추가"""
        try:
            insert_sql = 'INSERT INTO Products (productName, productPrice) VALUES (?, ?)'
            self.cursor.execute(insert_sql, (product_name, product_price))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"✗ 데이터 추가 실패: {e}")
            return None
    
    def insert_many(self, data_list):
        """여러 제품 데이터 일괄 추가"""
        try:
            insert_sql = 'INSERT INTO Products (productName, productPrice) VALUES (?, ?)'
            self.cursor.executemany(insert_sql, data_list)
            self.conn.commit()
            print(f"✓ {len(data_list)}개의 데이터가 추가되었습니다")
        except sqlite3.Error as e:
            print(f"✗ 대량 데이터 추가 실패: {e}")
    
    def select_all(self):
        """모든 제품 조회"""
        try:
            select_sql = 'SELECT * FROM Products'
            self.cursor.execute(select_sql)
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"✗ 데이터 조회 실패: {e}")
            return []
    
    def select_by_id(self, product_id):
        """ID로 제품 조회"""
        try:
            select_sql = 'SELECT * FROM Products WHERE productID = ?'
            self.cursor.execute(select_sql, (product_id,))
            result = self.cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"✗ 데이터 조회 실패: {e}")
            return None
    
    def select_by_price_range(self, min_price, max_price):
        """가격 범위로 제품 조회"""
        try:
            select_sql = 'SELECT * FROM Products WHERE productPrice BETWEEN ? AND ? ORDER BY productPrice'
            self.cursor.execute(select_sql, (min_price, max_price))
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"✗ 데이터 조회 실패: {e}")
            return []
    
    def select_by_name(self, product_name):
        """이름으로 제품 조회 (부분 검색)"""
        try:
            select_sql = 'SELECT * FROM Products WHERE productName LIKE ?'
            self.cursor.execute(select_sql, (f'%{product_name}%',))
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"✗ 데이터 조회 실패: {e}")
            return []
    
    def update(self, product_id, product_name=None, product_price=None):
        """제품 데이터 수정"""
        try:
            if product_name is None and product_price is None:
                print("✗ 수정할 데이터가 없습니다")
                return False
            
            if product_name is not None and product_price is not None:
                update_sql = 'UPDATE Products SET productName = ?, productPrice = ? WHERE productID = ?'
                self.cursor.execute(update_sql, (product_name, product_price, product_id))
            elif product_name is not None:
                update_sql = 'UPDATE Products SET productName = ? WHERE productID = ?'
                self.cursor.execute(update_sql, (product_name, product_id))
            else:
                update_sql = 'UPDATE Products SET productPrice = ? WHERE productID = ?'
                self.cursor.execute(update_sql, (product_price, product_id))
            
            self.conn.commit()
            if self.cursor.rowcount > 0:
                return True
            else:
                print(f"✗ 해당 ID({product_id})를 찾을 수 없습니다")
                return False
        except sqlite3.Error as e:
            print(f"✗ 데이터 수정 실패: {e}")
            return False
    
    def delete(self, product_id):
        """제품 데이터 삭제"""
        try:
            delete_sql = 'DELETE FROM Products WHERE productID = ?'
            self.cursor.execute(delete_sql, (product_id,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                return True
            else:
                print(f"✗ 해당 ID({product_id})를 찾을 수 없습니다")
                return False
        except sqlite3.Error as e:
            print(f"✗ 데이터 삭제 실패: {e}")
            return False
    
    def delete_all(self):
        """모든 제품 데이터 삭제"""
        try:
            delete_sql = 'DELETE FROM Products'
            self.cursor.execute(delete_sql)
            self.conn.commit()
            print(f"✓ {self.cursor.rowcount}개의 데이터가 삭제되었습니다")
            return True
        except sqlite3.Error as e:
            print(f"✗ 모든 데이터 삭제 실패: {e}")
            return False
    
    def get_count(self):
        """전체 제품 개수 조회"""
        try:
            count_sql = 'SELECT COUNT(*) FROM Products'
            self.cursor.execute(count_sql)
            count = self.cursor.fetchone()[0]
            return count
        except sqlite3.Error as e:
            print(f"✗ 개수 조회 실패: {e}")
            return 0
    
    def get_statistics(self):
        """가격 통계 조회"""
        try:
            stats_sql = 'SELECT COUNT(*), AVG(productPrice), MIN(productPrice), MAX(productPrice) FROM Products'
            self.cursor.execute(stats_sql)
            count, avg_price, min_price, max_price = self.cursor.fetchone()
            return {
                'count': count,
                'average_price': round(avg_price, 2) if avg_price else 0,
                'min_price': min_price,
                'max_price': max_price
            }
        except sqlite3.Error as e:
            print(f"✗ 통계 조회 실패: {e}")
            return None
    
    def close(self):
        """데이터베이스 연결 종료"""
        if self.conn:
            self.conn.close()
            print("✓ 데이터베이스 연결이 종료되었습니다")


def generate_sample_data(count=10000):
    """샘플 제품 데이터 생성"""
    categories = ['노트북', '스마트폰', '태블릿', '모니터', 'TV', '이어폰', '마우스', '키보드', '프린터', 'SSD']
    brands = ['삼성', 'LG', '애플', 'HP', '델', '소니', '캐논', '에이수스', '레노버', 'MSI']
    
    sample_data = []
    for i in range(count):
        category = random.choice(categories)
        brand = random.choice(brands)
        product_name = f"{brand} {category} {i+1:05d}"
        product_price = random.randint(50000, 5000000)
        sample_data.append((product_name, product_price))
    
    return sample_data


if __name__ == "__main__":
    print("="*60)
    print("SQLite 전자제품 데이터베이스 관리 시스템")
    print("="*60)
    
    # ProductManager 객체 생성
    manager = ProductManager('MyProduct.db')
    
    # 기존 데이터 확인
    existing_count = manager.get_count()
    
    if existing_count == 0:
        print("\n[1단계] 샘플 데이터 생성 중...")
        sample_data = generate_sample_data(10000)
        
        print("[2단계] 샘플 데이터 추가 중...")
        manager.insert_many(sample_data)
    else:
        print(f"\n데이터베이스에 이미 {existing_count}개의 데이터가 있습니다")
    
    # 통계 정보 출력
    print("\n" + "="*60)
    print("[데이터베이스 통계]")
    print("="*60)
    stats = manager.get_statistics()
    if stats:
        print(f"총 제품 개수: {stats['count']:,}개")
        print(f"평균 가격: ₩{stats['average_price']:,.0f}")
        print(f"최저 가격: ₩{stats['min_price']:,}")
        print(f"최고 가격: ₩{stats['max_price']:,}")
    
    # CRUD 작업 예제
    print("\n" + "="*60)
    print("[CRUD 작업 예제]")
    print("="*60)
    
    # INSERT 예제
    print("\n[INSERT] 새로운 제품 추가")
    new_product_id = manager.insert("삼성 갤럭시북 프로 15", 2500000)
    if new_product_id:
        print(f"✓ 제품이 추가되었습니다 (ID: {new_product_id})")
    
    # SELECT 예제
    print("\n[SELECT] ID로 제품 조회")
    product = manager.select_by_id(new_product_id)
    if product:
        print(f"✓ ID: {product[0]}, 상품명: {product[1]}, 가격: ₩{product[2]:,}")
    
    # UPDATE 예제
    print("\n[UPDATE] 제품 정보 수정")
    if manager.update(new_product_id, product_price=2800000):
        product = manager.select_by_id(new_product_id)
        print(f"✓ 수정 완료 - 새로운 가격: ₩{product[2]:,}")
    
    # SELECT 범위 검색 예제
    print("\n[SELECT] 가격대별 제품 검색 (100만원~200만원)")
    products = manager.select_by_price_range(1000000, 2000000)
    print(f"✓ 검색 결과: {len(products)}개의 제품")
    for i, product in enumerate(products[:3], 1):
        print(f"  {i}. {product[1]} - ₩{product[2]:,}")
    if len(products) > 3:
        print(f"  ... 외 {len(products)-3}개")
    
    # DELETE 예제 (추가한 제품만 삭제)
    print("\n[DELETE] 제품 삭제")
    if manager.delete(new_product_id):
        print(f"✓ ID {new_product_id} 제품이 삭제되었습니다")
    
    # 최종 통계
    print("\n" + "="*60)
    print(f"최종 데이터베이스 상태: {manager.get_count():,}개의 제품")
    print("="*60)
    
    manager.close()

# 파일 객체 생성
f = open('test.txt', 'w', encoding='utf-8')  # 'w'는 쓰기 모드, 'utf-8'은 인코딩 방식
# 파일에 문자열 쓰기
f.write('Hello, World!\n')      
f.write('This is a test file.\n')
# 파일 닫기
f.close()

# 파일읽기
f = open('test.txt', 'r', encoding='utf-8')  # 'r'은 읽기 모드, 'utf-8'은 인코딩 방식
content = f.read()
print(content)
f.close()


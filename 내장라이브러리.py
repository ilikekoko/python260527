# 내장라이브러리 

import random

print(random.random())  # 0부터 1 사이의 랜덤 실수 출력
print(random.randint(1, 10))  # 1부터 10 사이의 랜덤 정수 출력

print(random.choice(['apple', 'banana', 'cherry']))  # 리스트에서 랜덤 요소 선택
print(random.uniform(1.0, 10.0))  # 1.0부터 10.0 사이의 랜덤 실수 출력


print([random.randrange(20) for i in range(10)])

print(random.sample(range(1,46), 5)) # 1부터 45 사이의 숫자 중에서 5개를 랜덤하게 선택하여 리스트로 반환

fileName = "c:\\python313\\python.exe"

import os.path

print(os.path.basename(fileName)) # 파일 이름 추출
print(os.path.dirname(fileName))  # 디렉토리 경로 추출



if os.path.exists(fileName):
    print("파일의 크기 :{0} bytes".format(os.path.getsize(fileName))) # 파일 크기 출력
else:
    print("파일이 존재하지 않습니다.") # 파일이 존재하지 않는 경우 처리


import glob
print(glob.glob('*.py'))  # 현재 디렉토리의 모든 .py 파일 목록 출력



import shutil

# 파일 경로 설정
source_file = 'source.txt'  # 원본 파일 경로
destination_file = 'destination.txt'  # 복사할 파일 경로
# 파일 복사
shutil.copy(source_file, destination_file)
print(f'{source_file} has been copied to {destination_file}')


# 사전식 구조

colors = {"apple":["red","aa"], "banana":"yellow"}
print(len(colors))

print(colors["apple"])
# 입력
colors["cherry"] = "red"
# 수정
colors["apple"] = "blue"
print(colors)
# 삭제
del colors["apple"]

for item in colors.items():
    print(item)

print(colors["banana"])    
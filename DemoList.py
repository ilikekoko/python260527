# DemoList.py

lst = [1,2,3,4,5]

print(len(lst))
lst.append(3)
print(lst)

lst.remove(3)
print(lst)

aa = "py" "thon"

print(aa[-3:-1])

#문자열 슬라이싱
strA = "python"
strB = "파이썬은 강력해"
strC = """다중라인으로
저장하는
경우입니다"""

print(strA)
print(strB[0])
print(strB[0:3])
print(strB[-3:])
print(strC)
print(len(strC))

# set형식 
a = {1,2,3,3}
b = {3,4,4,5}
print(a)
print(b)
print(len(a))
print(len(b))
print(a.union(b))
print(a.intersection(b))
print(a.difference(b))


#Tuple 형식
print("=================tp===============")
tp = (10,20,30)
print(len(tp))
print(tp[0])
print(tp.index(30))

def calc(a,b):
    return a+b, a*b

print(calc(3,4))
print("id: %s, name: %s" % ("kim","coco"))

# 형식변환
a = set((1,2,3))
print(a)
b = list(a)
b.append(4)
print(b)







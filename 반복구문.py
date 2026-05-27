value = 5
while value > 0:
    print(value)
    value -= 1

print("for ~ in ")
for i in [1,2,3]:
    print(i)


# 딕셔너리
d = {"name":"전우치", "age":"30", "addr":"city"}
for item in d.items():
    print(item)

print("-------range function -------")
print( list(range(2000,2027)))
print(list(range(1,32)))
print(list(range(1,11,2)))

for i in range(5):
    print(i)

print("------ list comprehention----")
lst = [1,2,3,4,5,6,7,8,10]
print([i**2 for i in lst if i>5])
tp = ("apple","kiwi")
print([len(i) for i in tp])
d = { 100:"apple", 200:"kiwi"}
print( [v.upper() for v in d.values() ])


print("-----------filter function----------")
lst = [10,25,30]
itemL = filter(None, lst)
for item in itemL:
    print(item)

def getBiggerThan20(i):
    return i>20

lst = [10,25,30]
itemL = filter(getBiggerThan20, lst)
for item in itemL:
    print(item)


print("----lambda function----")
itemL = filter(lambda x:x>20, lst)
for item in itemL:
    print(item)
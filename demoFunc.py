# 함수연습

def setValue(newValue):
    x = newValue
    print("함수내부: ",x)


setValue(7)
retValue = setValue(5)
print(retValue)


def swap(a,b):
    return b,a

reVal = swap(3,4)
print(reVal)

#전역변수
x = 5
def func(a):
    return a+x

print(func(1))

def func2(a):
    x=2
    return a+x

print(func2(1))


#기본값을 명시
def times(a=10, b=20):
    return a*b

print(times())
print(times(5))
print(times(5,6))

#키워드 인자
def connectURI(server = "hoho.com", port="9999"):
    strURL = "https://" + server + ":" + port
    return strURL

print(connectURI("naver.com","80"))
print(connectURI(port="8080",server="naver2.com"))
print(connectURI(port="8080"))

#디버깅 예시
def union(*ar):
    result=[]
    for item in ar:
        for x in item:
            if x not in result:
                 result.append(x)
    return result

print(union("HAM","EGG"))
print(union("HAM","EGG","SPAM"))

#람다함수 정의
g = lambda x,y : x*y

print(g(3,4))
print(g(5,6))

print( (lambda x:x*x)(4))

print( dir() )
print( "================================" )
print( globals())


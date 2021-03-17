# 파이썬 람다식
# 다중 리턴
def func_mul(x):
    y1 = x * 100
    y2 = x * 200
    y3 = x * 300
    return y1,y2,y3

val1, val2, val3 = func_mul(100)
print(type(val1), val1, val2, val3)

# 데이터 타입 변환 가능


# *args, *kwargs

def args_func(*args): #매개변수 개수를 알지 못할 때 다양한 매개변수를 받을 수 있음 -> 다 튜플 형태로 작동함
    print(args)
    # for t in args:
    #     print(t)
    for i,v in enumerate(args): # 알아서 인덱스를 만들어서 사용가능
        print(i, v)

args_func('kim')
args_func('kim', 'park')


# kwargs : 딕셔너리 형태로 넘어감

def kwargs_func(**kwargs):
    print(kwargs)
    for k, v in kwargs.items():
        print(k, v)

kwargs_func(name1='kim', name2='Park', name3='Lee')

# 혼합
def example_mul(arg1, arg2, *args, **kwargs): # 여러개의 인자를 사용해서 들어오는 게 어떤 것인지에 따라서 적용해서 쓰면 됨
    print(arg1, arg2, args, kwargs)

example_mul(10, 20)


# 중첩 함수(클로저) -> 변수 선언 줄이기
# 데코레이터 클로저 
def nested_func(num):
    def func_in_func(num):
        print(num)
    print("in func")
    func_in_func(num + 10000)

nested_func(10000)


# nonlocal
z = 3

def outer(x):
    y = 10
    def inner():
        x = 1000
        return x

    return inner()

print(outer(10))


# hint 사용하기
def func_mul3(x : int) -> list:
    y1 = x * 100
    y2 = x * 200
    y3 = x * 300
    return [y1,y2,y3]


print(func_mul3(5.0))


# 람다식
# 람다식 : 메모리 절약, 가독성 향상, 코드 간결
# 함수는 객체 생성 -> 리소스(메모리) 할당
# 람다는 즉시 실행(Heap 초기화) -> 메모리 초기화

# 일반적 함수 -> 변수 할당
def mul_10(num : int) -> int:
    return num * 10

var_func = mul_10 #이미 메모리에 올라가있음
print(var_func)
print(type(var_func))

print(var_func(10))

lambda_mul_10 = lambda num: num * 10

print('>>>', lambda_mul_10(10))

def func_final(x, y, func):
    print(x * y * func(10))

func_final(10, 10, lambda_mul_10) # 함수를 매개변수로 넘길 때

print(func_final(10, 10, lambda x : x * 1000)) # 함수를 직접적으로 만듦(한번 실행할 때)
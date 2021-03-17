# self , 클래스, 인스턴스 변수

# 클래스, 인스턴스 차이 중요
# 네임스페이스 : 객체를 인스턴스화 할 때 저장된 공간
# 클래스 변수 : 직접 사용 가능, 객체보다 먼저 생성
# 인스턴스 변수 : 객체마다 별도로 존재, 인스턴스 생성 후 사용

# 선언
# class 클래스명:
#     함수
#     함수
#     함수

# 예제1
class UserInfo:
    # 속성, 메소드
    def __init__(self, name):
        self.name = name
    def print_user_p(self):
        print("Name : ", self.name)
    
# 네임스페이스 안에는 전혀 다른 값이 들어가있기 때문에 같다고 할 수 없다
user1 = UserInfo("kim")
user1.print_user_p()
user2 = UserInfo("Park")
user2.print_user_p()

print(id(user1))
print(id(user2))


# self 이해
class SelfTest():
    def function1(): # 클래스 메소드
        print('function1 called!')

    def function2(self): # 인스턴스 메소드
        print(id(self))
        print('function2 called!')

self_test = SelfTest()
# self_test.function1() -> 클래스 메소드라서 이렇게 호출할 수 없다
SelfTest.function1()
self_test.function2()

print(id(self_test))
SelfTest.function2(self_test)


# 클래스 변수, 인스턴스 변수

class WareHouse:
    # 클래스 변수
    stock_num = 0
    def __init__(self, name):
        self.name = name
        WareHouse.stock_num += 1

    def __del__(self):
        WareHouse.stock_num -= 1
    

user1 = WareHouse('Kim')
user2 = WareHouse('Park')
user3 = WareHouse('Lee')

print(user1.__dict__)
print(user2.__dict__)
print(user3.__dict__)
print(WareHouse.__dict__) #클래스 네임스페이스, 클래스 변수 공유

print(user1.name)
print(user2.name)
print(user3.name)

print(user1.stock_num)
print(user2.stock_num)
print(user3.stock_num)

del user1

print(user2.stock_num)
print(user3.stock_num)
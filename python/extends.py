# 상속, 다중 상속

# 상속 기본
# 슈퍼클래스(부모) 및 서브클래스(자식) -> 모든 속성, 메소드 사용 가능

# 라면 -> 속성(종류, 회사, 맛, 면 종류, 이름) : 부모

class Car:
    """parent class"""
    def __init__(self, tp, color):
        self.type = tp
        self.color = color
    
    def show(self):
        return 'Car Class "show Method!"'


class BmwCar(Car):
    '''Sub Class'''
    def __init__(self, car_name,tp, color):
        super().__init__(tp, color)
        self.car_name = car_name

    def show_model(self) ->  None:
        return "Your Car Name : %s" %self.car_name

class BenzCar(Car):
    '''Sub Class'''
    def __init__(self, car_name,tp, color):
        super().__init__(tp, color)
        self.car_name = car_name

    def show_model(self) ->  None:
        return "Your Car Name : %s" %self.car_name

    def show(self):
        print(super().show())
        return 'Car Info : %s %s %s' %(self.car_name, self.type, self.color)


# 일반 사용
model1 = BmwCar('520d', 'sedan', 'red')

print(model1.color) #super
print(model1.type) #super
print(model1.car_name) #sub
print(model1.show()) #super
print(model1.show_model()) #sub
print(model1.__dict__)


#method overriding(오버라이딩) -> 코드 재활용
model2 = BenzCar("220d", 'suv', 'black')
print(model2.show())

#Parent Method Call
model3 = BenzCar("350s", 'sadan', 'silver')
print(model3.show())

#Inheritance Info(상속 정보)
print(BmwCar.mro())
print(BenzCar.mro())

#다중 상속

class X():
    pass

class Y():
    pass

class Z():
    pass

class A(X, Y):
    pass

class B(Y, Z):
    pass

class M(B, A, Z): # 클래스 안에 있는 모든 것을 상속 받음!
    pass

print(M.mro()) # [<class '__main__.M'>, <class '__main__.B'>, <class '__main__.A'>, <class '__main__.X'>, <class '__main__.Y'>, <class '__main__.Z'>, <class 'object'>]
print(A.mro()) # [<class '__main__.A'>, <class '__main__.X'>, <class '__main__.Y'>, <class 'object'>]
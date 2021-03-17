def outer_func(): #1
    message = 'Hi' #3

    def inner_func(): #4
        print(message) #6 

    return inner_func #5

my_func = outer_func() #2
my_func()
my_func()
my_func()


# 클로저를 사용해서 하나의 함수로 여러가지의 함수를 간단히 만들 수 있으며, 기존에 만들어진 함수나 모듈등을 수정하지 않고 wrapper 함수를 이용해 커스터마이징을 할 수 있게 해주는 것
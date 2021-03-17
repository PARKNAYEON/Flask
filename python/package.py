# 파이썬 모듈과 패키지

#패키지 예제
# 상대 경로


from pkg.fibonacci import Fibonacci

Fibonacci.fib(300)

print("ex1 : ", Fibonacci.fib2(400))
print("ex1 : ", Fibonacci().title) # 클래스 생성 후 (인스턴스 하고 난 후)



from pkg.fibonacci import * # 전부 다 가져오겠다,,, 절대 권장하지 않음

Fibonacci.fib(500)

print("ex2 : ", Fibonacci.fib2(600))
print("ex2 : ", Fibonacci().title) # 클래스 생성 후 (인스턴스 하고 난 후)


from pkg.fibonacci import Fibonacci as fb # 가독성을 올리기 위해서 권장함!!

fb.fib(1000)

print("ex3 : ", fb.fib2(1600))
print("ex3 : ", fb().title) # 클래스 생성 후 (인스턴스 하고 난 후)


import pkg.calculations as c

print("ex4 : ", c.add(10, 100))
print("ex4 : ", c.mul(10, 100))


from pkg.calculations import div as d
# 필요한 것만 가져오기!

print("ex 5 : " ,int(d(100, 10)))

import pkg.prints as p
import builtins

p.prt1()
p.prt2()
print(dir(builtins))
# 흐름제어, 병행처리(Concurrency)

# 파이썬 반복형 종류
# for, collections, text file, List, Dict, Set, Tuple, unpacking, *args
# 반복형 객체 내부적으로 iter 함수 내용, 제네레이터 동작 원리, yield from

# 반복 가능한 이유? -> iter(x) 함수 호출

t = 'ABCDEF'

# for  사용
for c in t:
    print('Ex1-1 -', c)

print()

#while

w = iter(t)
while True:
    try:
        print('Ex1-2 -', next(w))
    except StopIteration:
        break

from collections import abc

# 반복형 확인
print('EX1-3 -', hasattr(t, '__iter__'))
print('Ex1-4 -', isinstance(t, abc.Iterable))

print()
print()

# next 사용

class WordSplitIter:
    def __init__(self, text):
        self._idx = 0
        self._text = text.split(' ')

    def __next__(self):
        print('Called __next__')
        try:
            word = self._text[self._idx]
        except IndexError:
            raise StopIteration('test')
        self._idx += 1
        return word

    def __iter__(self):
        print('Called __iter__')
        return self

    def __repr__(self):
        return 'WordSplit(%s)' %(self._text)

wi = WordSplitIter('Who says the nights are for sleeping')

print('Ex2-1 -', wi)
print('Ex2-1 -', next(wi))
print('Ex2-2 -', next(wi))
print('Ex2-3 -', next(wi))
print('Ex2-4 -', next(wi))
print('Ex2-5 -', next(wi))
print('Ex2-6 -', next(wi))
print('Ex2-7 -', next(wi))
# print('Ex2-8 -', next(wi))
# print('Ex2-9 -', next(wi))

print()
print()

# generator 패턴
# 지능형 리스트, 딕셔너리, 집합 -> 데이터 셋이 증가 될 경우 메모리 사용량 증가 -> 제네레이터 완화
# 단위 실행 가능한 코루틴 구현에 아주 중요
# 딕셔너리, 리스트 한 번 호출 할 때마다 하나의 값만 리턴 -> 아주 작은 메모리 양을 필요로 함

class WordSplitGenerator:
    def __init__(self, text):
        self._idx = 0
        self._text = text.split(' ')

    def __iter__(self):
        for word in self._text:
            yield word # generator
        return

    def __repr__(self):
        return 'WordSplit(%s)' %(self._text)

wg = WordSplitGenerator('Who says the nights are for sleeping')

wt = iter(wg)

print('Ex3-1 -', wt)
print('Ex3-1 -', next(wt))
print('Ex3-2 -', next(wt))
print('Ex3-3 -', next(wt))
print('Ex3-4 -', next(wt))
print('Ex3-5 -', next(wt))
print('Ex3-6 -', next(wt))
print('Ex3-7 -', next(wt))
# print('Ex2-8 -', next(wi))
# print('Ex2-9 -', next(wi))


def generator_ex1():
    print('start!')
    yield 'AAA'
    print('continue')
    yield 'BBB'
    print('end')

temp = iter(generator_ex1())

# print('EX4-1 -', next(temp))
# print('EX4-2 -', next(temp))

# 더 안전하게 사용할 수 있다.
for v in generator_ex1():
    # print('EX4-3 -', v)
    pass

print()
print()

# Generator 예제2
temp2 = [x * 3 for x in generator_ex1()]
temp3 = (x * 3 for x in generator_ex1())

# print('Ex5-1 -', temp2)
# print('Ex5-1 -', temp3)

for i in temp2:
    print('Ex5-3 -',i)

print()
print()

for i in temp3:
    print('Ex5-4 -',i)

print()
print()

# Generator 예제3(자주 사용하는 함수)

import itertools

gen1 = itertools.count(1, 2.5) # next가 호출되어야 반환한다(아주 적은 메모리만 쓴다)

print('Ex6-1 -', next(gen1))
print('Ex6-2 -', next(gen1))
print('Ex6-3 -', next(gen1))
print('Ex6-4 -', next(gen1))
#... infinite

print()

# 조건
gen2 = itertools.takewhile(lambda n : n < 1000, itertools.count(1, 2.5))

for v in gen2:
    print('Ex6-5 -', v)

print()

# 핕터 반대
gen3 = itertools.filterfalse(lambda n : n <3, [1,2,3,4,5])
for v in gen3:
    print('Ex6-6 -', v)

print()

# 누적 합계
gen4 = itertools.accumulate([x for x in range(1, 101)])

for v in gen4:
    print('Ex6-7 -', v)

print()

# 연결1
gen5 = itertools.chain('ABCDE', range(1,11,2))
print('Ex6-8 -', list(gen5))

# 연결2
gen6 = itertools.chain(enumerate('ABCDE'))
print('Ex6-9 -', list(gen6))

# 개별
gen7 = itertools.product('ABCDE')
print('Ex6-10 -', list(gen7))

# 연산
gen8 = itertools.product('ABCDE', repeat=2)
print('Ex6-11 -', list(gen8))

# 그룹화
gen9 = itertools.groupby('AAABBCCCCDDEE')
# print('Ex6-12 -', list(gen9))
for chr,group in gen9:
    print('Ex6-12 -', chr, ' : ', list(group))



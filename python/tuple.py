# 튜플 (순서o, 중복o, 수정 x, 삭제 x)

a = ()
b = (1, )
c = (1, 2, 3, 4)
d = (10, 100, ('a', 'b', 'c'))


# del c[2]

print(c[2])
print(c[3])
print(d[2][2])

print(d[2:])
print(d[2][0:2])

print(c + d)
print(c * 3)
print()
print()

# 튜플 함수

z = (5,2,1,3,4,1)

print(z)
print(3 in z)
print(z.index(5))
print(z.count(1))



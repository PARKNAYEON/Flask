# 클래스 구조
# 구조 설계 후 재사용성 증가, 코드 반복 최소화, 메소드 활용

class Student(object):
    def __init__(self, name, number, grade, details):
        self._name = name
        self._number = number
        self._grade = grade
        self._details = details

    def __str__(self):
        return 'str : {} - {}'.format(self._name, self._number)

    # str 이 없을 때 실행된다 아니면 직접적으로 repr을 호출한다
    def __repr__(self):
        return 'str : {} - {}'.format(self._name, self._number)

    
student1 = Student('Kim',1, 1, {'gender' : 'Male', 'score1' : 95})
student2 = Student('Lee',2, 3, {'gender' : 'Male', 'score1' : 77})
student3 = Student('Kim',3, 4, {'gender' : 'Male', 'score1' : 95})

# 모든 객체는 딕셔너리 안에 포함되어 있다. -> __dict__ : 속성값을 알 수 있다
print(student1.__dict__)


# 리스트 선언
students_list = []
students_list.append(student1)
students_list.append(student2)
students_list.append(student3)

print(students_list)

# 반복(__str__)
for x in students_list:
    # print(repr(x))
    print(x)
    # __str__ 함수로 여기가
    # str : Kim
    # str : Lee
    # str : Kim
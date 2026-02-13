# 파이썬에서 일반적인 함수 정의하기
def some(a, b):
    return a + b
print(some(3, 5))

# 클래스 정의
class Person:
    # 클래스 변수
    blood_color = 'red'

    def __init__(self, name):
        # 인스턴스 변수
        self.name = name

    # 인스턴스 메서드
    def singing(self):
        return f'{self.name}가 노래합니다.'


# 인스턴스 생성
singer1 = Person('iu')
# 메서드 호출
print(singer1.singing())  
# 속성(변수) 접근
print(singer1.blood_color)

# 두번째 인스턴스 생성
singer2 = Person('winter')


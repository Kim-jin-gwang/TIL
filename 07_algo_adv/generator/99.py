import inspect
# inspect 모듈은 객체의 정보를 얻을 수 있는 다양한 함수를 제공하는 모듈

def gen():
    print('A, 시작')
    x = 1
    yield x
    print('B, 중간')
    x += 1
    yield x
    print('C, 끝')


g = gen()
print('상태:', inspect.getgeneratorstate(g))  # GEN_CREATED

print("next ->", next(g))
print('상태:', inspect.getgeneratorstate(g))  # GEN_SUSPENDED

print("next ->", next(g))
print('상태:', inspect.getgeneratorstate(g))  # GEN_SUSPENDED

try:
    print("next ->", next(g))
except StopIteration:
    print("StopIteration raised")
print('상태:', inspect.getgeneratorstate(g))  # GEN_CLOSED
# 후입 선출이 가능한 Stack 클래스 구현
class Stack:
    # 스택을 초기화 하는 메서드
    def __init__(self, size=10):
        self.size = size
        self.items = [None] * size
        self.top = -1

    # 스택이 가득 찼는지 확인하는 메서드
    def is_full(self):
        # 반환값이 True라면, 꽉찼다는뜻
        return self.top == self.size - 1

    # 데이터를 삽입하는 메서드
    def push(self, item):
        if self.is_full():
            print('Stack이 꽉 찼어요!')
            return
        self.top += 1
        self.items[self.top] = item

    # 스택이 비어있는지 확인하는 메서드
    def is_empty(self):
        # True를 반환한다면, 비었다는 뜻
        return self.top == -1

    # 데이터를 제거 하는 메서드
    def pop(self):
        if self.is_empty():
            print('스택이 비었습니다!')
            return
        delete_data = self.items[self.top]
        self.items[self.top] = None
        self.top -= 1
        return delete_data


    pass
    
stack = Stack()

stack.push(1)
stack.push(2)
stack.push(3)
print(stack.items)

print(stack.pop())
print(stack.pop())
# print(stack.peek())
# print(stack.is_empty())
# print(stack.pop())
# print(stack.pop())

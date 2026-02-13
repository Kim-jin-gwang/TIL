class Queue:
    # 초기화 메서드
    def __init__(self, size=5):
        self.items = [None] * size
        self.size = size
        self.front = -1
        self.rear = -1

    # 꽉 찼는지 확인하는 메서드
    def is_full(self):
        return self.rear == self.size - 1

    # 값을 삽입하는 메서드
    def enqueue(self, item):
        if self.is_full():
            print('큐가 가득 찼습니다.')
            return
        self.rear += 1
        self.items[self.rear] = item

    # 비었는지 확인하는 메서드
    def is_empty(self):
        # 값을 삽입할때 rear가 1씩 증가
        # 값을 제거할때 front가 1씩 증가
        # 따라서, 삽입한 만큼 제거했다 -> 비었다
        # == front와 rear가 같은 위치에 있다.
        return self.front == self.rear
    
    # 값을 제거하는 메서드
    def dequeue(self):
        if self.is_empty():
            print('큐가 이미 비었습니다.')
            return
        self.front += 1
        delete_data = self.items[self.front]
        self.items[self.front] = None
        return delete_data

queue = Queue()

queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)

print(queue.items)
print(queue.dequeue())
print(queue.dequeue())
print(queue.dequeue())
print(queue.is_empty())
print(queue.items)
# print(queue.peek())

queue.enqueue(4)
queue.enqueue(5)

print(queue.items)
print(queue.is_full())
# queue.enqueue(11)
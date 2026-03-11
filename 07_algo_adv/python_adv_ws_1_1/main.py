class EvenIterator:
    def __init__(self, N):
        self.N = N
        self.cur = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.cur <= self.N:
            if self.cur % 2 == 0:
                v = self.cur
                self.cur += 1
                return v
            self.cur += 1
        
        raise StopIteration
        
        
# 사용 예시:
N = 10
even_iterator = EvenIterator(N)
for even_number in even_iterator:
    print(even_number)
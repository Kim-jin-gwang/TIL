class CountUp:
    def __init__(self, start, end):
        self.cur = start
        self.end = end

    # __iter__는 iterable 객체에서 iterator 객체를 반환하는 메서드
    def __iter__(self):
        return self  # iterator == iterable

    def __next__(self):
        # StopIteration 예외를 발생시키면 for 루프가 종료됨
        if self.cur > self.end:
            raise StopIteration
        v = self.cur
        self.cur += 1
        return v


for x in CountUp(3, 7):
    print(x)
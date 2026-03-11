def count_up(start, end):
    cur = start
    while cur <= end:
        yield cur
        cur += 1

for x in count_up(3, 7):
    print(x)
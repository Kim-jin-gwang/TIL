# 5! -> 5 * 4 * 3 * 2 * 1
# 최종 결괏값
result = 1   # 곱해 나갈것이기 때문에
# 구하고자 하는 값 N
N = 5
# 반복문 -> for, while
# for문 이라면 순회할 요소가 필요하다
# 5 4 3 2 1 > 곱하기라면, 순서는 상관없다!
for num in range(1, N+1):
    result = result * num
print(result)

# while 문이라면?
result = 1
while N >= 1:
    result *= N
    N -= 1
print(result)
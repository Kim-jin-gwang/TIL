def fibo(n):
    global count
    count += 1
    # 기본값은 0과 1은 무시
    # 아직 계산된 적 없다면 계산
    if n >= 2 and memo[n] == 0:
        # 할일
        memo[n] = fibo(n-1) + fibo(n-2)
    return memo[n]  # n번째 피보나치 수를 반환

n = 100
count = 0
memo = [0] * (n + 1) # 작은 문제들을 기록
# 피보나치 수열의 가장 작은 기본값
memo[0] = 0
memo[1] = 1
print(fibo(n), count)
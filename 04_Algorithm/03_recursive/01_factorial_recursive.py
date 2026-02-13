def fact(n):
    # 기본 부분 (basis part)
    if n == 1:
        return 1
    # 유도 부분 (inductive parte)
    else:
        # 자기 자신을 다시 호출
        return n * fact(n-1)

# 사용 예시
print(fact(5))  # 5*4*3*2*1을 계산하여 120을 출력합니다

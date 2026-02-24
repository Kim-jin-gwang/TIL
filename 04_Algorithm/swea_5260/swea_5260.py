import sys
sys.stdin = open("input.txt", "r")

'''
- 1부터 N까지 양의 정수를 원소로 갖는 집합이 있음
- 이 집합의 모든 부분 집합에 대해 원소의 합이 K인 경우의 수 M을 알아내려 함


'''


T = int(input())
for t in range(1,T+1):
    N,K = map(int,input().split())
    dp = [0] * (K+1)
    dp[0] = 1

    for i in range(1,N+1):
        for j in range(K,i-1,-1):
            dp[j] += dp[j-i]  # 합 j를 만드는 방법의 개수
    
    print(f'#{t} {dp[K]}')
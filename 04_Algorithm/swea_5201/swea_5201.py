import sys
sys.stdin = open("input.txt", "r")



T = int(input())
for t in range(1,T+1):
    N,M = map(int,input().split())      # N : 컨테이너 수, M : 트럭 수
    Wi = sorted(list(map(int,input().split())), reverse=True)  # Wi : N개의 화물의 무게
    Ti = sorted(list(map(int,input().split())), reverse=True)  # Ti : M개 트럭의 적재용량

    ans = 0

    # for 트럭 -> if 화물을 들 수 있으면 들고가기
    for i in range(M):
        while Wi:
            if Ti[i] < Wi[0]:
                Wi.pop(0)
            
            elif Ti[i] >= Wi[0]:
                ans += Wi.pop(0)
                break
    
    print(f'#{t} {ans}')
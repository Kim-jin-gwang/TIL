import sys
sys.stdin = open("input.txt", "r")


'''
 - 마름모 모양의 영역에서만 서비스가 제공됨
    - k = 1 => 운영 비용 = 1
    - k = 2 => 운영 비용 = 5
    - k = 3 => 운영 비용 = 13
    - k = 4 => 운영 비용 = 25
 - 운영 비용 : K * K + (K-1) * (K-1)       ex) K = 3일 때 운영 비용 = 3*3 + 2*2 = 13
 - 홈 방범 서비스를 제공받는 집들은 각각 M의 비용을 지불할 수 있어, 손해를 보지 않는 한 최대한 많은 집에 제공
 
 - 홈 방범 서비스를 제공 받는 집들의 수를 출력하는 프로그램을 작성

 - 아이디어
    - 완전 탐색 하면서 K별 보안회사의 이익을 모두 더하기
    - 마름모를 맨해튼 거리로? |a-b| + |c-d| => abs(a-b) + abs(c-d) <= K
    - 손해만 안보면 되니까 'M*집개수 - cal_cost' 가 양수이기만 하면 됨

    - 중심에서 집까지의 거리가 K가 안넘는 곳을 cnt에 담음
    - 비용이 이득이면 ans에 담음
'''

def cal_cost(K):
    return K**2 + (K-1)**2

T = int(input())
for t in range(1,T+1):
    N,M = map(int,input().split())
    city = [list(map(int,input().split())) for _ in range(N)]
    houses = [(i,j) for i in range(N) for j in range(N) if city[i][j]==1]  # 집 위치 미리 구해놓고 마름모 탐색할 때 K안에 있는지만 판단

    ans = 0

    for r in range(N):
        for c in range(N):
            for k in range(1,N*2):    # K가 N을 다 덮을 정도까지 증가 
                cnt = 0
                for x,y in houses:
                    if abs(r-x) + abs(c-y) < k: # 중심에서 집까지의 거리가 K가 안넘는 곳을 cnt에 담음
                        cnt += 1
                if M*cnt - cal_cost(k) >= 0: 
                    ans = max(ans,cnt)
    
    print(f'#{t} {ans}')




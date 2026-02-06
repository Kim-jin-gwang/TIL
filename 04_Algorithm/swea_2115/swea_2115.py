import sys
sys.stdin = open("input.txt", "r")

'''
- 1. 각각의 일꾼은 가로로 연속되도록 M개의 벌통 선택, 선택한 벌통에서 꿀 채취
- 2. 일꾼들이 선택한 벌통은 겹치면 안됨
- 3. 하나의 벌통에서 채취한 꿀은 하나의 용기에 담아야 함
- 4. 벌통에 있는 모든 꿀을 한번에 채취해야 함
- 5. C보다 많은 꿀을 채취해야 할 때, 많은 이득을 볼 수 있는 꿀통 선택해야 함
- 6. 각 용기에 있는 꿀의 양의 제곱만큼의 수익이 생김

- 일꾼 1이 작업 1을 찾았을 때, 일꾼 2가 얻을 수 있는 최대 값 찾고 그걸 max에 저장
- 
'''




def cal_profix(cells, C):
    M = len(profix)
    best = 0

    def dfs(idx, total, profit):
        nonlocal best

        if total > C:
            return

        if idx == M:
            best = max(best,profix)
            return

        dfs(idx+1, total, profit)
        dfs(idx+1, total+cells[idx], profit + cells[idx]**2)

    dfs(0,0,0)
    return best

T = int(input())
for t in range(1,T+1):
    N,M,C = map(int,input().split())  # 벌통 크기, 선택할 수 있는 벌통 개수, 꿀 채취할 수 있는 최대 양
    honey = [list(map(int,input().split())) for _ in range(N)]
    ans = 0
    profix = [[-1]*(N-M+1) for _ in range(N)]










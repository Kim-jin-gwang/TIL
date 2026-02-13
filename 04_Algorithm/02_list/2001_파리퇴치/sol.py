import sys
sys.stdin = open('input.txt')


T = int(input())

for tc in range(1, T + 1):
    # 가로 N, 범위 M
    N, M = map(int, input().split())
    data = [list(map(int, input().split())) for _ in range(N)]

    # 최종 결괏값
    result = 0

    # 모든 범위에 대해 조사
    '''
        단, x를 기준으로, x부터 + M 까지의 범위를 조사할 것이므로
        조사 대상 시작 범위에 N-M 은 제외한다. 
        예를들어, 다음과 같은 2차원 리스트가 있을때, 범위가 3이라면 
          0 1 2 3 
        0   
        1   . . .
        2   . . .
        3   . . .
        
        위 영역을 조사하고, x를 한칸 옆으로 옮긴 아래와 같은 범위는
        최댓값을 조사하는 이번 과정에서는 필요없는 과정이다.
        y역시 마찬가지지
         0 1 2 3 
        0   
        1     . .
        2     . .
        3     . .
        따라서, N이 4, M이 3일때 최대 조회 시작 index는 1
        4-3 == 1 이므로, range에서는 N-M+1 
    '''
    for x in range(N-M+1):
        for y in range(N-M+1):
            temp = 0
            # 조사 시작지점 x, y에서부터 범위 M만큼 더한 위치를 조사
            for r in range(M):
                for c in range(M):
                    # print(r,c)
                    temp += data[x+r][y+c]  # 값 누적
            # 현재 지점 기준 모든 범위 조사를 끝났다면 최갯값 갱신
            if result < temp:
                result = temp

    print(f'#{tc} {result}')
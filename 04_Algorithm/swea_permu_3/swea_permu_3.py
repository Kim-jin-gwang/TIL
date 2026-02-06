import sys
sys.stdin = open("input.txt", "r")

'''
- 세로, 가로, 미생물 수, 이동방향(상 1, 하 2, 좌 3, 우 4)
- 시간이 다 지난 후 남은 미생물 수를 계산
- 군집이 합쳐질 때, 이동 방향은 가장 군집이 큰 미생물의 이동 방향이 됨
- 필드에 미생물이 있을 때
    - 해당 방향으로 이동(이동한 인덱스에 값 옮기고 원래 자리 값 삭제)
    - 만약 도착 지점으로 이동하는 미생물이 많을 경우 가장 큰 군집의 방향을 따라감
    - 이동한 자리가 가장자리이면 값 감소

'''
def change_move(move):
    if move == 1:
        return 2
    elif move == 2:
        return 1
    elif move == 3:
        return 4
    elif move == 4:
        return 3

def sum_field(field,N):
    res = 0
    for i in range(N):
        for j in range(N):
            if field[i][j]:
                res += field[i][j][0]
    return res

# 상하좌우
dx = {1:-1, 2:1, 3:0, 4:0}
dy = {1:0, 2:0, 3:-1, 4:1}

T = int(input())
for t in range(1,T+1):
    N,M,K = map(int,input().split()) # 셀의 개수, 격리 시간, 군집의 개수
    field = [[0 for _ in range(N)] for _ in range(N)]

    #field에 값 채우기
    for _ in range(K):
        x,y,num,move = map(int,input().split())
        field[x][y] = [num,move]

    # M시간 돌면서 미생물 값 변환
    for _ in range(M):
        #temp = [합 ,최대(move 변동을 위한 저장), move]
        temp = [[None]*N for _ in range(N)] #field는 그대로 두고 여기서 값 채우기

        for x in range(N):
            for y in range(N):
                # field에 값이 없으면 continue
                if not field[x][y]:
                    continue

                size, move = field[x][y]
                nx = x+dx[move]
                ny = y+dy[move]

                #가장자리 처리
                if nx == 0 or nx == N-1 or ny == 0 or ny == N-1:
                    size //= 2
                    move = change_move(move)

                #size가 0이 되면 continue
                if size == 0:
                    continue

                #temp에 값 없으면 추가, 있으면 지금 사이즈랑 temp 최대값 비교
                #[size 총합, size 최댓값, move]
                if temp[nx][ny] == None:
                    temp[nx][ny] = [size,size,move]
                else:
                    temp[nx][ny][0] += size
                    if size > temp[nx][ny][1]:
                        temp[nx][ny][1] = size
                        temp[nx][ny][2] = move

        field = [[0 for _ in range(N)] for _ in range(N)]
        for i in range(N):
            for j in range(N):
                if temp[i][j] is not None:
                    res_size,a,res_move = temp[i][j]
                    field[i][j] = [res_size,res_move]

    ans = sum_field(field,N)
    print(f'#{t} {ans}')


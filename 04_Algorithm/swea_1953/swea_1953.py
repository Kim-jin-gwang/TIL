import sys
sys.stdin = open("input.txt", "r")


from collections import deque


one_dx = [1,-1,0,0]
one_dy = [0,0,1,-1]

two_dx = [1,-1]
two_dy = [0,0]

three_dx = [0,0]
three_dy = [1,-1]

four_dx = [-1,0]
four_dy = [0,1]

five_dx = [1,0]
five_dy = [0,1]

six_dx = [1,0]
six_dy = [0,-1]

seven_dx = [-1,0]
seven_dy = [0,-1]


T = int(input())
for t in range(1,T+1):
    # 세로 크기 N, 가로 크기 M, 맨홀 세로 위치 R, 맨홀 가로 위치 C, 탈출 소요 시간 L
    N,M,R,C,L = map(int,input().split())
    maps = [list(map(int,input().split())) for _ in range(N)]

    queue = deque([(R,C,1)])
    visited =[[False]*M for _ in range(N)]
    visited[R][C] = True
    cnt = 1

    while queue:
        x,y,time = queue.popleft()

        if time == L:
            continue

        if maps[x][y] == 1:  # 상 하 좌 우
            for i in range(4):
                nx = one_dx[i]+x
                ny = one_dy[i]+y
                if one_dx[i] == -1 and one_dy[i] == 0: # 상
                    if 0<=nx<N and 0<=ny<M:
                        if not visited[nx][ny] and maps[nx][ny] in [1,2,5,6]:
                            visited[nx][ny] = True
                            queue.append((nx,ny,time+1))
                            cnt+=1
                elif one_dx[i] == 1 and one_dy[i] == 0: # 하
                    if 0<=nx<N and 0<=ny<M:
                        if not visited[nx][ny] and maps[nx][ny] in [1,2,4,7]:
                            visited[nx][ny] = True
                            queue.append((nx,ny,time+1))
                            cnt+=1
                elif one_dx[i] == 0 and one_dy[i] == -1: # 좌
                    if 0<=nx<N and 0<=ny<M:
                        if not visited[nx][ny] and maps[nx][ny] in [1,3,4,5]:
                            visited[nx][ny] = True
                            queue.append((nx,ny,time+1))
                            cnt+=1
                elif one_dx[i] == 0 and one_dy[i] == 1: # 우
                    if 0<=nx<N and 0<=ny<M:
                        if not visited[nx][ny] and maps[nx][ny] in [1,3,6,7]:
                            visited[nx][ny] = True
                            queue.append((nx,ny,time+1))
                            cnt+=1

        elif maps[x][y] == 2:   # 상 하
            for i in range(2):
                nx = two_dx[i]+x
                ny = two_dy[i]+y
                if two_dx[i] == -1 and two_dy[i] == 0: # 상
                    if 0<=nx<N and 0<=ny<M:
                        if not visited[nx][ny] and maps[nx][ny] in [1,2,5,6]:
                            visited[nx][ny] = True
                            queue.append((nx,ny,time+1))
                            cnt+=1
                elif two_dx[i] == 1 and two_dy[i] == 0: # 하
                    if 0<=nx<N and 0<=ny<M:
                        if not visited[nx][ny] and maps[nx][ny] in [1,2,4,7]:
                            visited[nx][ny] = True
                            queue.append((nx,ny,time+1))
                            cnt+=1
        
        elif maps[x][y] == 3:   # 좌 우
            for i in range(2):
                nx = three_dx[i]+x
                ny = three_dy[i]+y
                if three_dx[i] == 0 and three_dy[i] == -1: # 좌
                    if 0<=nx<N and 0<=ny<M:
                        if not visited[nx][ny] and maps[nx][ny] in [1,3,4,5]:
                            visited[nx][ny] = True
                            queue.append((nx,ny,time+1))
                            cnt+=1
                elif three_dx[i] == 0 and three_dy[i] == 1: # 우
                    if 0<=nx<N and 0<=ny<M:
                        if not visited[nx][ny] and maps[nx][ny] in [1,3,6,7]:
                            visited[nx][ny] = True
                            queue.append((nx,ny,time+1))
                            cnt+=1
        
        elif maps[x][y] == 4:   # 상 우
            for i in range(2):
                nx = four_dx[i]+x
                ny = four_dy[i]+y
                if four_dx[i] == -1 and four_dy[i] == 0: # 상
                    if 0<=nx<N and 0<=ny<M:
                        if not visited[nx][ny] and maps[nx][ny] in [1,2,5,6]:
                            visited[nx][ny] = True
                            queue.append((nx,ny,time+1))
                            cnt+=1
                elif four_dx[i] == 0 and four_dy[i] == 1: # 우
                    if 0<=nx<N and 0<=ny<M:
                        if not visited[nx][ny] and maps[nx][ny] in [1,3,6,7]:
                            visited[nx][ny] = True
                            queue.append((nx,ny,time+1))
                            cnt+=1
        
        elif maps[x][y] == 5:   # 하 우
            for i in range(2):
                nx = five_dx[i]+x
                ny = five_dy[i]+y
                if five_dx[i] == 1 and five_dy[i] == 0: # 하
                    if 0<=nx<N and 0<=ny<M:
                        if not visited[nx][ny] and maps[nx][ny] in [1,2,4,7]:
                            visited[nx][ny] = True
                            queue.append((nx,ny,time+1))
                            cnt+=1
                elif five_dx[i] == 0 and five_dy[i] == 1: # 우
                    if 0<=nx<N and 0<=ny<M:
                        if not visited[nx][ny] and maps[nx][ny] in [1,3,6,7]:
                            visited[nx][ny] = True
                            queue.append((nx,ny,time+1))
                            cnt+=1
        
        elif maps[x][y] == 6:   # 하 좌
            for i in range(2):
                nx = six_dx[i]+x
                ny = six_dy[i]+y
                if six_dx[i] == 1 and six_dy[i] == 0: # 하
                    if 0<=nx<N and 0<=ny<M:
                        if not visited[nx][ny] and maps[nx][ny] in [1,2,4,7]:
                            visited[nx][ny] = True
                            queue.append((nx,ny,time+1))
                            cnt+=1
                elif six_dx[i] == 0 and six_dy[i] == -1: # 좌
                    if 0<=nx<N and 0<=ny<M:
                        if not visited[nx][ny] and maps[nx][ny] in [1,3,4,5]:
                            visited[nx][ny] = True
                            queue.append((nx,ny,time+1))
                            cnt+=1
        
        elif maps[x][y] == 7:   # 상 좌 
            for i in range(2):
                nx = seven_dx[i]+x
                ny = seven_dy[i]+y
                if seven_dx[i] == -1 and seven_dy[i] == 0: # 상
                    if 0<=nx<N and 0<=ny<M:
                        if not visited[nx][ny] and maps[nx][ny] in [1,2,5,6]:
                            visited[nx][ny] = True
                            queue.append((nx,ny,time+1))
                            cnt+=1
                elif seven_dx[i] == 0 and seven_dy[i] == -1: # 좌
                    if 0<=nx<N and 0<=ny<M:
                        if not visited[nx][ny] and maps[nx][ny] in [1,3,4,5]:
                            visited[nx][ny] = True
                            queue.append((nx,ny,time+1))
                            cnt+=1

    print(f'#{t} {cnt}')
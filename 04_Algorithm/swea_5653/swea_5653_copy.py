import sys
sys.stdin = open("input.txt", "r")

'''
5653. [모의 SW 역량테스트] 줄기세포배양
https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWXRJ8EKe48DFAUo

 - 줄기세포들을 배양 용기에 도포한 후 일정 시간 동안 배양을 시킨 후 줄기 세포의 개수가 몇 개가 되는지 계산
 - 줄기 세포
    - 초기 상태에서 줄기 세포들은 비활성 상태이며 생명력 수치가 X인 줄기 세포의 경우 X시간동안 비활성 상태
    - X시간이 지나는 순간 활성 상태가 됨
    - 활성 상태가 되면 X 시간 동안 살아있을 수 있으며 X시간이 지나면 세포는 죽음
    - 죽은 상태로 해당 그리드 셀을 차지하게 됨

- 활성화된 줄기 세포는 첫 1시간 동안 상하좌우 네 방향으로 동시에 번식을 함, 번식된 줄기 세포는 비활성 상태
    - 델타 탐색

- 이미 줄기 세포가 존재하는 경우 번식하지 않음
    - 0일때만 번식함

- 두 개 이상의 줄기 세포가 하나의 그리드 셀에 동시 번식하려고 하는 경우 생명력 수치가 높은 줄기 세포가 해당 그리드 셀을 혼자 차지
    - 숫자가 높은 줄기세포로 덮어쓰기


[아이디어]
    - 줄기 세포를 저장할 때, 활성 상태인지, 비활성 상태인지, 죽었는지 체크가 필요함

    - 초마다 해야할 것
        - 비활성 세포 시간 증가
        - 활성세포 시간 증가 및 주변 증식
        - 활성세포 시간 달성 시 죽은 세포로 변환

    - 각각의 격자에 예를 들어 1,2,3의 인식표를 심어놓고 1은 비활성, 2는 활성, 3은 죽음이라고 표시
    - 한 격자에 들어가는 데이터(생명력, 경과 시간, 현재 상태) -> 딕셔너리로 저장

'''
T = int(input())
 
for tc in range(1, T+1):
    N, M, K = map(int, input().split()) # 세로, 가로, 시간
    board = [list(map(int, input().split())) for _ in range(N)]
 
    # 세포는 최대 K칸까지 퍼질 수 있으므로 맵을 크게 만듬
    row, col = N + 2*K + 2, M + 2*K + 2  # 확장된 접시 크기
    offset = K + 1  # 초기 세포를 중앙에 배치하기 위한 오프셋

    # 세포의 생명력을 저장하는 전체 배양 접시
    cell_map = [[0] * col for _ in range(row)]
 
    di = [-1, 1, 0, 0]
    dj = [0, 0, -1, 1]
 
    cells = []  # 현재 살아있는 세포 정보를 저장

    # 초기 세포를 확장된 맵 중앙에 배치
    for i in range(N):
        for j in range(M):
            x = board[i][j]  # 해당 위치의 생명력
            if x:
                r, c = i + offset, j + offset  # 확장된 맵에서의 위치
                cell_map[r][c] = x  # 맵에 생명력 기록
                cells.append([r, c, x, x, 1]) 
 
    for _ in range(K):
        new_cells = {}  # 이번 시간 번식 후보
        nxt = [] # 다음 상태 세포들
 
        for r, c, life, timer, status in cells:
            timer -= 1 # 시간 1 감소
 
            # 비활성 끝 -> 활성 시작
            if status == 2 and timer == life - 1:
                for a, b in zip(di, dj):
                    ni, nj = r + a, c + b
                    if cell_map[ni][nj] == 0:
                        prev = new_cells.get((ni, nj), 0)
                        if prev < life:
                            new_cells[(ni, nj)] = life
 
              
            if timer == 0:
                if status == 1: # 비활성 끝 -> 활성 시작
                    status = 2
                    timer = life
                else: # 활성 끝 -> 죽음
                    status = 0
 
            if status != 0:
                nxt.append([r, c, life, timer, status])
 
        for (nr, nc), n_life in new_cells.items():
            cell_map[nr][nc] = n_life
            nxt.append([nr, nc, n_life, n_life, 1])
 
        cells = nxt
 
    print(f"#{tc} {len(cells)}")
    


    
    
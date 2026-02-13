import sys
sys.stdin = open('input.txt')


for _ in range(10):
    tc = int(input())
    data = [list(map(int, input().split())) for _ in range(100)]
    result = 0

    # 모든 좌표 y에 대해
    for start in range(100):
        x = 0   # 초기 row 0으로 초기화
        y = start # 초기 col start 지점으로 초기화
        # 사다리 시작지점 이라면
        if data[x][y] == 1:
            # 가장 아래에 도달할 때 까지
            while x < 99:   # 마지막 좌표에서 결정지을 것이므로 x가 98일때까지 다음 칸 진행
                # 오른쪽 좌표가
                ny = y + 1
                # 범위를 벗어나지 않고, 이동 가능하다면
                if ny < 100 and data[x][ny] == 1:
                    y = ny  # y를 갱신하고
                    continue    # 아래 코드를 실행하지 않고 넘어가기
                # 그 외에는 항상 아래로만 진행 (사다리가 끊긴적 없으므로)
                # 위에서 끝나지 않았다면 왼쪽을 확인
                ny = y - 1
                # 위와 같지만 방향만 바꿔 진행
                if 0 <= ny and data[x][ny] == 1:
                    y = ny
                    continue
                x += 1
                # 만약 그 아래가 2라면
                if data[x][y] == 2:
                    result = start  # 시작지점으로 초기화

    ...

    '''
        지금 상황대로라면...
        1 0 0 1
        1 1 1 1 <- 여기서 오른쪽 한번, 왼쪽 한번 왔다갔다 반복하게 된다.
        1 0 0 1
        
        이 상황을 해결하려면...?
        오른쪽이든 왼쪽이든 한 번 갈수 있다면 끝까지 가도록 한다.
        그럼 오른쪽으로 계속 가도록
            조건은? data[x][ny]가 1이면... 계속 while문?
        그것만으로 해결이 되나?
            안된다. 오른쪽 끝으로 가도록 한 다음 다음 코드 실행하면
            다시 왼쪽 끝으로 갈것..
        
        그럼 한쪽 방향으로 횡이동을 마치면 x가 1 증가 하도록 한다.
        
        코드가... 복잡해진다!
        문제를 풀기 시작할떄 예상못한 상황을 발견했으니, 다시 고려해서 풀어보자
    '''
    print(f'#{tc} {result}')

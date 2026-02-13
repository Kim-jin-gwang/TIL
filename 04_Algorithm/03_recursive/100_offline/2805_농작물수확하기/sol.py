import sys
sys.stdin = open('input.txt')


T = int(input())

for tc in range(1, T+1):
    N = int(input())  # 정사각형 한 변의 길이 입력
    arr = [list(map(int, input())) for _ in range(N)]  # 2차원 배열 입력
    result = 0  # 결과 합 초기화

    for i in range(N):  # 각 행마다
        if i <= N//2:
            # 중앙행(N//2)까지는 마름모의 윗부분 및 중심.
            # 예를 들어 N=5일 때,
            # i=0:       arr[0][2:3]                -> 가운데 1개 (0 1 [2] 3 4)
            # i=1:    arr[1][1:4]                   -> 가운데부터 좌우 1칸씩 확장
            # i=2: arr[2][0:5]                      -> 전체 (최대)
            # 슬라이싱: (N//2-i) ~ (N//2+i+1)로 범위 확장
            result += sum(arr[i][N//2-i:N//2+i+1])
        else:
            # 중앙행 아래는 마름모 아랫부분.
            # 즉, 아래로 갈수록 범위가 줄어듦
            # 예) N=5, i=3: (N//2-(N-1-i))~(N//2+(N-1-i)+1)
            # i=3: arr[3][1:4]    i=4: arr[4][2:3]
            # 점점 범위가 좁아짐
            result += sum(arr[i][N//2-(N-1-i):N//2+(N-1-i)+1])

    print(f'#{tc} {result}')  # 결과 출력
'''
    ㅋㅋㅋㅋ 
'''

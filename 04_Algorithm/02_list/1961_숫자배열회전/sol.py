import sys
sys.stdin = open('input.txt')


T = int(input())

for tc in range(1, T + 1):
    # 길이 N
    N = int(input())
    data = [list(input().split()) for _ in range(N)]

    # 각도별 결과를 담을 배열
    result_90 = [[''] * N for _ in range(N)]
    result_180 = [[''] * N for _ in range(N)]
    result_270 = [[''] * N for _ in range(N)]

    # 전체 범위를 순회하여
    for i in range(N):
        for j in range(N):
            '''
                2차원 배열이 다음과 같을떄
                  0 1 2 3 
                0 a b c d
                1 e f g h
                2 i j k l
                3 m n o p

                90도 회전한 결과는
                  0 1 2 3
                0 m i e a
                1 n j f b
                2 o k g c
                3 p l h d

                원본과 90도 회전의 인덱스 차이는
                e의 경우,
                원본: (1, 0)
                90도 회전: (0, 2)

                f의 경우,
                원본: (1, 1)
                90도 회전: (1, 2)

                g의 경우,
                원본: (1, 2)
                90도 회전: (2, 2)

                ...

                즉, (i, j) -> (j, N-1-i) 로 바뀜

                90도 회전: (i, j) -> (j, N-1-i)
                180도 회전: (i, j) -> (N-1-i, N-1-j)
                270도 회전: (i, j) -> (N-1-j, i)
            '''
            result_90[j][N - 1 - i] = data[i][j]
            result_180[N - 1 - i][N - 1 - j] = data[i][j]
            result_270[N - 1 - j][i] = data[i][j]
    # 출력
    print(f'#{tc}')

    # 각 2차원 배열의 첫번째 행을 공백을 기준으로 출력
    for i in range(N):
        print(''.join(result_90[i]), ''.join(result_180[i]), ''.join(result_270[i]))
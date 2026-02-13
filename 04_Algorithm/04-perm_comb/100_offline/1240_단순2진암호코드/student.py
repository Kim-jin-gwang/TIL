t = int(input())


# 암호값 저장
def check_pass(arr):
    if arr == [0, 0, 0, 1, 1, 0, 1]:
        return 0
    elif arr == [0, 0, 1, 1, 0, 0, 1]:
        return 1
    elif arr == [0, 0, 1, 0, 0, 1, 1]:
        return 2
    elif arr == [0, 1, 1, 1, 1, 0, 1]:
        return 3
    elif arr == [0, 1, 0, 0, 0, 1, 1]:
        return 4
    elif arr == [0, 1, 1, 0, 0, 0, 1]:
        return 5
    elif arr == [0, 1, 0, 1, 1, 1, 1]:
        return 6
    elif arr == [0, 1, 1, 1, 0, 1, 1]:
        return 7
    elif arr == [0, 1, 1, 0, 1, 1, 1]:
        return 8
    elif arr == [0, 0, 0, 1, 0, 1, 1]:
        return 9


for tc in range(t):
    n, m = (map(int, input().split()))
    mat = []
    for _ in range(n):
        line = input().strip()  # 줄바꿈 제거 후 읽기
        row = [int(ch) for ch in line]  # 문자열을 int로 바꿔 읽어오기
        mat.append(row)

    password_line = []

    # 암호가 포함된 첫번째 행을 password_line에 저장
    for i in range(n):
        for j in range(m):
            if mat[i][j] == 1:
                word = mat[i][:]
                password_line.append(word)
                break
    # 모든 암호는 1로 끝나므로 배열을 뒤집얼 저장
    password_line = password_line[0][-1::-1]
    count = 0
    # 뒤집은 배열에서 1이 시작하는 인덱스 값을 저장
    idx = password_line.index(1)
    # 해당 인덱스를 기준으로 56번째 까지 배열 저장
    password = password_line[idx:idx + 56]
    # 원래 배열의 상태로 뒤집기
    password = password[-1::-1]
    real_pass = []
    check = []
    for i, p in enumerate(password):
        i += 1
        check.append(p)
        if i % 7 == 0:
            real_pass.append(check_pass(check))
            check = []
    result = 0
    for i, r in enumerate(real_pass):
        i += 1
        if i % 2 == 0:
            result += r
        else:
            result += r * 3

    if result % 10 == 0:
        print(f'#{tc + 1} {sum(real_pass)}')
    else:
        print(f'#{tc + 1} {0}')
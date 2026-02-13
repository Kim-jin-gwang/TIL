import sys
sys.stdin = open('input.txt')

def search(x, y):
    """
    주어진 위치에서 M개의 연속된 벌통에서 얻을 수 있는 최대 수익을 계산
    
    Args:
        x (int): 시작 행 위치
        y (int): 시작 열 위치
    
    Returns:
        tuple: (최대 수익, 사용된 위치 리스트)
    """
    now_set = data[x][y:y+M]
    case = sum(map(lambda x: x*x, now_set))

    def perm(arr, r, cnt, acc):
        """
        순열을 이용해 C 이하의 꿀로 최대 수익을 구하는 함수
        
        Args:
            arr (list): 현재 벌통 배열
            r (int): 현재 순열 인덱스
            cnt (int): 현재까지 선택한 꿀의 총량
            acc (int): 현재까지 얻은 수익 (꿀^2의 합)
        """
        nonlocal case
        # 꿀의 총량이 C를 넘으면 가지치기
        if cnt > C:
            acc -= arr[r-1] * arr[r-1]
            if acc > case:
                case = acc
            return

        # 모든 벌통을 확인했으면 최대값 갱신
        if r == M:
            if acc > case:
                case = acc
            return
        else:
            # 순열을 통해 모든 경우의 수 확인
            for i in range(r, M):
                item = arr[i]
                arr[i], arr[r] = arr[r], arr[i]
                perm(arr, r+1, cnt+item, acc+item*item)
                arr[i], arr[r] = arr[r], arr[i]
                
    acc = sum(now_set)
    # 전체 꿀의 합이 C를 넘으면 순열로 부분집합 찾기
    if acc > C:
        case = 0
        perm(data[x][y:y+M], 0, 0, 0)
    return case, list(zip([x]*M, range(y, y+M)))


T = int(input())

for tc in range(1, T+1):
    # N: 벌통 크기, M: 선택할 수 있는 벌통의 개수, C: 꿀을 채취할 수 있는 최대 양
    N, M, C = map(int, input().split())
    data = [list(map(int, input().split())) for _ in range(N)]
    result = 0  # 최대 수익을 저장할 변수

    # 모든 가능한 M개 연속 구간의 최대 수익을 계산하여 리스트에 저장
    acc_list = []
    for i in range(N):
        for j in range(N-M+1):
            acc_list.append(search(i, j))
    
    # 수익이 높은 순으로 정렬
    acc_list.sort(reverse=True)
    n = len(acc_list)

    # 두 구간이 겹치지 않으면서 최대 수익을 가지는 조합 찾기
    for i in range(n - 1):
        for j in range(i+1, n):  # j는 i+1부터 시작 (중복 방지)
            a, b = acc_list[i], acc_list[j]
            set_a, set_b = set(a[1]), set(b[1])
            sum_val = a[0] + b[0]
            # 두 구간이 겹치지 않으면 결과 갱신
            if not set_a & set_b and sum_val > result:
                result = sum_val
    print(f'#{tc} {result}')

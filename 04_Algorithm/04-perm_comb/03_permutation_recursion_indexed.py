def perm_no_slice(arr, start_idx):
    '''
    Args:
        arr: 순열을 만들 원본 리스트 (여기서는 변경 가능)
        start_idx: 현재 순열을 만들고 있는 시작 인덱스
    '''
    if start_idx == 1:
        print(arr)
        return
    # 시작 인덱스부터, 끝까지
    for idx in range(start_idx, len(arr)):
        # 현재 위치 idx와 시작 위치 start_idx의 값을 서로 위치를 변경
        arr[start_idx], arr[idx] = arr[idx], arr[start_idx]
        perm_no_slice(arr, start_idx + 1)
        arr[start_idx], arr[idx] = arr[idx], arr[start_idx]


# 사용 예시
my_list = [1, 2, 3]
perm_no_slice(my_list, 0)
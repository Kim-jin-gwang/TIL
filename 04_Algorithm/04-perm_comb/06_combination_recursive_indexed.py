def combinations(arr, r, current_comb, start_idx):
    if len(current_comb) == r:
        print(current_comb)
        return

    # 쓸데없는 조사 안하도록 하기...

    for idx in range(start_idx, len(arr)):
        current_comb.append(arr[idx])
        combinations(arr, r, current_comb, idx+1)
        current_comb.pop()
# 사용 예시
my_list = [1, 2, 3, 4]
r = 3 # 3개의 요소를 선택하는 조합

# 함수를 호출할 때는 초기 상태를 전달
# 빈 리스트 []는 현재 선택된 요소가 없음을 의미
# 0은 arr의 첫 번째 인덱스부터 탐색을 시작함을 의미
combinations(my_list, r, [], 0)
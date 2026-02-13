permutaion_list = []
count = 0
def perm(selected, remain):
    global count
    count += 1
    '''
    Args:
        selected: 선택된 값 목록
        reamin: 선택되지 않고 남은 값 목록 
    '''
    if not remain: # 남은 요소가 없을때 까지
        # 만들어진 순열 출력
        print(selected)
        permutaion_list.append(selected)
    else:   # 아니면 -> 유도부분
        # remain 리스트의 요소들을 하나씩 빼서, selected에 삽입
        for idx in range(len(remain)):
            selected_elem = remain[idx]
            remain_list = remain[:idx] + remain[idx+1:]
            perm(selected + [selected_elem], remain_list)

            # selected.append(remain.pop(idx)) # 선택된 요소
        
        

# 초기 호출로 빈 리스트와 [1, 2, 3] 리스트 사용
perm([], [1, 2, 3])
print(permutaion_list)
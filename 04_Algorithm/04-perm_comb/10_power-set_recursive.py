def create_subset(depth, included):
    '''
     Args:
        depth: 현재 깊이 (처리 중인 요소의 인덱스)
        included: 각 요소가 부분 집합에 포함되는지 여부를 나타내는 불리언 리스트
    '''
    if depth == len(arr):
        cnt_subset = []
        for i in range(len(arr)):
            if included[i] == 1:
                cnt_subset.append(arr[i])
        subsets.append(cnt_subset)
        return

    included[depth] = 0
    create_subset(depth + 1, included)

    included[depth] = 1
    create_subset(depth + 1, included)

    
arr = [1, 2, 3] # 부분 집합을 생성할 입력 리스트
subsets = [] # 모든 부분 집합을 저장할 리스트
init_included = [0] * len(arr) # 각 요소의 포함 여부를 저장할 리스트 초기화
create_subset(0, init_included) 
print(subsets)
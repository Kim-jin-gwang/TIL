import sys
sys.stdin = open("input.txt", "r")


import heapq  # 최소힙 구현하는 함수 -> 이 문제는 최대힙 구현해야 함

T = int(input())
for t in range(1,T+1):
    N = int(input())

    heap_arr = []
    ans = []
    for _ in range(N):
        cal_heap = list(map(int,input().split()))
        if cal_heap[0] == 1:
            heapq.heappush(heap_arr, -cal_heap[1])
        elif cal_heap[0] == 2:
            if not heap_arr:
                ans.append(-1)
            else:
                ans.append(-heapq.heappop(heap_arr))
    
    print(f'#{t}',*ans)

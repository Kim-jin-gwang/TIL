import sys
sys.stdin = open("input.txt", "r")

'''
- 직원들의 번호가 1부터 N까지 매겨져 있고, 해야 할 일에도 번호가 1부터 N까지 매겨져 있을 때, 
- i번 직원이 j번 일을 하면 성공할 확률이 Pi, j이다.
- "주어진 일이 모두 성공할 확률”의 최댓값을 구하는 프로그램을 작성"

- 완탐으로 task 순회
- idx가 N이 되면 돌아가기
'''

def Search(task, N, visited, idx, cur):
    global ans
    if idx == N:
        ans = max(ans, cur)
        return
    
    if cur <= ans:
         return
    
    for i in range(N):
        if not visited[i] and task[idx][i] != 0:
                success_percent = task[idx][i] / 100
                visited[i] = True
                Search(task, N, visited, idx+1, cur*success_percent)
                visited[i] = False



T = int(input())
for t in range(1,T+1):
    N = int(input())
    task = []
    for _ in range(N):
        task.append(list(map(int,input().split())))
    
    ans = 0
    visited = [False] * N
    Search(task, N, visited, 0, 1)

    print(f'#{t} {ans*100:.6f}')
import sys
sys.stdin = open("input.txt", "r")

'''
swea_2105. [모의 SW 역량테스트] 디저트 카페
https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV5VwAr6APYDFAWu

- 한 변의 길이가 N인 정사각형 모양을 가진 지역에 디저트 카페가 보여 있음
- 격자 안의 숫자는 해당 디저트 카페에서 팔고 있는 디저트의 종류를 의미
- 카페들 사이에는 대각선 방향으로 움직을 수 있는 길들이 있음
- 디저트 카페 투어는 어느 한 카페에서 출발하여 대각선 방향으로 움직이고 사각형 모양을 그리며 출발한 카페로 와야함

- 카페 투어 중 같은 숫자의 디저트를 팔고 있는 카페가 있으면 안됨
- 하나의 카페에서 디저트를 먹는 것도 안됨
- 왔던 길을 다시 돌아가는 것도 안됨

- 디저트를 가장 많이 먹을 수 있는 경로를 찾고 그 때의 디저트 수를 정답으로 출력
- 디저트를 먹을 수 없는 경우 -1 출력


[제약사항]
1. 시간제한 : 최대 50개 테스트 케이스를 모두 통과하는 데 C/C++/Java 모두 3초
2. 디저트 카페가 모여있는 지역의 한 변의 길이 N은 4 이상 20 이하의 정수이다. (4 ≤ N ≤ 20)
3. 디저트 종류를 나타나는 수는 1 이상 100 이하의 정수이다.

[아이디어]
1. 델타 탐색을 대각선으로 하기
2. dfs로 탐색하기
    - 사각형이 되려면 어떻게 방향을 만들어야 할지 생각해야 함 -> 그냥 완탐 돌리면 되는거 아닌가 어차피 알아서 제약 걸릴듯
3. 가지치기
    - 같은 숫자를 만났을 때 -> 디저트를 먹을 수 없는 경우
4. 종료 조건
    - 시작지점으로 돌아왔을 때

'''

# 순서 : ↘ ↙ ↖ ↗, dir은 사각형을 만들기 위한 제약조건
dx = [1,1,-1,-1]
dy = [1,-1,-1,1]
def cafe_tour(x,y,cnt,target,dir):
    global ans

    for i in range(dir, 4):
        nx = x + dx[i]
        ny = y + dy[i]

        if nx == target[0] and ny == target[1] and cnt >= 4:
            ans = max(ans, cnt)
            return
        
        
        if 0<=nx<N and 0<=ny<N:
            if not visited[nx][ny] and cafe[nx][ny] not in eaten:
                visited[nx][ny] = True
                eaten.add(cafe[nx][ny])

                cafe_tour(nx,ny,cnt+1,target,i)

                visited[nx][ny] = False
                eaten.remove(cafe[nx][ny])


T = int(input())
for t in range(1,T+1):
    N = int(input())
    cafe = [list(map(int,input().split())) for _ in range(N)]
    visited = [[False] * N for _ in range(N)]

    ans = -1
    for i in range(N):
        for j in range(N):
            eaten = set()
            eaten.add(cafe[i][j])
            visited = [[False] * N for _ in range(N)]
            visited[i][j] = True
            target = [i,j]
            cafe_tour(i, j, 1, target,0)

    print(f'#{t} {ans}')
#import sys

#sys.stdin = open("input.txt", "r")

'''
1. start에 시작지점 x좌표 저장
2. 1로 내려가다가 꺾는 지점이 있으면 꺾기
    - 일단 한칸 내려감.
    - if 내려갔을 때 좌 혹은 우에 길이 있으면 그쪽으로 이동
    - 더 이상 옆쪽으로 갈 수 있는 길이 없으면 다시 아래로 내려가기
3. 도착지점이 2이면 return

- dx dy를 아래 좌 우만 하면 되나?
    - 기본 아래 (dx=0, dy=1)
    - 오른쪽 만나면 (dx=1, dy=0)
    - 왼쪽 만나면 (dx=-1,dy=0)
- 꺾이는 지점을 어떻게 표시? - flag = true / false ?
    -굳이 flag 해야하는지 확인
    -그냥 꺾이면 dx랑 dy만 바꾸면 되지 않나?


그러지 말고 2를 찾아서 거꾸로 올라가기
- 
'''

for _ in range(10):
    T = int(input())
    ladder = [list(map(int,input().split())) for _ in range(100)]
    start_y = 0

    for i in range(100):
        if ladder[99][i] == 2:
            start_y = i
            break

    def dfs(x,y,status):
        if x == 0:
            return y

        if status == 'up':
            for i in [1, -1]:
                ny = y+i
                if 0<=ny<100 and ladder[x][ny] == 1:
                    if i == 1:
                        return dfs(x,ny,'right')
                    elif i == -1:
                        return dfs(x,ny,'left')
            return dfs(x-1,y,'up')

        elif status == 'right':
            ny = y+1
            if ny>=100 or ladder[x][ny] == 0:
                if x == 0:
                    return y
                return dfs(x-1, y, 'up')
            return dfs(x, ny, 'right')

        elif status == 'left':
            ny = y-1
            if ny < 0 or ladder[x][ny] == 0:
                if x == 0:
                    return y
                return dfs(x - 1, y, 'up')
            return dfs(x, ny, 'left')

    ans = dfs(99,start_y,'up')
    print(f'#{T} {ans}')
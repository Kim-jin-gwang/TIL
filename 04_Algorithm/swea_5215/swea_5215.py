import sys
sys.stdin = open("input.txt", "r")


def search(idx,score_cur,cal_cur):
    global ans
    if cal_cur > L:
        return
    
    if idx == N:
        ans = max(ans,score_cur)
        return
    
    search(idx+1, score_cur+foods_info[idx][0], cal_cur+foods_info[idx][1])
    search(idx+1, score_cur, cal_cur)



T = int(input())
for t in range(1,T+1):
    N,L = map(int,input().split())
    foods_info = []
    for _ in range(N):
        score,cal = map(int,input().split())
        foods_info.append([score,cal])
    ans = 0
    search(0,0,0)

    print(f'#{t} {ans}')
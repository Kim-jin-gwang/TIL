import sys
sys.stdin = open("input.txt", "r")


def dfs(cnt,s_table):
    global ans
    if cnt == 0:
        cur = int(''.join(s_table))
        ans = max(ans,cur)
        return

    # 모든 자리 쌍 탐색
    for i in range(0,len(s_table)-1):
        for j in range(i+1,len(s_table)):
            s_table[i], s_table[j] = s_table[j], s_table[i]
            #print(s_table)
            state = (''.join(s_table), cnt-1)  # 바꾼 후의 문자열을 미리 확인
            if state not in visited: # 바꾼 후의 문자열이 방문 안한 문자열이면
                visited.add(state)
                dfs(cnt-1, s_table) # 바꿔버리기
            #print(visited)
            s_table[j], s_table[i] = s_table[i], s_table[j]

T = int(input())
for t in range(1,T+1):

    score_table, change = input().split()
    score_table = list(str(score_table))
    change = int(change)

    ans = 0
    visited = set()

    dfs(change,score_table)
    print(f'#{t} {ans}')
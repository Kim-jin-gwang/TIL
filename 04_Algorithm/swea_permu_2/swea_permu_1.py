import sys
from itertools import combinations

sys.stdin = open("input.txt", "r")

def Synerge(arr, food):
    res = 0
    for t1,t2 in combinations(food,2):
        res += arr[t1][t2] + arr[t2][t1]
    return res


T = int(input())
for t in range(1,T+1):
    N = int(input())
    foods = [list(map(int,input().split())) for _ in range(N)]
    ans = 1000001
    food_list = list(range(N))

    for first_food in combinations(food_list,N//2):
        first_food = set(first_food)
        second_food = set(food_list) - first_food
        first_score = Synerge(foods, first_food)
        second_score = Synerge(foods, second_food)

        ans = min(ans,abs(first_score-second_score))
    print(f'#{t} {ans}')








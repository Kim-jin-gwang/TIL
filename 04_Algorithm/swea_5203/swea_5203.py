import sys
sys.stdin = open("input.txt", "r")

T = int(input())
for t in range(1,T+1):
    ans = 0
    cards = list(map(int,input().split()))  #p1이 홀수번째 숫자(인덱스는 짝수) 가져감
    cnt_p1 = [0] * len(cards)
    cnt_p2 = [0] * len(cards)

    for i in range(len(cards)):
        card = cards[i]

        # p1 
        if i%2 == 0:         # p1이 홀수번째 숫자이지만 인덱스는 짝수
            cnt_p1[card] += 1
            
            # triplet 체크(같은 숫자가 3개 이상)
            if cnt_p1[card] >= 3:
                ans = 1
                break

            # run 체크(연속인 숫자가 3개 이상) (x-2,x-1,x)  (x-1,x,x+1)  (x,x+1,x+2) 
            if card <= 7 and cnt_p1[card+1] >= 1 and cnt_p1[card+2] >= 1:
                ans = 1
                break
            if card >= 2 and  cnt_p1[card-2] >= 1 and cnt_p1[card-1] >= 1:
                ans = 1
                break
            if 1<=card<=8 and  cnt_p1[card-1] >= 1 and cnt_p1[card+1] >= 1:
                ans = 1
                break
        
        # p2
        elif i%2 == 1:       # p2의 인덱스는 홀수
            cnt_p2[card] += 1

            # triplet 체크(같은 숫자가 3개 이상)
            if cnt_p2[card] >= 3:
                ans = 2
                break
        
            # run 체크(연속인 숫자가 3개 이상) (x-2,x-1,x)  (x-1,x,x+1)  (x,x+1,x+2) 
            if card <= 7 and cnt_p2[card+1] >= 1 and cnt_p2[card+2] >= 1:
                ans = 2
                break
            if card >= 2 and  cnt_p2[card-2] >= 1 and cnt_p2[card-1] >= 1:
                ans = 2
                break
            if 1<=card<=8 and  cnt_p2[card-1] >= 1 and cnt_p2[card+1] >= 1:
                ans = 2
                break


    
    print(f'#{t} {ans}')
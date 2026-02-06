#import sys
#sys.stdin = open("input.txt", "r")


'''
- 가로 길이는 무조건 56
- 올바른 암호코드 = (홀수 합 * 3) + (짝수 합) == 10의 배수

1. 배열 중 암호코드의 위치를 찾아야 함
2. 한줄씩 입력받아서 그 줄에 1이 있으면 암호코드임.

'''

password = ['0001101','0011001','0010011','0111101','0100011'
    ,'0110001','0101111','0111011','0110111','0001011']

T = int(input())
for t in range(1,T+1):
    N,M = map(int,input().split())
    code = ''

    for _ in range(N):
        line = input().strip()
        if '1' in line:
            code = line

    last = code.rfind('1')
    arr = code[last-55:last+1]

    token = []
    for i in range(0,56,7):
        part = arr[i:i+7]
        if part in password:
            token.append(password.index(part))

    even = token[1] + token[3] + token[5] + token[7]
    odd = token[0] + token[2] + token[4] + token[6]

    if (even+(odd*3)) % 10 == 0:
        print(f'#{t} {even+odd}')
    else:
        print(f'#{t} 0')




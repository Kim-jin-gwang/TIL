coins = [1, 5, 10, 50, 100, 500]  # 동전 종류
change = 882  # 잔돈

# 아래의 경우라면 어떨까?
# coins = [1, 5, 10, 50, 100, 400, 500]  # 동전 종류
# change = 882  # 잔돈

result = get_minimum_coins(coins, change)
for coin, count in result.items():
    print(f"{coin}원: {count}개")

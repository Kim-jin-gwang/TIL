def coin_change(coins, amount):
    # 0원 1원 2원 3원 4원 5원 6원... n원을 해결하는 최적해 메모
    # 초기화당시엔, 최악의 상황을 고려해서 작성
    dp = list(range(amount + 1))

    # 1원부터 amount까지 갱신
    for i in range(1, amount + 1):
        # 내가 가진 동전 체계
        for coin in coins:
            # 이 coin 가치가, 내가 지금 해결하려는 금액 i보다
            # 작아야 한다.
            if coin <= i:
                # 내가 이전에 dp[i] 번째에 할당한 최적해가
                # 이번 coin을 사용함으로써 얻을 수 있는 최적해와
                # 비교해서 더 작은 값이 진짜 dp[i]번째의 최적해
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount]

coins = [1, 4, 6]  # 사용 가능한 동전의 종류
amount = 8  # 만들어야 할 금액

print(coin_change(coins, amount))

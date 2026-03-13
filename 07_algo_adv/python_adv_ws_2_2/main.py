import numpy as np


def filter_valid_prices(prices, min_price, max_price):
    """유효 구간 가격만 유지하고 나머지는 0으로 대체한다."""

    if prices.ndim != 1:
        raise ValueError
    
    if min_price > max_price:
        raise ValueError
    
    if prices.size == 0:
        return prices
    
    prices[(prices < min_price) | (prices > max_price)] = 0
    return prices



def main():
    prices = np.array([500, 1200, 50, 3300, 1800], dtype=float)
    print(filter_valid_prices(prices, 200, 2000))


if __name__ == '__main__':
    main()

import numpy as np


def clean_order_prices(prices):

    if prices.size == 0:
        return {
            'cleaned_prices' : [],
            'avg_price' : float(0.0),
        }
    
    cleaned_price = prices.copy()
    cleaned_price[cleaned_price < 0] = 0

    avg_price = np.mean(cleaned_price)

    return {
        'cleaned_prices' : cleaned_price,
        'avg_price' : float(avg_price),
    }


def main():
    prices = np.array([12000, -3000, 9000, 15000, -1000], dtype=float)
    result = clean_order_prices(prices)
    print(result)


if __name__ == '__main__':
    main()

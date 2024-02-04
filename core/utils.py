def get_change_in_fewest_coins(change: int):
    coins = (100, 50, 20, 10, 5)
    change_distribution = {}

    for coin in coins:
        if change >= coin:
            num_coins = change // coin
            change -= num_coins * coin
            change_distribution[coin] = f"{num_coins} coins"
            if change == 0:
                break
    return change_distribution

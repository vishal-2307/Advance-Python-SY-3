import timeit
import random

def knapsack_brute_force(weights, values, capacity, n=None):
    if n is None:
        n = len(weights)

    if n == 0 or capacity == 0:
        return 0

    if weights[n - 1] > capacity:
        return knapsack_brute_force(weights, values, capacity, n - 1)

    take = values[n - 1] + knapsack_brute_force(
        weights, values, capacity - weights[n - 1], n - 1
    )

    skip = knapsack_brute_force(
        weights, values, capacity, n - 1
    )

    return max(take, skip)


def knapsack_top_down(weights, values, capacity):
    n = len(weights)
    memo = {}

    def solve(i, capacity):
        if i == 0 or capacity == 0:
            return 0

        if (i, capacity) in memo:
            return memo[(i, capacity)]

        if weights[i - 1] > capacity:
            result = solve(i - 1, capacity)
        else:
            take = values[i - 1] + solve(
                i - 1, capacity - weights[i - 1]
            )
            skip = solve(i - 1, capacity)
            result = max(take, skip)

        memo[(i, capacity)] = result
        return result

    return solve(n, capacity)


def build_knapsack_table(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] > w:
                dp[i][w] = dp[i - 1][w]
            else:
                skip = dp[i - 1][w]
                take = values[i - 1] + dp[i - 1][w - weights[i - 1]]
                dp[i][w] = max(skip, take)

    return dp


def find_selected_items(dp, weights, capacity):
    selected = []
    n = len(weights)
    w = capacity

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= weights[i - 1]

    selected.reverse()
    return selected


def knapsack_bottom_up(weights, values, capacity):
    dp = build_knapsack_table(weights, values, capacity)
    maximum_value = dp[len(weights)][capacity]
    selected = find_selected_items(dp, weights, capacity)

    return maximum_value, selected, dp


if __name__ == "__main__":
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 5

    print("Items:", list(zip(weights, values)))
    print("Knapsack Capacity:", capacity)

    brute_result = knapsack_brute_force(weights, values, capacity)
    print("\n1. Brute Force:", brute_result)

    top_down_result = knapsack_top_down(weights, values, capacity)
    print("2. Top-Down:", top_down_result)

    maximum_value, selected, dp = knapsack_bottom_up(
        weights, values, capacity
    )

    print("3. Bottom-Up:", maximum_value)
    print("Selected Items:", selected)

    for index in selected:
        print(
            "Item", index,
            ": Weight =", weights[index],
            ", Value =", values[index]
        )

    assert brute_result == maximum_value
    assert top_down_result == maximum_value

    print("\nAll three methods give the same result.")

    random.seed(42)

    n = 22
    large_weights = [random.randint(1, 15) for _ in range(n)]
    large_values = [random.randint(1, 20) for _ in range(n)]
    large_capacity = 50

    brute_time = timeit.timeit(
        lambda: knapsack_brute_force(
            large_weights, large_values, large_capacity
        ),
        number=1
    )

    bottom_up_time = timeit.timeit(
        lambda: knapsack_bottom_up(
            large_weights, large_values, large_capacity
        ),
        number=1
    )

    print("\nPerformance Comparison")
    print("Brute Force Time:", round(brute_time, 5), "seconds")
    print("Bottom-Up Time:", round(bottom_up_time, 8), "seconds")
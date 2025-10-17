from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        total_profit = 0

        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:
                total_profit += prices[i] - prices[i - 1]

        return total_profit


if __name__ == "__main__":
    prices = [7, 1, 5, 3, 6, 4]

    solution = Solution()
    print(solution.maxProfit(prices))  # Output: 7

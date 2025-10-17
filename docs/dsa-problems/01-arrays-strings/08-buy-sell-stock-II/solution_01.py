from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        total_profit = 0
        local_max = prices[0]
        local_min = prices[0]

        for i in range(1, len(prices)):
            if prices[i] < prices[i - 1]:
                total_profit += local_max - local_min

                local_max = prices[i]
                local_min = prices[i]
            elif prices[i] > local_max:
                local_max = prices[i]

        total_profit += local_max - local_min

        return total_profit


if __name__ == "__main__":
    prices = [7, 1, 5, 3, 6, 4]

    solution = Solution()
    print(solution.maxProfit(prices))  # Output: 7

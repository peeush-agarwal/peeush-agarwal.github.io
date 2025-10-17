from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit = 0

        for i in range(len(prices)):
            for j in range(i+1, len(prices)):
                max_profit = max(max_profit, prices[j] - prices[i])
        
        return max_profit


if __name__ == "__main__":
    solution = Solution()

    prices = [7,1,5,3,6,4]
    print(solution.maxProfit(prices))  # Output: 5

    prices = [7,6,4,3,1]
    print(solution.maxProfit(prices))  # Output: 0

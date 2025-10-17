# Intuition

If you can buy and sell as many times as you want, the optimal strategy is to take every increase: buy before every rise and sell at the peak. This means you simply sum up all positive price differences between consecutive days.

# Approach

Iterate through the price list. For each day, if the price is higher than the previous day, add the difference to the total profit. This greedy approach ensures you capture all possible gains from every upward movement, effectively simulating buying before every rise and selling at every peak.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(1)$$

# Code

```python
from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        total_profit = 0
        # Iterate through the price list, starting from the second day
        for i in range(1, len(prices)):
            # If today's price is higher than yesterday's, add the difference
            if prices[i] > prices[i - 1]:
                total_profit += prices[i] - prices[i - 1]
        return total_profit
```

[Back to Problem Statement](./index.md)

# Intuition

The goal is to maximize profit when you can make as many transactions as you like (buy then sell, multiple times). Every increasing adjacent pair of days contributes profit equal to the difference between the later and earlier price. Summing all such positive differences yields the maximum profit. Another equivalent view is to capture each ascending segment's valley-to-peak gain and sum them.

# Approach

Traverse the prices once, tracking the start (local_min) and current peak (local_max) of an ascending segment. When the price drops compared to the previous day, add the profit of the finished segment (local_max - local_min) to the total and start a new segment. At the end add the last segment's profit. This greedy approach effectively captures all gains from every upward movement.

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
        # Handle trivial case: no profit possible with fewer than 2 days
        if not prices or len(prices) < 2:
            return 0

        total_profit = 0
        # Initialize local_min and local_max to the first day's price
        local_min = prices[0]
        local_max = prices[0]

        # Iterate through prices starting from day 2
        for i in range(1, len(prices)):
            # If price drops compared to previous day, we close the current segment
            if prices[i] < prices[i - 1]:
                # Add profit from the previous ascending segment (if any)
                total_profit += local_max - local_min
                # Start a new segment at the current (lower) price
                local_min = prices[i]
                local_max = prices[i]
            else:
                # If price goes up and exceeds current local_max, extend the peak
                if prices[i] > local_max:
                    local_max = prices[i]

        # Add profit from the final ascending segment
        total_profit += local_max - local_min

        return total_profit
```

[Back to Problem Statement](./index.md)

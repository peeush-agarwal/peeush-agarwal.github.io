# Intuition

The first idea that comes to mind is to try every possible pair of days: buy on one day and sell on another day after it, and keep track of the maximum profit. This brute-force approach checks all possibilities but is not efficient for large inputs.

# Approach

The provided solution uses a brute-force approach. It iterates through all pairs of days `(i, j)` where `i < j`, calculates the profit for each pair as `prices[j] - prices[i]`, and keeps track of the maximum profit found. If no profit is possible (i.e., prices always decrease), it returns 0.

# Complexity

- Time complexity:
$$O(n^2)$$
Because for each day, it checks all following days, resulting in a nested loop.

- Space complexity:
$$O(1)$$
Only a constant amount of extra space is used for variables.

# Code

```python
from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit = 0

        for i in range(len(prices)):
            for j in range(i+1, len(prices)):
                max_profit = max(max_profit, prices[j] - prices[i])
        
        return max_profit
```

[Back to Problem Statement](./index.md)

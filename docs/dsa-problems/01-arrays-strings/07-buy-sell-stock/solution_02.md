# Intuition

Instead of checking every possible pair of days, we can keep track of the minimum price seen so far as we iterate through the list. For each day, we calculate the profit if we sold on that day (current price minus the minimum price so far) and update the maximum profit accordingly. This way, we only need a single pass through the array.

# Approach

- Initialize `max_profit` to 0 and `buy_price` to the first price in the list.
- Iterate through the prices starting from the second day.
    - For each price, calculate the profit if we sold on that day: `prices[i] - buy_price`.
    - Update `max_profit` if this profit is higher than the current `max_profit`.
    - Update `buy_price` if the current price is lower than the current `buy_price`.
- Return `max_profit` at the end.

# Complexity

- Time complexity:
$$O(n)$$
We only traverse the list once.

- Space complexity:
$$O(1)$$
We use only a constant amount of extra space.

# Code

```python
from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit = 0
        buy_price = prices[0]

        for i in range(1, len(prices)):
            max_profit = max(max_profit, prices[i] - buy_price)
            buy_price = min(buy_price, prices[i])
        
        return max_profit
```

[Back to Problem Statement](./index.md)

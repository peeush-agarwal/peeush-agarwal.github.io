# Intuition

The problem can be visualized as a sequence of slopes (uphill, downhill, flat) in the ratings. My first thought was to count the lengths of increasing and decreasing sequences and use arithmetic series to efficiently calculate the candies needed for each segment.

# Approach

We traverse the ratings and track the length of the current increasing (up) and decreasing (down) slopes. When the slope changes (from up to flat, down to flat, or up to down), we sum the candies for the previous segment using the formula for the sum of the first k natural numbers. For each flat segment, we add one candy. At the end, we add the candies for the last segment and one for the first child.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(1)$$

# Code

```python3
from typing import List

class Solution:
    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        if n <= 1:
            return n

        candies = 0
        up = 0
        down = 0
        old_slope = 0
        for i in range(1, n):
            new_slope = (
                1
                if ratings[i] > ratings[i - 1]
                else (-1 if ratings[i] < ratings[i - 1] else 0)
            )

            if (old_slope > 0 and new_slope == 0) or (old_slope < 0 and new_slope >= 0):
                candies += self.count(up) + self.count(down) + max(up, down)
                up = 0
                down = 0

            if new_slope > 0:
                up += 1
            elif new_slope < 0:
                down += 1
            else:
                candies += 1

            old_slope = new_slope

        candies += self.count(up) + self.count(down) + max(up, down) + 1
        return candies

    def count(self, x):
        return x * (x + 1) // 2
```

[Back to Problem Statement](./index.md)

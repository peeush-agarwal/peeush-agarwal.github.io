# Intuition

To solve the Trapping Rain Water problem, the key insight is that the water trapped at each position depends on the minimum of the maximum heights to its left and right. If you know the tallest bar to the left and right of each position, you can compute the water above that position.

# Approach

We precompute two arrays:
- `left_max[i]`: the highest bar from the start up to index `i`.
- `right_max[i]`: the highest bar from the end up to index `i`.

For each position, the water trapped is `min(left_max[i], right_max[i]) - height[i]`. We sum this for all positions to get the total trapped water.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(n)$$

# Code

```python3
from typing import List

class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        left_max = [0] * n
        right_max = [0] * n

        left_max[0] = height[0]
        for i in range(1, n):
            left_max[i] = max(left_max[i - 1], height[i])

        right_max[n - 1] = height[n - 1]
        for i in range(n - 2, -1, -1):
            right_max[i] = max(right_max[i + 1], height[i])

        ans = 0
        for i in range(n):
            ans += min(left_max[i], right_max[i]) - height[i]

        return ans
```

[Back to Problem Statement](./index.md)

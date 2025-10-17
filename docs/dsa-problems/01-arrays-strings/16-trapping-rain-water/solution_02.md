# Intuition

The problem asks for the total water trapped between bars after raining. My first thought was to use two pointers to efficiently calculate the trapped water without extra space for left/right max arrays.

# Approach

We use two pointers, one starting from the left and one from the right. We keep track of the maximum height seen so far from both ends (`left_max` and `right_max`). At each step, we move the pointer with the smaller height inward, updating the respective max and adding the trapped water at that position. This works because the water trapped at any position is determined by the shorter boundary.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(1)$$

# Code

```python3
from typing import List

class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        if n == 0:
            return 0

        l = 0
        r = n - 1
        left_max = 0
        right_max = 0

        ans = 0
        while l < r:
            if height[l] < height[r]:
                left_max = max(left_max, height[l])
                ans += left_max - height[l]
                l += 1
            else:
                right_max = max(right_max, height[r])
                ans += right_max - height[r]
                r -= 1

        return ans
```

[Back to Problem Statement](./index.md)

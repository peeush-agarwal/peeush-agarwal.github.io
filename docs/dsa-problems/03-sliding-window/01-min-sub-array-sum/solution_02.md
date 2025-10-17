# Intuition

To find the minimal length of a contiguous subarray with sum at least `target`, we can use a sliding window. By expanding and shrinking the window, we efficiently track the sum and update the minimal length when the sum meets or exceeds the target.

# Approach

- Use two pointers (`l` and `r`) to represent the window's bounds.
- Expand the window by moving `r` and adding `nums[r]` to the sum.
- When the sum is at least `target`, shrink the window from the left by moving `l` and subtracting `nums[l]` from the sum, updating the minimal length each time.
- Continue until all elements are processed.
- If no valid subarray is found, return 0.

# Complexity

- Time complexity:
$$O(n)$$, where $n$ is the length of the array (each element is visited at most twice).

- Space complexity:
$$O(1)$$, only a few variables are used.

# Code

```python
from typing import List

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        l, r, s = 0, 0, 0
        res = float("inf")

        for r in range(len(nums)):
            s += nums[r]

            while s >= target:
                res = min(res, r - l + 1)
                s -= nums[l]
                l += 1

        return int(0 if res > len(nums) else res)
```

[Back to Problem Statement](./index.md)

# Intuition

The problem is to find the minimum number of jumps needed to reach the last index of the array, where each element represents the maximum jump length from that position. My first thought was to use a greedy approach, always jumping to the farthest reachable index within the current jump range.

# Approach

We iterate through the array, keeping track of the farthest index we can reach (`far`) and the end of the current jump (`end`). Whenever we reach the end of the current jump, we increment the jump count (`ans`) and update the end to the farthest index we can reach so far. We do not need to jump from the last index, so we iterate up to `n-2`.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(1)$$

# Code

```python3
from typing import List

class Solution:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        ans = 0
        end = 0
        far = 0

        for i in range(n - 1):
            far = max(far, i + nums[i])

            if i == end:
                ans += 1
                end = far

        return ans
```

[Back to Problem Statement](./index.md)

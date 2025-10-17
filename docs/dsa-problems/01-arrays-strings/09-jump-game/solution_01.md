# Intuition

To determine if you can reach the last index, you need to know for each position whether it's possible to jump to the end. A good way to think about this is to work backwards: if you know you can reach the end from a certain position, can you also reach it from earlier positions?

# Approach

Start from the end of the array and move backwards. Keep track of the leftmost position from which the end is reachable (initially the last index). For each index, if you can jump from there to the current leftmost reachable position, update the leftmost position to the current index. At the end, if the leftmost position is 0, then you can reach the end from the start.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(1)$$

# Code

```python
from typing import List

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        last_pos = len(nums) - 1
        # Traverse the array backwards
        for i in range(len(nums) - 2, -1, -1):
            # If you can jump from i to last_pos or beyond, update last_pos
            if i + nums[i] >= last_pos:
                last_pos = i
        # If you can reach the end from the start, last_pos will be 0
        return last_pos == 0
```

[Back to Problem Statement](./index.md)

# Intuition

To determine if you can reach the last index, consider each position's maximum jump length. The key is to check, for every index, whether you can reach the end from there. By working backwards, you can efficiently track the leftmost position from which the end is reachable.

# Approach

Start from the last index and move backwards. Maintain a variable `last_pos` representing the leftmost index from which you can reach the end. For each index, if you can jump from there to `last_pos` or beyond, update `last_pos` to the current index. At the end, if `last_pos` is 0, you can reach the end from the start.

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

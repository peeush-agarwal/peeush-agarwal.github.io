# Intuition

To maximize the area between two lines, we need to consider both the distance between the lines and the height of the shorter line. Starting with the widest possible container (the two ends), we can try to improve the area by moving the pointers inward, always moving the pointer at the shorter line, since moving the taller one cannot increase the area.

# Approach

Use two pointers, one at the start and one at the end of the array. Calculate the area formed by the lines at these pointers. Move the pointer at the shorter line inward, and repeat until the pointers meet. Track the maximum area found during this process.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(1)$$

# Code

```python
from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        i = 0
        j = len(height) - 1
        maxarea = 0

        while i < j:
            new_area = min(height[i], height[j]) * (j - i)
            maxarea = max(maxarea, new_area)

            if height[i] < height[j]:
                i += 1
            else:
                j -= 1

        return maxarea
```

[Back to Problem Statement](./index.md)

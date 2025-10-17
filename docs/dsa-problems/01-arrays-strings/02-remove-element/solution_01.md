# Intuition

The problem asks us to remove all occurrences of a given value from an array in-place and return the new length. My first thought is to use a two-pointer approach: one pointer to read through the array, and another to write the next valid element (not equal to the value to remove).

# Approach

We use two pointers:
- `reader` traverses every element in the array.
- `writer` keeps track of the position to write the next valid element (not equal to `val`).

For each element, if it is not equal to `val`, we write it at the `writer` position and increment `writer`. At the end, `writer` will be the count of elements not equal to `val`.

This approach ensures all valid elements are moved to the front of the array, and the order of the remaining elements does not matter.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(1)$$

# Code

```python
from typing import List

class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        # Pointer to place the next valid element
        writer = 0
        # Traverse all elements
        for reader in range(len(nums)):
            # If current element is not val, write it at writer position
            if nums[reader] != val:
                nums[writer] = nums[reader]
                writer += 1
        # writer is the new length of the array without val
        return writer
```

[Back to Problem Statement](./index.md)

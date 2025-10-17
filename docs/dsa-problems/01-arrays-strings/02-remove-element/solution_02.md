# Intuition

To remove all occurrences of a value from an array in-place, we can minimize the number of writes by swapping unwanted elements with the last element. This way, we avoid shifting elements multiple times and only move each element at most once.

# Approach

We use two pointers:
- `i` starts from the beginning and scans the array.
- `j` starts from the end and represents the new length of the array.

While `i < j`:
- If `nums[i]` equals `val`, we swap it with `nums[j-1]` (the last unchecked element) and decrease `j` by 1. We do not increment `i` in this case, because the swapped-in element at `i` needs to be checked.
- If `nums[i]` does not equal `val`, we increment `i`.

At the end, `i` is the count of elements not equal to `val`.

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
        i = 0
        j = len(nums)
        # Loop until i reaches j
        while i < j:
            if nums[i] == val:
                # Swap with the last unchecked element
                nums[i] = nums[j - 1]
                j -= 1
            else:
                i += 1
        # i is the new length of the array without val
        return i
```

[Back to Problem Statement](./index.md)

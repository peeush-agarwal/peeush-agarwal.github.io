# Intuition

The problem asks us to remove duplicates from a sorted array such that each unique element appears at most twice. Since the array is sorted, duplicates are adjacent, making it easy to count occurrences as we iterate.

# Approach

We use two pointers:
- `insert_index` points to the position where the next valid element should be placed.
- We iterate through the array, keeping a `count` of consecutive duplicates.

For each element:
- If it is the same as the previous one, increment `count`.
- If `count` exceeds 2, skip the element.
- Otherwise, write the element at `insert_index` and increment `insert_index`.

This ensures that each unique element appears at most twice, and the order is preserved.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(1)$$

# Code

```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0

        insert_index = 1
        count = 1
        for i in range(1, n):
            if nums[i] == nums[i-1]:
                count += 1
                if count > 2:
                    continue
            else:
                count = 1
            nums[insert_index] = nums[i]
            insert_index += 1
        return insert_index
```

[Back to Problem Statement](./index.md)

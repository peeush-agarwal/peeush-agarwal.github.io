# Intuition

The problem asks for the majority element, which is defined as the element that appears more than ⌊n / 2⌋ times in the array. Since the majority element always exists, we can leverage this property to find an efficient solution.

# Approach

We use the **Boyer-Moore Voting Algorithm**. The idea is to maintain a candidate for the majority element and a counter. We iterate through the array:
- If the counter is zero, we set the current element as the candidate.
- If the current element is the candidate, we increment the counter.
- Otherwise, we decrement the counter.

Since the majority element appears more than half the time, it will always be the candidate at the end.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(1)$$

# Code

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        # Initialize the candidate and counter
        ans = nums[0]
        count = 1

        for i in range(1, len(nums)):
            if nums[i] == ans:
                count += 1
            elif count == 0:
                ans = nums[i]
                count = 1
            else:
                count -= 1
        
        return ans
```

[Back to Problem Statement](./index.md)

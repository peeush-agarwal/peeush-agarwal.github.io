# Minimum Size Subarray Sum

Given an array of positive integers `nums` and a positive integer `target`, find the minimal length of a contiguous subarray of which the sum is greater than or equal to `target`. If no such subarray exists, return `0`.

**Examples**

- **Example 1**  
    Input: `target = 7`, `nums = [2,3,1,2,4,3]`  
    Output: `2`  
    Explanation: The subarray `[4,3]` has the minimal length under the problem constraint.

- **Example 2**  
    Input: `target = 4`, `nums = [1,4,4]`  
    Output: `1`

- **Example 3**  
    Input: `target = 11`, `nums = [1,1,1,1,1,1,1,1]`  
    Output: `0`

**Constraints**

- `1 <= target <= 10^9`
- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^4`

**Follow-up**  
If you have solved the problem with an O(n) solution, try implementing an O(n log n) solution.

## Code Template

```python
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        # Your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md): This approach uses prefix sums and binary search to find the minimal length of a contiguous subarray with sum at least `target`. The time complexity is O(n log n) and space complexity is O(n).
- [Solution 2](./solution_02.md): This approach uses the sliding window technique to find the minimal length of a contiguous subarray with sum at least `target`. The time complexity is O(n) and space complexity is O(1).

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)

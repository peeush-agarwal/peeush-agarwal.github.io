# Three Sum

## Problem Statement

Given an integer array `nums`, find all unique triplets `[nums[i], nums[j], nums[k]]` such that:

- `i`, `j`, and `k` are distinct indices (`i != j`, `i != k`, `j != k`)
- The sum of the triplet is zero: `nums[i] + nums[j] + nums[k] == 0`
- The solution set must not contain duplicate triplets.

### Examples

**Example 1**

```
Input: nums = [-1, 0, 1, 2, -1, -4]
Output: [[-1, -1, 2], [-1, 0, 1]]
Explanation:
- (-1) + 0 + 1 = 0
- 0 + 1 + (-1) = 0
- (-1) + 2 + (-1) = 0
Distinct triplets are [-1, 0, 1] and [-1, -1, 2].
Order of output and triplets does not matter.
```

**Example 2**

```
Input: nums = [0, 1, 1]
Output: []
Explanation: No triplet sums to 0.
```

**Example 3**

```
Input: nums = [0, 0, 0]
Output: [[0, 0, 0]]
Explanation: Only one triplet sums to 0.
```

### Constraints

- `3 <= nums.length <= 3000`
- `-10^5 <= nums[i] <= 10^5`

## Code Template

```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        # Write your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md): This approach uses hash sets and hash maps to find all unique triplets that sum to zero. Time complexity is O(n^2) and space complexity is O(n).

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)

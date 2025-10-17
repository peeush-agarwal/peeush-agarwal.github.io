# Jump Game

## Problem Description

You are given an integer array `nums`. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position.

Return `true` if you can reach the last index, or `false` otherwise.

### Examples

**Example 1:**

- Input: `nums = [2,3,1,1,4]`
- Output: `true`
- Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.

**Example 2:**

- Input: `nums = [3,2,1,0,4]`
- Output: `false`
- Explanation: You will always arrive at index 3 no matter what. Its maximum jump length is 0, which makes it impossible to reach the last index.

### Constraints

- $1 \leq \text{nums.length} \leq 10^4$
- $0 \leq \text{nums}[i] \leq 10^5$

## Code Template

```python
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        pass
```

## Solutions

- [Solution 1](solution_01.md): This approach uses a dynamic programming technique to determine if the last index is reachable.

[Back to Problems List](../index.md) | [Back to Categories](../../index.md)

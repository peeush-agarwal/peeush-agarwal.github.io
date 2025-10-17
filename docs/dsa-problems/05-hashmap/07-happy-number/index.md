# Happy Number

## Problem Statement

Given a positive integer `n`, determine if it is a happy number.

A happy number is defined by the following process:
- Starting with any positive integer, replace the number by the sum of the squares of its digits.
- Repeat this process until the number equals 1 (where it will stay), or it loops endlessly in a cycle that does not include 1.
- Numbers for which this process ends in 1 are considered happy.

Return `true` if `n` is a happy number, otherwise return `false`.

**Examples**

**Example 1:**
```
Input: n = 19
Output: true
Explanation:
1² + 9² = 82
8² + 2² = 68
6² + 8² = 100
1² + 0² + 0² = 1
```

**Example 2:**
```
Input: n = 2
Output: false
```

**Constraints**
- 1 <= n <= 2³¹ - 1

## Code Template

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        # Your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md) - Using a set to detect cycles in the process. Time complexity: O(log² n), Space complexity: O(k) where k is the number of unique numbers seen before a cycle is detected.

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)

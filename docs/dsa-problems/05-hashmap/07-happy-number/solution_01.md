# Intuition

A happy number eventually reaches 1 when repeatedly replaced by the sum of the squares of its digits. If it falls into a cycle (other than 1), it will never reach 1. We can use a set to detect cycles.

# Approach

- Use a helper function to compute the sum of squares of digits.
- Use a set to track numbers seen so far.
- Repeat the process until the number becomes 1 or a cycle is detected (number repeats).
- Return `True` if 1 is reached, otherwise `False`.

# Complexity

- Time complexity:
$$O(\,\text{log}^2 n)$$ (each step reduces the number, and the sum of squares is bounded for integers).

- Space complexity:
$$O(k)$$, where $k$ is the number of unique numbers seen before a cycle is detected (typically small).

# Code

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        def get_next(x):
            s = 0
            while x > 0:
                d = x % 10
                s += d**2
                x = x // 10
            return s

        seen = set()
        while n != 1 and n not in seen:
            seen.add(n)
            n = get_next(n)

        return n == 1
```

[Back to Problem Statement](./index.md)

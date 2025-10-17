# Intuition

The problem requires distributing candies such that each child gets at least one, and children with higher ratings than their neighbors get more candies. My first thought was to scan the ratings from left to right and right to left to ensure both neighbor conditions are satisfied.

# Approach

We initialize every child with one candy. First, we scan from left to right: if a child has a higher rating than the previous child, they get one more candy than the previous child. Then, we scan from right to left: if a child has a higher rating than the next child, we ensure they have at least one more candy than the next child. The total candies is the sum after both passes.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(n)$$

# Code

```python3
from typing import List

class Solution:
    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)

        candies = [1] * n

        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                candies[i] = candies[i - 1] + 1

        total_candies = candies[-1]
        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                candies[i] = max(candies[i], candies[i + 1] + 1)

            total_candies += candies[i]

        return total_candies

if __name__ == "__main__":
    solution = Solution()
    print(solution.candy([1, 0, 2]))
    print(solution.candy([1, 2, 2]))
```

[Back to Problem Statement](./index.md)

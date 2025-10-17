from typing import List


class Solution:
    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        if n <= 1:
            return n

        candies = 0
        up = 0
        down = 0
        old_slope = 0
        for i in range(1, n):
            new_slope = (
                1
                if ratings[i] > ratings[i - 1]
                else (-1 if ratings[i] < ratings[i - 1] else 0)
            )

            if (old_slope > 0 and new_slope == 0) or (old_slope < 0 and new_slope >= 0):
                candies += self.count(up) + self.count(down) + max(up, down)
                up = 0
                down = 0

            if new_slope > 0:
                up += 1
            elif new_slope < 0:
                down += 1
            else:
                candies += 1

            old_slope = new_slope

        candies += self.count(up) + self.count(down) + max(up, down) + 1
        return candies

    def count(self, x):
        return x * (x + 1) // 2


if __name__ == "__main__":
    solution = Solution()
    print(solution.candy([1, 0, 2]))
    print(solution.candy([1, 2, 2]))

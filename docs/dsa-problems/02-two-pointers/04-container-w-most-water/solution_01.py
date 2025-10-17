from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        i = 0
        j = len(height) - 1
        maxarea = 0

        while i < j:
            new_area = min(height[i], height[j]) * (j - i)
            maxarea = max(maxarea, new_area)

            if height[i] < height[j]:
                i += 1
            else:
                j -= 1

        return maxarea


if __name__ == "__main__":
    solution = Solution()
    print(solution.maxArea(height=[1, 8, 6, 2, 5, 4, 8, 3, 7]))
    print(solution.maxArea(height=[1, 1]))

from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        if n == 0:
            return 0

        left = 0
        right = n - 1
        left_max = 0
        right_max = 0

        ans = 0
        while left < right:
            if height[left] < height[right]:
                left_max = max(left_max, height[left])
                ans += left_max - height[left]
                left += 1
            else:
                right_max = max(right_max, height[right])
                ans += right_max - height[right]
                right -= 1

        return ans


if __name__ == "__main__":
    solution = Solution()
    print(solution.trap(height=[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))
    print(solution.trap(height=[4, 2, 0, 3, 2, 5]))

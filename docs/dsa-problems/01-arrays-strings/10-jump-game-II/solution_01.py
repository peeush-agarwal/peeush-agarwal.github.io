from typing import List


class Solution:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        ans = 0
        end = 0
        far = 0

        for i in range(n - 1):
            far = max(far, i + nums[i])

            if i == end:
                ans += 1
                end = far

        return ans


if __name__ == "__main__":
    solution = Solution()
    print(solution.jump([2, 3, 0, 1, 4]))  # Output: 2

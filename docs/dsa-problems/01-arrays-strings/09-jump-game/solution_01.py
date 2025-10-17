from typing import List


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        last_pos = len(nums) - 1

        for i in range(len(nums) - 2, -1, -1):
            if i + nums[i] >= last_pos:
                last_pos = i

        return last_pos == 0


if __name__ == "__main__":
    solution = Solution()
    nums = [3, 2, 1, 0, 4]
    print(solution.canJump(nums))  # Output: False
    nums = [2, 3, 1, 1, 4]
    print(solution.canJump(nums))  # Output: True

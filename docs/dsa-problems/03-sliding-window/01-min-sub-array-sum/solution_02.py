from typing import List


class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left, right, sub_sum = 0, 0, 0
        res = float("inf")

        for right in range(len(nums)):
            sub_sum += nums[right]

            while sub_sum >= target:
                res = min(res, right - left + 1)
                sub_sum -= nums[left]
                left += 1

        return int(0 if res > len(nums) else res)


if __name__ == "__main__":
    solution = Solution()
    print(solution.minSubArrayLen(target=7, nums=[2, 3, 1, 2, 4, 3]))
    print(solution.minSubArrayLen(target=4, nums=[1, 4, 4]))
    print(solution.minSubArrayLen(target=11, nums=[1, 1, 1, 1, 1, 1, 1, 1]))

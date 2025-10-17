from typing import List


class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        n = len(nums)
        prefix_sum = [0] * n
        prefix_sum[0] = nums[0]

        for i in range(1, n):
            prefix_sum[i] = prefix_sum[i - 1] + nums[i]

        res = float("inf")
        for i in range(n):
            start, end = 0, n - 1
            while start <= end:
                mid = (start + end) // 2
                sub_sum = prefix_sum[mid] - prefix_sum[i] + nums[i]
                if sub_sum >= target:
                    res = min(res, mid - i + 1)
                    end = mid - 1
                else:
                    start = mid + 1

        return int(0 if res > n else res)


if __name__ == "__main__":
    solution = Solution()
    print(solution.minSubArrayLen(target=7, nums=[2, 3, 1, 2, 4, 3]))
    print(solution.minSubArrayLen(target=4, nums=[1, 4, 4]))
    print(solution.minSubArrayLen(target=11, nums=[1, 1, 1, 1, 1, 1, 1, 1]))

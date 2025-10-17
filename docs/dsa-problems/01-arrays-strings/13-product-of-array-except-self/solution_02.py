from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        answer = [0] * n
        R = 1

        answer[0] = 1
        for i in range(1, n):
            answer[i] = answer[i - 1] * nums[i - 1]

        for i in range(n - 1, -1, -1):
            answer[i] = answer[i] * R
            R *= nums[i]

        return answer


if __name__ == "__main__":
    solution = Solution()
    print(solution.productExceptSelf([1, 2, 3, 4]))  # Output: [24, 12, 8, 6]
    print(solution.productExceptSelf([-1, 1, 0, -3, 3]))  # Output: [0, 0, 9, 0, 0]

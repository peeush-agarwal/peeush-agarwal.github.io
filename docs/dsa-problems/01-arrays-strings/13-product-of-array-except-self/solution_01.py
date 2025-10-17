from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        prefix_prod = [0] * n
        suffix_prod = [0] * n
        answer = []

        prefix_prod[0] = 1
        for i in range(1, n):
            prefix_prod[i] = prefix_prod[i - 1] * nums[i - 1]

        suffix_prod[n - 1] = 1
        for i in range(n - 2, -1, -1):
            suffix_prod[i] = suffix_prod[i + 1] * nums[i + 1]

        for i in range(n):
            answer.append(prefix_prod[i] * suffix_prod[i])

        return answer


if __name__ == "__main__":
    solution = Solution()
    print(solution.productExceptSelf([1, 2, 3, 4]))  # Output: [24, 12, 8, 6]
    print(solution.productExceptSelf([-1, 1, 0, -3, 3]))  # Output: [0, 0, 9, 0, 0]

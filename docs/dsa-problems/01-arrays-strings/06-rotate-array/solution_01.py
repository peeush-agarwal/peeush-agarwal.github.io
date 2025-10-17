from typing import List


class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        k %= n

        def reverse(start, end):
            i = start
            j = end

            while i < j:
                nums[i], nums[j-1] = nums[j-1], nums[i]
                i += 1
                j -= 1

        reverse(0, n)
        reverse(0, k)
        reverse(k, n)


if __name__ == "__main__":
    nums = [1,2,3,4,5,6,7]
    k = 3

    solution = Solution()
    solution.rotate(nums, k)
    print(nums)

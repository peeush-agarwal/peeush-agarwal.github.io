from typing import List


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        i = 0
        j = len(nums)

        while i < j:
            if nums[i] == val:
                nums[i] = nums[j - 1]
                j -= 1
            else:
                i += 1
        return i


if __name__ == "__main__":
    solution = Solution()

    nums = [3,2,2,3]
    val = 3

    end = solution.removeElement(nums, val)
    print(nums[:end])

    nums = [0,1,2,2,3,0,4,2]
    val = 2

    end = solution.removeElement(nums, val)
    print(nums[:end])

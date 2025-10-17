from typing import List


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        # Your code here
        writer = 0

        for reader in range(len(nums)):
            if nums[reader] != val:
                nums[writer] = nums[reader]
                writer += 1
        
        return writer


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

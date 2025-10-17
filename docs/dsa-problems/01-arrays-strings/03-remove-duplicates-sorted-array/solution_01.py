from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        n = len(nums)

        if n == 0:
            return 0
        
        insert_index = 1
        for i in range(1, n):
            if nums[i] != nums[i-1]:
                nums[insert_index] = nums[i]
                insert_index += 1
        
        return insert_index


if __name__ == "__main__":
    solution = Solution()

    nums = [0,0,1,1,1,2,2,3,3,4]
    k = solution.removeDuplicates(nums)
    print(nums[:k])  # Output: [0, 1, 2, 3, 4]

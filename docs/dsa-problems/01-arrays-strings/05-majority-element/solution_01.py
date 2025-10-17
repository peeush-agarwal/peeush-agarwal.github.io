from typing import List


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        ans = nums[0]
        count = 1

        for i in range(1, len(nums)):
            if nums[i] == ans:
                count += 1
            elif count == 0:
                ans = nums[i]
                count = 1
            else:
                count -= 1
        
        return ans


if __name__ == "__main__":
    nums = [2,2,1,1,1,2,2]

    solution = Solution()
    print(solution.majorityElement(nums))  # Output: 2

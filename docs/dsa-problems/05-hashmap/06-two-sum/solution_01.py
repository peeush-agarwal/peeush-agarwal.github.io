from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        map_ = {nums[0]: 0}

        for i in range(1, len(nums)):
            comp = target - nums[i]

            if comp in map_:
                return [map_[comp], i]

            map_[nums[i]] = i

        return [-1, -1]


if __name__ == "__main__":
    solution = Solution()
    print(solution.twoSum(nums=[2, 7, 11, 15], target=9))
    print(solution.twoSum(nums=[3, 2, 4], target=6))
    print(solution.twoSum(nums=[3, 3], target=6))

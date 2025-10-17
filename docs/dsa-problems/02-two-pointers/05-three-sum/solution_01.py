from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res, dups = set(), set()
        seen = {}

        for i in range(len(nums)):
            if nums[i] not in dups:
                dups.add(nums[i])

                for j in range(i + 1, len(nums)):
                    compl = -nums[i] - nums[j]
                    if compl in seen and seen[compl] == i:
                        res.add(tuple(sorted((nums[i], nums[j], compl))))
                    seen[nums[j]] = i

        return [list(x) for x in res]


if __name__ == "__main__":
    solution = Solution()
    print(solution.threeSum(nums=[-1, 0, 1, 2, -1, -4]))
    print(solution.threeSum(nums=[0, 1, 1]))
    print(solution.threeSum(nums=[0, 0, 0]))

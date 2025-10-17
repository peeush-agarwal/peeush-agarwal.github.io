from typing import List


class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        n = len(gas)

        total_gain = 0
        curr_gain = 0
        answer = 0

        for i in range(n):
            total_gain += gas[i] - cost[i]
            curr_gain += gas[i] - cost[i]

            if curr_gain < 0:
                curr_gain = 0
                answer = i + 1

        return answer if total_gain >= 0 else -1


if __name__ == "__main__":
    gas = [1, 2, 3, 4, 5]
    cost = [3, 4, 5, 1, 2]

    solution = Solution()
    print(solution.canCompleteCircuit(gas, cost))
    print(solution.canCompleteCircuit(gas=[2, 3, 4], cost=[3, 4, 3]))

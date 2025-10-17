from typing import List


class Solution:
    def hIndex(self, citations: List[int]) -> int:
        n = len(citations)
        papers = [0] * (n + 1)

        for i in range(n):
            papers[min(n, citations[i])] += 1

        cumm_papers = 0
        for h in range(n, -1, -1):
            cumm_papers += papers[h]
            if cumm_papers >= h:
                return h

        return 0


if __name__ == "__main__":
    solution = Solution()
    citations = [3, 0, 6, 1, 5]
    print(solution.hIndex(citations))
    citations = [1, 3, 1]
    print(solution.hIndex(citations))

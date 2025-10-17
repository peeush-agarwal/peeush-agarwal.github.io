from typing import List


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        m = len(matrix)
        n = len(matrix[0])
        res = []

        def boundary_items(rs, re, cs, ce):
            # First row
            res.extend([matrix[rs][c] for c in range(cs, ce + 1)])

            # Last col
            res.extend([matrix[r][ce] for r in range(rs + 1, re)])

            if rs != re:
                # Bottom row
                res.extend([matrix[re][c] for c in range(ce, cs - 1, -1)])

            if cs != ce:
                # First col
                res.extend([matrix[r][cs] for r in range(re - 1, rs, -1)])

        rs, re = 0, m - 1
        cs, ce = 0, n - 1

        while (rs <= re) and (cs <= ce):
            boundary_items(rs, re, cs, ce)

            rs += 1
            re -= 1
            cs += 1
            ce -= 1

        return res


if __name__ == "__main__":
    solution = Solution()
    print(solution.spiralOrder(matrix=[[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    print(solution.spiralOrder(matrix=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]))

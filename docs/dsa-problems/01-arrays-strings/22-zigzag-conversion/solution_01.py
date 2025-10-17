class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if (numRows == 1) or (len(s) <= numRows):
            return s

        rows = {}
        cur_row = 0
        step = 1

        for c in s:
            rows[cur_row] = rows.get(cur_row, [])
            rows[cur_row].append(c)
            cur_row += step

            if (cur_row <= 0) or (cur_row >= numRows - 1):
                step = -1 * step

        ans = []
        for r in range(numRows):
            ans.extend(rows[r])

        return "".join(ans)


if __name__ == "__main__":
    solution = Solution()
    print(solution.convert(s="PAYPALISHIRING", numRows=3))  # Output: PAHNAPLSIIGYIR
    print(solution.convert(s="PAYPALISHIRING", numRows=4))  # Output: PINALSIGYAHRPI
    print(solution.convert(s="PAYPALISHIRING", numRows=14))  # Output: PAYPALISHIRING

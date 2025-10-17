class Solution:
    def convert(self, s: str, numRows: int) -> str:
        n = len(s)
        if (numRows == 1) or (n <= numRows):
            return s

        ans = []
        chars_in_section = 2 * numRows - 2

        for i in range(numRows):
            index = i
            while index < n:
                ans.append(s[index])

                if (i != 0) and (i != numRows - 1):
                    chars_in_betw = chars_in_section - 2 * i
                    second_index = index + chars_in_betw

                    if second_index < n:
                        ans.append(s[second_index])

                index += chars_in_section

        return "".join(ans)


if __name__ == "__main__":
    solution = Solution()
    print(solution.convert(s="PAYPALISHIRING", numRows=3))  # Output: PAHNAPLSIIGYIR
    print(solution.convert(s="PAYPALISHIRING", numRows=4))  # Output: PINALSIGYAHRPI
    print(solution.convert(s="PAYPALISHIRING", numRows=14))  # Output: PAYPALISHIRING

from typing import List


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        def transpose():
            for i in range(n):
                for j in range(i):
                    matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

        def reflect():
            for i in range(n):
                for j in range(n // 2):
                    matrix[i][j], matrix[i][-j - 1] = matrix[i][-j - 1], matrix[i][j]

        n = len(matrix)
        transpose()
        reflect()


if __name__ == "__main__":
    solution = Solution()
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    solution.rotate(matrix)
    print(matrix)

    matrix = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
    solution.rotate(matrix)
    print(matrix)

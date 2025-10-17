from typing import List


class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        m = len(board)
        n = len(board[0])

        new_board = [[board[r][c] for c in range(n)] for r in range(m)]

        neighbors = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        for row in range(m):
            for col in range(n):
                live_neighbors = 0
                for i, j in neighbors:
                    r = row + i
                    c = col + j

                    if (0 <= r < m) and (0 <= c < n) and (new_board[r][c] == 1):
                        live_neighbors += 1

                if (new_board[row][col] == 1) and (
                    live_neighbors < 2 or live_neighbors > 3
                ):
                    board[row][col] = 0

                if (new_board[row][col] == 0) and (live_neighbors == 3):
                    board[row][col] = 1


if __name__ == "__main__":
    solution = Solution()

    board = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
    solution.gameOfLife(board)
    print(board)

    board = board = [[1, 1], [1, 0]]
    solution.gameOfLife(board)
    print(board)

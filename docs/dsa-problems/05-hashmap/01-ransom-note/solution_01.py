class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        m_counts = {}
        for c in magazine:
            m_counts[c] = m_counts.get(c, 0) + 1

        for c in ransomNote:
            if c not in m_counts or m_counts[c] == 0:
                return False

            m_counts[c] -= 1

        return True


if __name__ == "__main__":
    solution = Solution()
    print(solution.canConstruct(ransomNote="a", magazine="b"))
    print(solution.canConstruct(ransomNote="aa", magazine="ab"))
    print(solution.canConstruct(ransomNote="a", magazine="aab"))

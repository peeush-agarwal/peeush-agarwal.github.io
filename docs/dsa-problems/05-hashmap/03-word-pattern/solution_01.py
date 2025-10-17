class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split()
        if len(pattern) != len(words):
            return False

        mapped_dict = {}
        mapped_set = set()

        for p, word in zip(pattern, words):
            mapped_dict[p] = mapped_dict.get(p, word)
            if mapped_dict[p] != word:
                return False

            mapped_set.add(word)

        if len(mapped_set) != len(mapped_dict):
            return False
        return True


if __name__ == "__main__":
    solution = Solution()
    print(solution.wordPattern(pattern="abba", s="dog cat cat dog"))
    print(solution.wordPattern(pattern="abba", s="dog cat cat fish"))
    print(solution.wordPattern(pattern="aaaa", s="dog cat cat dog"))

from collections import Counter, defaultdict
from typing import List


class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        n = len(s)
        k = len(words)
        word_len = len(words[0])
        substring_size = k * word_len
        words_count = Counter(words)

        def sliding_window(left):
            seen = defaultdict(int)
            words_remaining = k
            excess_word = False

            for right in range(left, n, word_len):
                sub = s[right : right + word_len]
                if sub not in words_count:
                    seen = defaultdict(int)
                    words_remaining = k
                    excess_word = False
                    left = right + word_len
                else:
                    while right - left == substring_size or excess_word:
                        leftmost_word = s[left : left + word_len]
                        left += word_len
                        seen[leftmost_word] -= 1

                        if seen[leftmost_word] == words_count[leftmost_word]:
                            excess_word = False
                        else:
                            words_remaining += 1

                    seen[sub] += 1
                    if seen[sub] <= words_count[sub]:
                        words_remaining -= 1
                    else:
                        excess_word = True

                    if words_remaining == 0 and not excess_word:
                        ans.append(left)

        ans = []
        for i in range(word_len):
            sliding_window(i)

        return ans


if __name__ == "__main__":
    solution = Solution()
    print(solution.findSubstring(s="barfoothefoobarman", words=["foo", "bar"]))
    print(
        solution.findSubstring(
            s="wordgoodgoodgoodbestword", words=["word", "good", "best", "word"]
        )
    )
    print(
        solution.findSubstring(
            s="barfoofoobarthefoobarman", words=["bar", "foo", "the"]
        )
    )

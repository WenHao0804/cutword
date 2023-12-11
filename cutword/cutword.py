# -*- coding: utf-8 -*-

from collections import namedtuple
import math
import re
import ahocorasick
import re
import os

re_han = re.compile("([\u4E00-\u9FD5]+)")
re_skip = re.compile("([a-zA-Z0-9]+(?:\.\d+)?%?)")

root_path = os.path.dirname(os.path.realpath(__file__))

WordInfo = namedtuple('WordInfo', ['freq', 'pos'])

class Cutter:
    """Unigram tokenizer with Aho-Corasick automaton
    """
    def __init__(self, dict_name="dict.txt"):
        dict_path = os.path.join(root_path, dict_name)
        self._pieces = {}
        for line in open(dict_path):
            line = line.strip()
            word, freq, pos = line.split()
            self._pieces[word] = WordInfo(float(freq) + 1e-10, pos)

        # Aho-Corasick automaton
        log_total = math.log(sum([_.freq for _ in self._pieces.values()]))
        self._automaton = ahocorasick.Automaton()
        for word, info in self._pieces.items():
            self._automaton.add_word(word, (len(word), math.log(info.freq) - log_total, info.pos))

        self._automaton.make_automaton()


    def _tokenize(self, text):
        inf = -1e10
        scores = [0] + [inf] * len(text)
        routes = list(range(len(text) + 1))
        tokens = []
        for end, (word_len, value, pos) in self._automaton.iter(text):
            start, end = end - word_len + 1, end + 1
            if scores[start] == inf:
                #word not include in dict
                last = start
                while scores[last] == inf and last > 0:
                    last -= 1
                scores[start] = scores[last] -10 #punish score
                routes[start] = last

            score = scores[start] + value
            if score > scores[end]:
                scores[end], routes[end] = score, start

        if end < len(text):
            tokens.append(text[end:])
            text = text[:end]

        while text:
            start = routes[end]
            tokens.append(text[start:end])
            text, end = text[:start], start
        return tokens[::-1]

    def cutword(self, text):
        res = []
        blocks = re_han.split(text)
        for blk in blocks:
            if re_han.match(blk):
                res.extend(self._tokenize(blk))
            else:
                tmp = re_skip.split(blk)
                tmp = [i for i in tmp if i]
                res.extend(tmp)
        return res

if __name__ == "__main__":
    tokenizer = Cutter()
    text = "小明硕士毕业于中国科学院计算所，后在日本京都大学深造"
    res = tokenizer.cutword(text)
    print(res)

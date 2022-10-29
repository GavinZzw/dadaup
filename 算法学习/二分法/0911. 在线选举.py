# -*- coding: utf-8 -*-
# @Time    : 2022/10/21 10:16
# @Author  : zzw
# @File    : 0911. 在线选举.py
"""
给你两个整数数组 persons 和 times 。在选举中，第 i 张票是在时刻为 times[i] 时投给候选人 persons[i] 的。

对于发生在时刻 t 的每个查询，需要找出在 t 时刻在选举中领先的候选人的编号。

在 t 时刻投出的选票也将被计入我们的查询之中。在平局的情况下，最近获得投票的候选人将会获胜。
[0, 1, 1, 0, 0, 1, 0], [0, 5, 10, 15, 20, 25, 30]
"""
from typing import List


class TopVotedCandidate:

    def __init__(self, persons: List[int], times: List[int]):
        self.tops = []
        self.votes = {}
        self.times = times
        top_person, max_vote = -1, 0

        for person in persons:
            vote = self.votes.get(person, 0)
            vote += 1
            self.votes[person] = vote
            if vote >= max_vote:
                top_person, max_vote = person, vote
            self.tops.append(top_person)

    def q(self, t: int) -> int:
        l, r = 0, len(self.times) - 1
        while l < r:
            mid = (l + r + 1) // 2
            if self.times[mid] > t:
                r = mid - 1
            else:
                l = mid
        return self.tops[l]


s = TopVotedCandidate([0, 0, 0, 0, 1], [0, 6, 39, 52, 75])
print(s.q(78))

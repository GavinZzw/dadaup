# -*- coding: utf-8 -*-
# @Time    : 2022/10/9 11:55
# @Author  : zzw
# @File    : 0275. H 指数 II.py
from typing import List

"""
给你一个整数数组 citations ，其中 citations[i] 表示研究者的第 i 篇论文被引用的次数，citations 已经按照 升序排列 。
计算并返回该研究者的 h 指数。

h 指数的定义：h 代表“高引用次数”（high citations），一名科研人员的 h 指数是指他（她）的 （n 篇论文中）总共有 h 篇论文分别被引用了至少 h 次。
且其余的 n - h 篇论文每篇被引用次数 不超过 h 次。
"""


class Solution:
    def hIndex(self, citations: List[int]) -> int:
        n = len(citations)
        l, r = 0, n - 1
        while l <= r:
            mid = (l + r) // 2
            if citations[mid] >= n - mid:
                r = mid - 1
            else:
                l = mid + 1
        return n - l


s = Solution()
print(s.hIndex([0]))

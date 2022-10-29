# -*- coding: utf-8 -*-
# @Time    : 2022/10/21 10:02
# @Author  : zzw
# @File    : 0901. 股票价格跨度.py

"""
编写一个 StockSpanner 类，它收集某些股票的每日报价，并返回该股票当日价格的跨度。

今天股票价格的跨度被定义为股票价格小于或等于今天价格的最大连续日数（从今天开始往回数，包括今天）。

例如，如果未来7天股票的价格是 [100, 80, 60, 70, 60, 75, 85]，那么股票跨度将是 [1, 1, 1, 2, 1, 4, 6]。
"""


class StockSpanner:
    def __init__(self):
        self.stack = [(-1, float("inf"))]
        self.idx = -1

    def next(self, price: int) -> int:
        self.idx += 1
        # 单调栈
        while price >= self.stack[-1][1]:
            self.stack.pop()
        self.stack.append((self.idx, price))
        return self.idx - self.stack[-2][0]

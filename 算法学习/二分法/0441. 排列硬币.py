# -*- coding: utf-8 -*-
# @Time    : 2022/10/13 15:29
# @Author  : zzw
# @File    : 0441. 排列硬币.py
"""
你总共有 n 枚硬币，并计划将它们按阶梯状排列。对于一个由 k 行组成的阶梯，其第 i 行必须正好有 i 枚硬币。阶梯的最后一行 可能 是不完整的。

给你一个数字 n ，计算并返回可形成 完整阶梯行 的总行数。
"""


class Solution:
    def arrangeCoins(self, n: int) -> int:
        # n行需要(n+1)*n/2
        l, r = 1, n

        while l < r:
            mid = (l + r) // 2 + 1
            if (mid + 1) * mid / 2 > n:
                r = mid - 1
            else:
                l = mid

        return l


s = Solution()
print(s.arrangeCoins(5))

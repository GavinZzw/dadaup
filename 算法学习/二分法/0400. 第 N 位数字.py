# -*- coding: utf-8 -*-
# @Time    : 2022/10/12 10:44
# @Author  : zzw
# @File    : 0400. 第 N 位数字.py

"""
给你一个整数 n ，请你在无限的整数序列 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ...] 中找出并返回第 n 位上的数字。
"""


class Solution:
    def findNthDigit(self, n: int) -> int:
        # 几位数范围内
        i = 1

        # i位数总和
        sumi = 9 * 10 ** (i - 1) * i

        while n > sumi:
            n -= sumi
            i += 1
            sumi = 9 * 10 ** (i - 1) * i
        x, y = divmod(n, i)
        num = 10 ** (i - 1) + x - 1
        num_next = num + 1
        str_num = str(num)[-1] + str(num_next)
        return int(str_num[y])


s = Solution()
print(s.findNthDigit(11))

# -*- coding: utf-8 -*-
# @Time    : 2022/10/11 10:50
# @Author  : zzw
# @File    : 0367. 有效的完全平方数.py

"""
给定一个 正整数 num ，编写一个函数，如果 num 是一个完全平方数，则返回 true ，否则返回 false 。

进阶：不要 使用任何内置的库函数，如  sqrt 。

"""


class Solution:
    def isPerfectSquare(self, num: int) -> bool:

        l, r = 0, num

        while l <= r:
            mid = (l + r) // 2

            if mid * mid == num:
                return True
            elif mid * mid < num:
                l = mid + 1
            else:
                r = mid - 1
        return False


s = Solution()
print(s.isPerfectSquare(8))

# -*- coding: utf-8 -*-
# @Time    : 2022/7/25 10:13
# @Author  : zzw
# @File    : 0069. x 的平方根.py
"""
输入：x = 8
输出：2
解释：8 的算术平方根是 2.82842..., 由于返回类型是整数，小数部分将被舍去。
"""


class Solution:
    def mySqrt(self, x: int) -> int:
        l, r = 0, x
        res = 0
        while l <= r:
            mid = (l + r) // 2
            if mid ** 2 > x:
                r = mid - 1
            else:
                res = mid
                l = mid + 1
        return res


s = Solution()
print(s.mySqrt(0))

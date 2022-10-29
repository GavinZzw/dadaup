# -*- coding: utf-8 -*-
# @Time    : 2022/10/10 9:44
# @Author  : zzw
# @File    : 0287. 寻找重复数.py

"""
给定一个包含 n + 1 个整数的数组 nums ，其数字都在 [1, n] 范围内（包括 1 和 n），可知至少存在一个重复的整数。

假设 nums 只有 一个重复的整数 ，返回 这个重复的数 。
"""
from typing import List


class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        """
        二分法：统计每个大于等于改索引的数个数，第一个个数大于索引的索引就是重复的数字
        :param nums:
        :return:
        """

        n = len(nums)
        l, r = 1, n - 1

        while l < r:
            mid = (l + r) // 2
            cnt = 0
            for i in nums:
                if i <= mid:
                    cnt += 1
            if cnt <= mid:
                l = mid + 1
            else:
                r = mid
        return l

s = Solution()
print(s.findDuplicate([3, 1, 3, 4, 2]))

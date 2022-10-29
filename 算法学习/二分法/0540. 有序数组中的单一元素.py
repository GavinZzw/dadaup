# -*- coding: utf-8 -*-
# @Time    : 2022/10/17 11:00
# @Author  : zzw
# @File    : 0540. 有序数组中的单一元素.py

"""
给你一个仅由整数组成的有序数组，其中每个元素都会出现两次，唯有一个数只会出现一次。

请你找出并返回只出现一次的那个数。
"""
from typing import List


class Solution:
    def singleNonDuplicate(self, nums: List[int]) -> int:

        l, r = 0, len(nums) - 1

        while l < r:
            mid = (l + r) // 2

            if nums[mid] == nums[mid ^ 1]:
                l = mid + 1
            else:
                r = mid
        return nums[l]


s = Solution()
print(s.singleNonDuplicate([1, 1, 2, 3, 3, 4, 4, 8, 8]))

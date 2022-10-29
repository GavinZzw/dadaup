# -*- coding: utf-8 -*-
# @Time    : 2022/7/25 10:56
# @Author  : zzw
# @File    : 0268. 丢失的数字.py

"""
给定一个包含 [0, n] 中 n 个数的数组 nums ，找出 [0, n] 这个范围内没有出现在数组中的那个数。

"""
from typing import List


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        """
        输入：nums = [3,0,1]
        输出：2
        解释：n = 3，因为有 3 个数字，所以所有的数字都在范围 [0,3] 内。2 是丢失的数字，因为它没有出现在 nums 中。
        :param nums:
        :return:
        """
        d = 0

        for index, num in enumerate(nums):
            d += num - index
        return len(nums) - d


s = Solution()
print(s.missingNumber([9, 6, 4, 2, 3, 5, 7, 0, 1]))

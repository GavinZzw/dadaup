# -*- coding: utf-8 -*-
# @Time    : 2022/10/18 9:59
# @Author  : zzw
# @File    : 0611. 有效三角形的个数.py

"""
给定一个包含非负整数的数组 nums ，返回其中可以组成三角形三条边的三元组个数。
输入: nums = [2,2,3,4]
输出: 3
解释:有效的组合是:
2,3,4 (使用第一个 2)
2,3,4 (使用第二个 2)
2,2,3
"""
from typing import List


class Solution:
    def triangleNumber(self, nums: List[int]) -> int:

        """
        排序+双指针
        :param nums:
        :return:
        """
        nums.sort()
        ans = 0

        n = len(nums)

        for i in range(n):
            k = i + 1
            for j in range(i + 1, n):
                while k + 1 < n and nums[k + 1] < nums[i] + nums[j]:
                    k += 1
                if k - j < 0:
                    break
                ans += k - j
        return ans


s = Solution()
print(s.triangleNumber([0, 0, 0]))

# -*- coding: utf-8 -*-
# @Time    : 2022/7/18 10:26
# @Author  : zzw
# @File    : 2089. 找出数组排序后的目标下标
"""
给你一个下标从 0 开始的整数数组 nums 以及一个目标元素 target 。

目标下标 是一个满足 nums[i] == target 的下标 i 。

将 nums 按 非递减 顺序排序后，返回由 nums 中目标下标组成的列表。如果不存在目标下标，返回一个 空 列表。返回的列表必须按 递增 顺序排列。
"""
from typing import List


# 没有用到二分法
class Solution:
    def targetIndices(self, nums: List[int], target: int) -> List[int]:
        """
        输入：nums = [1,2,5,2,3], target = 2
        输出：[1,2]
        解释：排序后，nums 变为 [1,2,2,3,5]。
        满足 nums[i] == 2 的下标是 1 和 2。
        """
        start = 0
        ret_len = 0
        for num in nums:
            if num < target:
                start += 1
            elif num == target:
                ret_len += 1
        return list(range(start, start + ret_len))


s = Solution()
print(s.targetIndices([1, 2, 5, 2, 3], 2))

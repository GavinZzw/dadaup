# -*- coding: utf-8 -*-
# @Time    : 2022/7/25 17:27
# @Author  : zzw
# @File    : 1351. 统计有序矩阵中的负数.py
from typing import List


class Solution:
    def countNegatives(self, grid: List[List[int]]) -> int:
        """
        输入：grid = [[4,3,2,-1],[3,2,1,-1],[1,1,-1,-2],[-1,-1,-2,-3]]
        输出：8
        解释：矩阵中共有 8 个负数。

        :param grid:
        :return:
        """
        feifushu = 0
        m = len(grid)
        n = len(grid[0])
        l, r = 0, n - 1
        for row in range(m):
            l = 0
            while l < r:
                mid = (l + r + 1) // 2
                if grid[row][mid] < 0:
                    r = mid - 1
                else:
                    l = mid
            if r == 0 and grid[row][r] < 0:
                break
            feifushu += r + 1
        return m * n - feifushu


s = Solution()
print(s.countNegatives([[3,2],[1,0]]))

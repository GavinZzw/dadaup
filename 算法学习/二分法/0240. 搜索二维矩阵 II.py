# -*- coding: utf-8 -*-
# @Time    : 2022/10/8 16:33
# @Author  : zzw
# @File    : 0240. 搜索二维矩阵 II.py

"""
搜索 m x n 矩阵 matrix 中的一个目标值 target
每行的元素从左到右升序排列。
每列的元素从上到下升序排列。
"""
from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        """
        不是二分法
        :param matrix:
        :param target:
        :return:
        """
        m = len(matrix)
        n = len(matrix[0])

        x, y = 0, n - 1

        while x < m and y > 0:
            if matrix[x][y] == target:
                return True
            elif matrix[x][y] > target:
                y -= 1
            else:
                x += 1
        return False


s = Solution()
print(s.searchMatrix(
    [[1, 4, 7, 11, 15],
     [2, 5, 8, 12, 19],
     [3, 6, 9, 16, 22],
     [10, 13, 14, 17, 24],
     [18, 21, 23, 26, 30]], 17))

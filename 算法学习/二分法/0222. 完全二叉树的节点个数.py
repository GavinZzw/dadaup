# -*- coding: utf-8 -*-
# @Time    : 2022/10/8 15:07
# @Author  : zzw
# @File    : 0222. 完全二叉树的节点个数.py
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """
    二分法+位运算
    """

    def countNodes(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        # 计算层数
        level = 0
        tmp = root
        while tmp.left:
            level += 1
            tmp = tmp.left

        l, r = 2 ** level, 2 ** (level + 1) - 1
        while l < r:
            # 因为是找到第一个不存在的，所以向后取整
            mid = (l + r) // 2 + 1
            tmp = root
            # 二分法查找最后一层个数
            for c in bin(mid)[3:]:
                if c == "0":
                    tmp = tmp.left
                else:
                    tmp = tmp.right
            if tmp:
                l = mid
            else:
                r = mid - 1
        return l


s = Solution()
print(s.countNodes(TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3, TreeNode(6)))))

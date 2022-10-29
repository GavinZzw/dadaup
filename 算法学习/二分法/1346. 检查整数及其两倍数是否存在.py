# -*- coding: utf-8 -*-
# @Time    : 2022/7/20 10:18
# @Author  : zzw
# @File    : 1346. 检查整数及其两倍数是否存在.py

from typing import List


class Solution:
    def checkIfExist(self, arr: List[int]) -> bool:
        """
        输入：arr = [10,2,5,3]
        输出：true
        解释：N = 10 是 M = 5 的两倍，即 10 = 2 * 5 。
        """

        def find_target(arr, target):
            l = 0
            r = len(arr) - 1
            while l <= r:
                mid = (l + r) // 2
                if target == arr[mid]:
                    return True
                elif target < arr[mid]:
                    r = mid - 1
                else:
                    l = mid + 1
            return False

        arr.sort()
        for i in range(len(arr) - 1):
            if find_target(arr[:i] + arr[i + 1:], arr[i] * 2):
                return True
        return False


s = Solution()
print(s.checkIfExist([-10, 12, -20, -8, 15]))

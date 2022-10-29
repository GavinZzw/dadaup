# -*- coding: utf-8 -*-
# @Time    : 2022/10/20 14:47
# @Author  : zzw
# @File    : 0729. 我的日程安排表 I.py

"""
实现一个 MyCalendar 类来存放你的日程安排。如果要添加的日程安排不会造成 重复预订 ，则可以存储这个新的日程安排。

当两个日程安排有一些时间上的交叉时（例如两个日程安排都在同一时间内），就会产生 重复预订 。

日程可以用一对整数 start 和 end 表示，这里的时间是半开区间，即 [start, end), 实数 x 的范围为，  start <= x < end 。

实现 MyCalendar 类：

MyCalendar() 初始化日历对象。
boolean book(int start, int end) 如果可以将日程安排成功添加到日历中而不会导致重复预订，返回 true 。否则，返回 false 并且不要将该日程安排添加到日历中。

"""
import bisect


class MyCalendar:

    def __init__(self):
        self.slot = []

    def book(self, start: int, end: int) -> bool:
        # 计算start插入在有序日程数组位置
        i = bisect.bisect_right(self.slot, start)
        # i是偶数表示start可以插入，i是奇数表示start插入在原有日程之中，然后再判断end是否可以插入在下一个日程之前
        if i & 1 or (i < len(self.slot) and self.slot[i] < end):
            return False
        self.slot[i:i] = [start, end]
        return True


s = MyCalendar()
print(s.book(47, 50))
print(s.book(33, 41))
print(s.book(39, 45))
print(s.book(33, 42))
print(s.book(25, 32))
print(s.book(26, 35))
print(s.book(19, 25))
print(s.book(3, 8))
print(s.book(8, 13))
print(s.book(18, 27))

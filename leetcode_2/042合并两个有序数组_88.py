from typing import List
"""
给你两个按 非递减顺序 排列的整数数组 nums1 和 nums2
另有两个整数 m 和 n ，分别表示 nums1 和 nums2 中的元素数目

请你 合并 nums2 到 nums1 中，使合并后的数组同样按 非递减顺序 排列。

注意：最终，合并后数组不应由函数返回，而是存储在数组 nums1 中
为了应对这种情况，nums1 的初始长度为 m + n
其中前 m 个元素表示应合并的元素，后 n 个元素为 0 ，应忽略。nums2 的长度为 n 
"""


#1.我是否可以直接合并两个区间，然后 sort 排序呢-->可以但实际不推荐
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        nums1[m:]=nums2
        nums1.sort()



#2.正规解法：双指针
class Solution1:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        x=m-1
        y=n-1
        last=m+n-1

        while x>=0 and y>=0:
            if nums1[x]>nums2[y]:
                nums1[last]=nums1[x]
                x-=1
            else:
                nums1[last]=nums2[y]
                y-=1
            last-=1


        # 如果nums1的元素用完了，nums2里面还有剩下的更小的元素，直接放前面
        while y>=0:
            nums1[last]=nums2[y]
            last-=1
            y-=1

"""
我的想法：从两个数组开头开始用指针来比大小，用一个temp来记录被替换的数字，从前往后遍历
正确解法：从数组开头太麻烦，既然提示了（合并后数组不应由函数返回，而是存储在数组 nums1 中，nums1 的初始长度为 m + n）
为什么不从两个数列的末尾开始往前遍历呢

总结易错点：
1. while y>=0:
得处理nums2比nums1更长的情况

2、>=
要考虑能否取到0，一个元素出错则整个结果出错
"""
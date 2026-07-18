from typing import List
'''差分数组'''

#1.自然而然的想法
class Solution:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        answer=[0]*n
        for first,last,seats in bookings:
            for i in range(first-1,last):
                answer[i]+=seats

        return answer
'''
当last,seats到一两万或者更大的数，会超时
answer 数组的每一个元素都要被不断遍历，每一次遍历是因为 booking 的更新
'''


"""当一个区间要进行大量计算（这里是累加到同样的数）-->联想差分数组"""
#2.差分数组
class Solution1:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        diff=[0]*(n+1)
        for first,last,seats in bookings:
            diff[first-1]+=seats
            diff[last]-=seats

        answer=[0]*n
        last_seats=0
        for i in range(n):
            answer[i]=last_seats+diff[i]
            last_seats=answer[i]

        return answer

"""
能更为简单的原因是只记录上下车的站（类似公交车）
lastseats 的作用类似于前缀和
diff（计算每一个站上下车的人数，记录相邻站点的人数差值，也是一个数组，第一个循环就在计算每一个 diff）
最后利用每一个前缀和和记录的diff，算出每一个 answer 数组元素
"""

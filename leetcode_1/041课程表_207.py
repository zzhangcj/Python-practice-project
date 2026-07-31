from typing import List
from collections import deque

"""
1、这道题怎么想到思路呢？
看到「先修依赖、先后顺序、判断能否全部完成」→ 本质是判断有向图是否存在环

2、有向图涉及哪些知识点呢
有向图、环的概念
拓扑排序
邻接表存图
入度数组

3、什么是拓扑排序
对有向无环图（DAG）的所有节点排序得到
满足：任意一条边 a→b，排序结果中 a 一定出现在 b 前面
核心作用：
    处理有依赖关系的任务调度（如课程安排、编译顺序）
    用来判断图中是否有环：能排完所有节点 = 无环；排不完 = 有环
"""
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        #构造邻接表
        graph=[[] for _ in range(numCourses)]
        #构造入度表
        indegree=[0]*numCourses
        #遍历边列表
        for after,pre in prerequisites:
            graph[pre].append(after)#记录节点出度指向谁
            indegree[after]+=1#记录节点入度次数
        #初始化队列
        queue=deque()
        for i in range(numCourses):
            if indegree[i]==0:
                queue.append(i)
        #while循环处理图
        while queue:
            cur_class=queue.popleft()
            for after in graph[cur_class]:
                indegree[after]-=1
                if indegree[after]==0:
                    queue.append(after)
        #判断是否完成所有课程的学习
        for item in indegree:
            if item!=0:
                return False
        return True
"""

1、拓扑排序固定套路


2、什么是入度表和邻接表，有什么用
边列表prerequisites
    由题目可得，记录每个节点之间的出入度关系
入度表indegree
    由边列表得到，用来找到哪个节点是可消除的
邻接表graph
    由边列表得到，消除节点后，判断哪些节点入度受到影响，并更新情况

为什么要使用入度表和邻接表
    （1）入度表 indegree：记录入度数量，每个节点有多少个前置依赖
    用来消除节点，即消除入度为0的节点
    （2）邻接表 graph：记录出度情况，每个节点指向哪些后继节点
    当前课程学完后(节点消除后)，能快速找到它影响的所有后续课程，批量更新它们的入度(看哪些受到了影响)

3、为什么需要一个队列
    （1）先把所有入度为 0 的节点入队（当前可以直接学的课）
    （2）每次出队一个节点（学完这门课），将它所有后继节点的入度 -1
    （3）后继节点入度变为 0 → 入队（现在解锁，可以学了）
    关键-->队列用来按顺序处理「当前可执行的节点」，保证按依赖层序推进。

4、区分两种列表
indegree = [0] * n
    一维列表 n=3 → [0, 0, 0]
graph = [[] for _ in range(n)]
    二维列表 n=3 → [[], [], []]

5、为什么是for after,pre in prerequisites:
注意审题，先修课程对 [0, 1] 表示：想要学习课程 0 ，你需要先完成课程 1
即[0,1]表示的依赖关系是1->0

"""
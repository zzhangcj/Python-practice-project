"""单调栈"""
from multiprocessing.connection import answer_challenge

"""
给定一个整数数组 temperatures ，表示每天的温度
返回一个数组 answer ，其中 answer[i] 是指对于第 i 天
下一个更高温度出现在几天后。
如果气温在这之后都不会升高，请在该位置用 0 来代替
"""
from typing import List
"""
什么时候用单调栈

当你看到当前的值处理结果需要往后的信息
--> 打包当前信息来增援未来（有记忆功能的数据结构都可以这么说，比如哈希表这些）
-->找左右两侧最近的更大 / 更小元素 
-->需要不断弹出栈顶不符合条件的旧元素，维持有序序列
"""

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        stack=[]
        n = len(temperatures)
        answer = [0]*n

        for i in range(n):
            cur_temperature = temperatures[i]
            while stack and cur_temperature > temperatures[stack[-1]]:
                    #比较当前温度和历史温度
                    pre_idx=stack.pop()
                    answer[pre_idx]=i-pre_idx

            stack.append(i)
        return answer


"""
1.while 循环的简写
正常思路的while循环如下：
while True:
    #比较当前温度和历史温度
    if cur_temperature > temperatures[stack[-1]] and stack!=[]:
        pre_idx=stack.pop()
        answer[pre_idx]=i-pre_idx
    else: #如果不满足条件，不能填写answer
        break #
        
总结什么时候可以简写while循环：
循环终止条件只有一个判断分支
循环内只有「满足条件就执行操作，不满足直接break退出」，没有多层 else 嵌套、没有多个分支逻辑；

如果循环里有多个分支、需要多层判断，就不能简写

        
2.为什么最后没有上升的地方，不用补0
因为创造的answer = [0]*n -->原本就是0，前面做修改就是在原本为0的answer的基础上

3.while stack and cur_temperature > temperatures[stack[-1]]:
注意（1）stack里面存储的是下标i，由stack.append(i)可知
（2）两个条件的顺序不能错
-->stack 为空时，and 直接终止判断，不会执行 temperatures[stack[-1]]，避免报错；
若先写数值对比再判断栈非空，会触发索引报错。
"""


"""栈"""

"""
stack栈，在python中用列表表示

✅ 有参数时，pop(n) 会按照索引n删除元素；
✅ 没有参数时，pop() 默认删除最后一个元素；
队列是后进先出的
-->用append方法来添加元素
-->用pop方法来删除元素
"""


class Solution:
    def isValid(self, s: str) -> bool:
        stack=[]
        mapping={")":"(","]":"[","}":"{"}
        for char in s: #找左括号
            if char in {"(","[","{"}:
                stack.append(char)
            else: #右括号匹配
                # 要判断栈是否为空
                if not stack: #等价于if stack==[]:
                    return False

                #如果栈里有元素
                top_ele=stack.pop()
                if mapping[char]!=top_ele:
                    return False

        if stack: #这里是为了判断栈里面是否还有剩余
            return False #有剩余说明还有左括号有多余的
        else:
            return True

"""
总结：如何想到要用栈的方法来解决问题
1.当题目出现对称结构
2.出现配队，两两消除的
3.先进后出的，后进先出的

补充：
4.找下一个更大 / 更小、区间最值 → 单调栈
5.多层嵌套、由内向外计算 → 普通栈
比如：3[a2[bc]] 字符串解码，内层bc先计算，再处理外层 a，最后处理 3 倍整体
6.栈由于先进后出的特点可以完成反序的功能
"""
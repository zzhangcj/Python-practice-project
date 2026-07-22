

class Solution:
    def decodeString(self, s: str) -> str:
        stack=[]
        current_num=0

        for char in s:
            if char.isdigit(): #如果char是数字
                current_num=current_num*10+int(char)
            elif char=="[": #遇到左括号，括号前完整数字存入栈
                stack.append(current_num)
                current_num=0 #清空记好的数字，用于下一个数字记录
                stack.append("[")
            elif char=="]":
                sub_str=[]
                while stack[-1]!="[":
                    sub_str.append(stack.pop())

                sub_str.reverse()
                inner_str="".join(sub_str)
                stack.pop()#弹出左括号
                repeat_time=stack.pop()#记录要乘的数字
                stack.append(inner_str*repeat_time) #结果再重新入栈

            else: #如果char为字母
                stack.append(char)

        return "".join(stack)

"""
关键注意点
1.数字可能是多位数，不能只读取单个字符，用 current_num = current_num*10 + int(char) 拼接数值。
2.栈中统一存放字符串；收集到括号内字符后，先用 join 转为字符串，再做重复运算，禁止直接把列表压栈（防止 ""join() 类型报错）。
即使用join拼接元素时，元素中不能有列表

3.碰到 [：先压入倍数，再压入标记 [；重置数字缓存。
4.碰到 ]：持续弹出字符直到遇见 [，反转拼接出括号内文本；弹出 [、弹出重复次数，文本重复后重新入栈。
5.普通字母直接入栈；循环结束后，把栈内所有字符串拼接得到最终答案。

"""
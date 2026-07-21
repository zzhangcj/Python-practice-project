"""
设计一个支持 push ，pop ，top 操作，并能在常数时间内检索到最小元素的栈。

实现 MinStack 类:

MinStack() 初始化堆栈对象。
void push(int value) 将元素 value 推入堆栈。
void pop() 删除堆栈顶部的元素。
int top() 获取堆栈顶部的元素。
int getMin() 获取堆栈中的最小元素。
"""




class MinStack:

    def __init__(self):
        self.data_stack=[] #用来存数据，没什么排序
        self.min_stack=[] #辅助栈，存两个栈之间同一层级最小的元素放在栈顶

    def push(self, value: int) -> None:
        self.data_stack.append(value)
        if self.min_stack: #min_stack里面有元素的时候
            top=self.min_stack[-1]
            min_value=min(value,top)#同一层级把最小的放在min_stack的栈顶
            self.min_stack.append(min_value)
        else: #当开始的时候min_stack里面还没有元素
            self.min_stack.append(value)

    def pop(self) -> None:
        self.data_stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.data_stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]

# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(value)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
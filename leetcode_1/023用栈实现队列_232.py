"""
请你仅使用两个栈实现先入先出队列。队列应当支持一般队列支持的所有操作（push、pop、peek、empty）：

实现 MyQueue 类：

void push(int x) 将元素 x 推到队列的末尾
int pop() 从队列的开头移除并返回元素
int peek() 返回队列开头的元素
boolean empty() 如果队列为空，返回 true ；否则，返回 false

假设所有操作都是有效的 （例如，一个空的队列不会调用 pop 或者 peek 操作）

"""


class MyQueue:

    def __init__(self):
        self.in_stack=[]
        self.out_stack=[]

    def push(self, x: int) -> None:
        self.in_stack.append(x)

    def pop(self) -> int:
        if self.out_stack:#out_stack里面有东西
            return self.out_stack.pop()
        else: ##out_stack里面为空
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
            return self.out_stack.pop()

    def peek(self) -> int:
        if self.out_stack:
            return self.out_stack[-1]
        else:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
            return self.out_stack[-1]

    def empty(self) -> bool:
        if self.in_stack or self.out_stack:
            return False
        else:
            return True

# Your MyQueue object will be instantiated and called as such:
# obj = MyQueue()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.peek()
# param_4 = obj.empty()

'''
关键：
1.只有 out_stack 彻底空的时候，才能搬运 in_stack 的数据！
2.pop 和 peek 逻辑高度相似：都要先保证 out_stack 有数据，区别只是 pop 弹出，peek 只看栈顶 
3.empty 判断：两个栈同时为空，队列才是空，注意用or 还是 and
'''
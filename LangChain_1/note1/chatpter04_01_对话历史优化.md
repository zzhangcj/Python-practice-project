# 1.6.2 对话历史优化 + 1.6.3多轮对话聊天机器人
## 问题背景
大模型多轮对话时，**每一轮都要把全部历史消息传给模型**。对话轮次变多，消息列表会越来越长。
- 坏处1：token消耗变多，调用花钱更多
- 坏处2：上下文窗口占满，会报错、或者模型性能下降

> 错误示范（非常容易踩坑）
```python
conversation = []
conversation.append({"role": "user", "content": "问题1"})
response1 = model.invoke(conversation)
# ❗错误：忘记把AI返回结果存入conversation
conversation.append({"role": "user", "content": "问题2"})
response2 = model.invoke(conversation)
```
问题：历史里面只有用户的两句话，**没有AI的回答**。模型看不到自己上一轮输出，上下文断裂，会失忆。

✅正确示范：**每一轮必须同时保存用户提问 + AI回复**
```python
conversation = []
# 第一轮
conversation.append({"role": "user", "content": "我叫张三"})
response1 = model.invoke(conversation)
# ✅关键：把assistant的回答加入历史列表
conversation.append({"role": "assistant", "content": response1.content})

# 第二轮，完整历史全部传给模型
conversation.append({"role": "user", "content": "我叫什么？"})
response2 = model.invoke(conversation)
```
> 此时模型能读到：system、用户：我叫张三、AI的回答、用户：我叫什么？，所以可以记住名字。

---

## 滚动窗口裁剪函数 keep_recent_messages
> 只使用字典格式消息 `{"role":"xxx","content":"xxx"}`，不要和LangChain的`HumanMessage/AIMessage`对象混用。

```python
def keep_recent_messages(messages, max_pairs=3):
    """
    保留最近的 N 轮对话
    max_pairs: 保留的对话轮数，1轮 = user(用户) + assistant(AI)两条消息
    """
    # 1.把system系统提示消息 和普通聊天消息分离开
    system_msgs = [m for m in messages if m.get("role") == "system"]
    conversation_msgs = [m for m in messages if m.get("role") != "system"]
    
    # 2.截取最近 max_pairs*2 条普通对话
    # 每一轮是2条消息(user+assistant)，max_pairs轮就需要 2*max_pairs条
    recent_msgs = conversation_msgs[-(max_pairs * 2):]
    
    # 3.拼接：永远保留system，拼接裁剪后的最近对话，返回新列表
    return system_msgs + recent_msgs
```
### 逐行通俗解析
1. `m.get("role")`：字典取值，拿到消息角色，`system/user/assistant`
2. `system_msgs`：过滤提取所有system消息，**角色设定永远不能丢**，丢了模型就忘记身份。
3. `conversation_msgs`：剩下全部是用户、AI的聊天记录。
4. 切片语法 `list[-N:]`：取列表**倒数N个元素**。
`conversation_msgs[-(max_pairs * 2):]`：拿到最晚的N轮对话。
> 例子max_pairs=2：取倒数4条消息，刚好2组（user+assistant）。
5. 返回新列表：`system消息 + 裁剪后的聊天记录`。旧的更早对话直接丢弃。

> ⚠️注意：这个函数返回**新列表**，不会修改传入的原始messages。原始long_conversation还是完整全部历史。

---

## 完整业务测试代码
```python
# 初始化历史，system角色提示
long_conversation = [
    {"role": "system", "content": "你是 Python 导师"}
]

# 第1轮对话
long_conversation.append({"role": "user", "content": "什么是列表？用一句解释"})
r1 = model.invoke(long_conversation)
long_conversation.append({"role": "assistant", "content": r1.content})

# 第2轮对话
long_conversation.append({"role": "user", "content": "列表和元组有什么区别？用一句解释"})
r2 = model.invoke(long_conversation)
long_conversation.append({"role": "assistant", "content": r2.content})

# 第3轮对话
long_conversation.append({"role": "user", "content": "什么是字典呢？用一句解释"})
r3 = model.invoke(long_conversation)
long_conversation.append({"role": "assistant", "content": r3.content})

print(f"原始消息数: {len(long_conversation)}")
# 优化：只保留最近2轮对话
optimized = keep_recent_messages(long_conversation, max_pairs=2)
print(f"优化后消息数: {len(optimized)}")
print(f"保留的内容: system + 最近2轮对话")

# 在裁剪后的历史上继续提问
optimized.append({"role": "user", "content": "我第一个问题问的是什么？"})
response = model.invoke(optimized)
print(f"\nAI 回复: {response.content}")
```

### 运行输出
```
原始消息数: 7
优化后消息数: 5
保留的内容: system + 最近2轮对话
AI 回复: 你第一个问题问的是：**“列表和元组有什么区别？用一句解释”**
```

## 一步步拆解数字与消息内容
原始`long_conversation`一共7条消息：
1. system：你是Python导师
2. user：什么是列表？用一句解释  ←第1轮user（会被裁剪丢掉）
3. assistant：（AI回答列表） ←第1轮ai（会被裁剪丢掉）
4. user：列表和元组有什么区别？用一句解释 ←第2轮user（保留）
5. assistant：（AI回答列表元组） ←第2轮ai（保留）
6. user：什么是字典呢？用一句解释 ←第3轮user（保留）
7. assistant：（AI回答字典） ←第3轮ai（保留）

`max_pairs=2`，保留最近2轮，也就是取聊天消息倒数4条：4、5、6、7。
拼接system消息 → 优化后一共 `1+4 =5`条消息，对应输出`优化后消息数:5`。

> 第一轮（2、3号消息）被彻底删掉了！模型看不到最早的“什么是列表？”这个问题。
所以当问：`我第一个问题问的是什么？`，模型眼里最早看到的问题是【列表和元组有什么区别】，所以输出这个答案。

## 初学者必懂关键点总结
1. 多轮对话本质：**把完整消息列表传给模型**，模型靠列表读懂上下文记忆。
2. 每一轮结束，**必须append user提问和assistant回答，缺一不可**，否则失忆。
3. 窗口裁剪逻辑：
   - system角色提示永远保留，不能删
   - 每一轮对话 = user + assistant两条消息
   - 使用列表切片取倒数N组，丢弃老旧消息，减少token消耗
4. 副作用：裁剪掉的历史模型彻底看不见，会“忘记更早的对话”。
5. 原始列表不会被修改，`keep_recent_messages`返回一份裁剪后的新列表，后续新提问要追加到`optimized`，不要追加到老的long_conversation。

## 补充思考（面试常问）
> 这种方案叫**固定轮数滑动窗口**。
缺点：不管每句话长短，固定按轮数删；如果单条消息特别长，依然会超token。进阶方案：按token总长度裁剪，而不是按对话轮数裁剪。

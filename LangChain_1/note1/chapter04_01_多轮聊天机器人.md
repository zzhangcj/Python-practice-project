# 多轮聊天机器人核心笔记
## 常量定义
```python
MODEL_NAME = "deepseek-v4-flash"
MAX_PAIRS_HISTORY = 10   # 最大保留10轮对话，1轮=user+assistant两条消息
EXIT_WORD = "quit"       # 程序退出关键词
print(model.invoke("你好")) # API连通性测试
```

## messages消息列表（核心内存）
```python
messages = [
    {
        "role":"system",
        "content":"你是小谷姐姐，尚硅谷教育的数字员工，也是一名耐心、友好的智能助手。我会用自然、清晰的方式回答用户问题。"
    }
]
```
- `messages`：保存**全部完整对话历史**，不会被裁剪
- `system`角色：设定AI身份，滑动窗口函数会强制保留，不可丢失
- 3种role：`system`角色设定、`user`用户提问、`assistant`AI回答
- ✅底层原理：**大模型本身无记忆，上下文完全依靠手动维护消息列表**

## 启动提示
```python
print(f"✨ 请输入问题，输入 {EXIT_WORD} 结束对话\n")
```

## while True 主循环
1. `while True`：无限循环，`break`才退出程序
2. `input()`：接收控制台用户输入
3. 退出判断：`user_input.lower()`统一小写，兼容大小写输入，匹配`EXIT_WORD`执行break

### 一轮对话完整流程
1. `messages.append({"role":"user","content":user_input})`
> 将用户提问存入完整历史列表

2. 流式输出准备
```python
print("🧚 小谷姐姐：", end="", flush=True)
reply_content = ""
```
- `end=""`：取消print自动换行
- `flush=True`：强制刷新缓冲区，实现实时打字效果
- `reply_content`：拼接流式返回的分片内容

3. 历史滑动窗口裁剪
```python
memory_messages = keep_recent_messages(messages,max_pairs = MAX_PAIRS_HISTORY)
```
|变量|用途|
|----|----|
|messages|本地保存全部会话，不直接传给模型|
|memory_messages|裁剪后的临时副本，真正发给大模型|

> 本地留存全部记录，模型只接收最近N轮，控制token消耗，防止上下文溢出

4. stream流式请求模型
```python
for chunk in model.stream(memory_messages):
    if chunk.content:
        print(chunk.content, end="", flush=True)
        reply_content += chunk.content
```
- `stream()`：边生成边返回分片`chunk`，实现打字机效果；对比`invoke()`一次性返回完整结果
- 需要手动拼接`chunk.content`得到完整AI回复

5. 保存AI回复
```python
messages.append({"role":"assistant","content":reply_content})
```
> ⭐高频易错点：必须存入assistant消息，否则下一轮对话模型失忆

## 依赖函数 keep_recent_messages
```python
def keep_recent_messages(messages, max_pairs=10):
    system_msgs = [m for m in messages if m.get("role") == "system"]
    conversation_msgs = [m for m in messages if m.get("role") != "system"]
    recent_msgs = conversation_msgs[-(max_pairs * 2):]
    return system_msgs + recent_msgs
```

## 重要易错点
1. 不要忘记追加`assistant`消息，会造成模型失忆
2. 消息要添加到原始`messages`，不要加到临时变量`memory_messages`
3. 流式输出必须：`end=""` + `flush=True`，手动拼接分片
4. 当前方案：**按轮数裁剪**；短板：长文本场景仍可能超上下文，进阶可改为按token数量裁剪
5. 一轮完整对话：`user消息 ↔ assistant消息`成对出现
```
用户输入 → 存入user → 裁剪历史 → stream调用模型 → 拼接回复 → 存入assistant → 等待下一轮输入
```

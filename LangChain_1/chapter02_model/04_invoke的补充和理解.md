# 补充1：invoke()的参数

> **一句话定义**：启动组件干活的**同步调用方法**，大模型、提示模板、Chain 链条通用。
> 
> **通俗类比**：微波炉的「启动按钮」——按下的同时告诉它：加热什么、加热多久、到什么程度停。

---

## 一、核心参数总览

| 参数 | 类型 | 传给谁 | 作用 | 新手是否常用 |
| :--- | :--- | :--- | :--- | :---: |
| `input` | 字符串 / 字典 / 列表 | 大模型 / 组件 | **要处理的原始输入数据** | ✅ 必传 |
| `config` | `RunnableConfig` | LangChain 框架 | 控制框架行为（超时、日志、回调） | ❌ 几乎不用 |
| `stop` | `list[str]` | 大模型 | 遇到指定文字立刻停止输出 | ⭕ 偶尔用 |
| `**kwargs` | 关键字参数 | 大模型 | 控制生成效果（温度、最大长度等） | ✅ 常用 |

---

## 二、参数详解

### 1. `input` —— 给 AI 的原材料（必传）

- **直接调用大模型**：传字符串
  ```python
  llm.invoke(input="解释一下什么是大模型")
  ```

- **调用 Chain 链条**：传字典，用于填充模板变量
  ```python
  chain.invoke({"question": "什么是 Ollama？"})
  ```

> 💡 记忆：`input` = 你要 AI 处理的「问题 / 数据」。

---

### 2. `config` —— 管框架，不管 AI

这个参数**不会发给大模型**，只控制 LangChain 框架本身的行为：
- `timeout`：超时时间，防止程序卡死
- `callbacks`：回调函数，打印日志、追踪耗时
- `metadata`：自定义标记，方便调试和监控

```python
# 新手写法：直接忽略，或填 None
llm.invoke("你好", config=None)
```

> 💡 记忆：`config` = 微波炉的「蜂鸣声、自动断电」设置，不改变食物本身。

---

### 3. `stop` —— 停止词，让 AI 闭嘴

列表格式。AI 输出内容一旦命中列表中的文字，**立刻截断返回**，不再往下写。

```python
llm.invoke(
    "按要点回答，用 ### 分隔",
    stop=["###", "\n\n"]  # 遇到 ### 或两个换行就停止
)
```

**用途**：强制控制输出格式，防止 AI 废话太多、脑补多余内容。

---

### 4. `**kwargs` —— 控制 AI 说话风格（最重要）

直接写在 `invoke` 括号里，**不要放进 `config`**。这些参数会真正透传给大模型。

| 常用参数 | 取值范围 | 作用 |
| :--- | :--- | :--- |
| `temperature` | `0 ~ 1` | 越小越严谨、越确定；越大越发散、越有创意 |
| `num_predict` | 整数 | 限制最大输出 token 数，防止输出过长 |
| `num_ctx` | 整数 | 设置上下文窗口大小 |

```python
llm.invoke(
    "写一段 Python 代码",
    temperature=0.2,   # 严谨模式，适合写代码
    num_predict=512    # 最多输出 512 个 token
)
```

> ⚠️ **易错点**：`temperature` 这类模型参数要直接写在 invoke 里，不能塞进 `config`。

---

## 三、三个容易混淆的方法

| 方法 | 特点 | 适用场景 |
| :--- | :--- | :--- |
| **`.invoke()`** | 同步阻塞，全部生成完一次性返回完整结果 | 普通脚本、简单调用（新手首选） |
| **`.stream()`** | 流式输出，文字一个一个蹦出来 | 聊天界面、打字机效果 |
| **`.ainvoke()`** | 异步调用 | Web 后端、高并发服务（初学者暂不用） |

---

## 四、最简可运行示例

```python
from langchain_ollama import OllamaLLM

# 1. 加载本地模型
llm = OllamaLLM(model="qwen3:4b")

# 2. 调用模型干活
response = llm.invoke(
    input="用一句话解释什么是大模型",
    stop=["###"],
    temperature=0.2,
    num_predict=300
)

# 3. 打印结果
print(response)
```

---

## 五、高频踩坑提醒

1. ❌ 不要把 `temperature` 放进 `config`，模型参数直接写在 invoke 外层。
2. ❌ `invoke` 是阻塞同步的，回答很长时代码会卡住等待。
3. ✅ 写小脚本优先用 `invoke`，简单直接。

---

---

# 补充2：Chat 模型 invoke() 三种输入方式

> **核心结论**：聊天模型的 `invoke()` 支持三种输入格式，效果完全相同，只是写法和适用场景不同。
> 
> 日常开发 **优先选「字典列表」**，最通用、最灵活。

---

## 一、三种方式总览对比

| 输入方式 | 写法形式 | 能否设置 system | 能否带对话历史 | 能否序列化为 JSON | 代码量 | 推荐场景 |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **① 纯文本** | 直接传字符串 | ❌ | ❌ | — | 最少 | 快速测试、一次性简单提问 |
| **② 字典列表** ⭐ | `[{"role": "...", "content": "..."}]` | ✅ | ✅ | ✅ | 中等 | **生产环境、日常开发首选** |
| **③ 消息对象列表** | `SystemMessage() / HumanMessage() / AIMessage()` | ✅ | ✅ | ❌ | 最多 | 大型项目、需要类型检查 |

---

## 二、三种方式详解

### 方式 1：纯文本输入（最简单）

直接把问题字符串传给 `invoke()`，LangChain 会自动转成 `user` 消息发给模型。

```python
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

load_dotenv(override=True)

model = init_chat_model(
    model="openai:gpt-5.4-mini",
    api_key=os.getenv("CLOSEAI_API_KEY"),
    base_url=os.getenv("CLOSEAI_BASE_URL")
)

# 直接传字符串
response = model.invoke("翻译成英文：你好世界")
print(response.content)
```

**优点**：代码最短，一行写完。  
**缺点**：无法设置系统提示（system prompt），无法传递对话历史。  
**适用**：快速测试、不需要上下文的简单生成任务。

---

### 方式 2：字典列表（⭐ 生产推荐）

用字典组成消息列表，每条消息包含 `role`（角色）和 `content`（内容）。

**三种角色：**

| 角色 | 英文 | 作用 | 示例 |
| :--- | :--- | :--- | :--- |
| 系统 | `system` | 设定 AI 的身份、行为、规则 | "你是一个专业的 Python 导师" |
| 用户 | `user` | 用户的输入 / 问题 | "什么是装饰器？" |
| 助手 | `assistant` | AI 的历史回复（用于对话上下文） | "装饰器是一种设计模式..." |

**基本格式：**

```python
messages = [
    {"role": "system", "content": "系统提示"},
    {"role": "user", "content": "用户消息"},
    {"role": "assistant", "content": "AI 回复"},  # 可选，用于对话历史
    {"role": "user", "content": "继续提问"}
]
```

**示例 1：设置系统提示**

```python
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

load_dotenv(override=True)

model = init_chat_model(
    model="gpt-5.4-mini",
    model_provider="openai",
    api_key=os.getenv("CLOSEAI_API_KEY"),
    base_url=os.getenv("CLOSEAI_BASE_URL")
)

messages = [
    {"role": "system", "content": "你是一个专业的数学老师。"},
    {"role": "user", "content": "什么是斐波那契数列？"}
]

response = model.invoke(messages)
print(f"AI 的回复：{response.content}")
```

**示例 2：多轮对话（带历史记忆）**

```python
messages = [
    {"role": "system", "content": "你是一个专业的数学老师。"},
    {"role": "user", "content": "2 + 3 * 2 = ？"},
    {"role": "assistant", "content": "8"},
    {"role": "user", "content": "我刚才问了什么问题？"}
]

response = model.invoke(messages)
print(f"AI 的回复：{response.content}")
# 输出：你刚才问的是："2 + 3 * 2 = ？"
```

> 💡 **关键认知**：大模型本身**没有记忆**。
> 不传历史消息 → AI 直接「失忆」；
> 把完整历史塞进消息列表 → AI 就能记住上下文。

**示例 3：手动维护对话历史**

```python
# 初始化对话列表
conversation = [
    {"role": "system", "content": "你是一个非常友好的 AI 助手"},
    {"role": "user", "content": "你好，我叫小明"}
]

# 第一次对话
response1 = model.invoke(conversation)
print(f"AI 回复 1：{response1.content}")

# 把 AI 回复和新问题追加进列表，手动维护记忆
conversation.append({"role": "assistant", "content": response1.content})
conversation.append({"role": "user", "content": "我叫什么名字？"})

# 第二次对话（带上完整历史）
response2 = model.invoke(conversation)
print(f"AI 回复 2：{response2.content}")
# 输出：你叫小明。
```

**优点**：可设置 system、可携带多轮历史、JSON 兼容、易于序列化和网络传输。  
**缺点**：代码稍多（但更清晰）。  
**适用**：生产环境、实际项目、日常开发 **首选**。

---

### 方式 3：消息对象列表

使用 LangChain 内置的消息类（`SystemMessage`、`HumanMessage`、`AIMessage`）构建消息。

**消息类型对照：**

| 消息类 | 对应字典格式 | 作用 |
| :--- | :--- | :--- |
| `SystemMessage` | `{"role": "system", ...}` | 系统提示 |
| `HumanMessage` | `{"role": "user", ...}` | 用户输入 |
| `AIMessage` | `{"role": "assistant", ...}` | AI 回复 |

**示例：**

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

load_dotenv(override=True)

model = init_chat_model(
    model="openai:gpt-5.4-mini",
    api_key=os.getenv("CLOSEAI_API_KEY"),
    base_url=os.getenv("CLOSEAI_BASE_URL")
)

messages = [
    SystemMessage("你是一个专业的数学老师。"),
    HumanMessage("2 + 3 * 2 = ？"),
    AIMessage("8"),
    HumanMessage("我刚才问什么问题了？")
]

response = model.invoke(messages)
print(f"AI 的回复：{response.content}")
```

**多轮对话追加：**

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

messages = [
    SystemMessage(content="你是一个 Python 专家"),
    HumanMessage(content="什么是生成器？"),
]

response = model.invoke(messages)

# 继续对话：追加 AI 回复和新问题
messages.append(AIMessage(content=response.content))
messages.append(HumanMessage(content="能给个例子吗？"))

response2 = model.invoke(messages)
print(response2.content)
```

**优点**：IDE 自动补全、类型检查、大型项目不容易写错。  
**缺点**：代码较长、不如字典简洁、难以直接序列化为 JSON。  
**适用**：大型工程、需要静态类型检查的场景。

---

## 三、返回值说明

`invoke()` 返回的**不是普通字符串**，而是一个 `AIMessage` 对象。

```python
response = model.invoke(messages)

print(response)          # 打印完整对象（含元数据），不是纯文字
print(response.content)  # ✅ 真正拿到 AI 回答的文本字符串
```

- `response.content`：AI 回答的纯文本内容 → **日常 99% 的情况只用这个**
- 对象内部还包含 token 消耗、模型参数等元数据 → 调试、统计时才用到

---

## 四、记忆要点速查

1. **三种输入方式效果等价**，只是写法和适用场景不同。
2. **日常开发优先选「字典列表」**，最通用、最灵活。
3. **大模型没有自带记忆**，对话历史必须手动塞进消息列表传给 `invoke()`。
4. **返回值是 `AIMessage` 对象**，用 `.content` 提取回答文本。
5. **纯文本写法只能临时测试**，不能设置 system，不适合多轮对话。

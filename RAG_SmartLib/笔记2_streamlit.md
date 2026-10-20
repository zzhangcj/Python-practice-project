# 一、streamlit的安装与使用

## 1.安装streamlit

终端：pip install streamlit -i [https://pypi.tuna.tsinghua.edu.cn/simple](https://pypi.tuna.tsinghua.edu.cn/simple)

创建streamlit_app.py文件

```python
import streamlit as st
def main():
    st.header("hello world")
if __name__ == "__main__":
    main()
```

header的作用：
	在网页页面渲染一级标题，是 Streamlit 内置组件，直接生成大标题文本

## 2.标题

```python
def main():
    # st.header("📚图书智能检索系统")
    st.markdown('<h1 class="main-header">📚图书智能检索系统</h1>',unsafe_allow_html=True)
```

同时在st.markdown里面导入css代码

```python
st.markdown("""这里是css代码""", unsafe_allow_html=True)
```

（1）st.markdown的作用
	渲染 Markdown 文本，支持 markdown 语法；开启参数后，还可以解析 HTML 标签。

（2）unsafe_allow_html=True的作用
	默认情况下 streamlit 禁止 html 代码渲染，这个参数开启 HTML 解析权限

总结：可以通过markdown去写原生的HTML语句

---

# 二、streamlit创建侧边栏

## 1.文档查阅

去streamlit官网 -> 上面Docs
 -> 搜索sidebar
 -> 搜索text_input

```python
def main():
	.......
    #侧边栏
    with st.sidebar:
        st.header("⚙️ 系统配置")
        st.text_input(
            "🔑 Deepseek API密钥",
            value="",
        )
```

（1）st.sidebar
	Streamlit 内置侧边栏容器。
	`with st.sidebar:` 上下文管理器，with 内部所有 UI 元素，全部放到页面左侧侧边栏里

（2）st.text_input
	单行文本输入框组件。第一个参数是输入框的提示标签；`value=""`是输入框默认初始内容

## 2.读取.env 配置函数 getEnvInfo

```python
def getEnvInfo(key):
    env_file = Path(".env")
    env_lines=[]
    env_res=None
    if env_file.exists():
        with open(env_file, "r",encoding='utf-8') as f:
            env_lines = f.readlines()
        #查找对应的配置项
        for i,line in enumerate(env_lines):
            if line.strip().startswith(f"{key}="):
               env_res = line.strip().split("=")[1]
    if env_res is None:
        raise ValueError(f"找不到环境变量 {key}，检查.env文件")
    return env_res
```

作用：
	接收环境变量名称`key`，读取项目根目录的`.env`文件，检索对应的配置值；如果找不到该配置，直接抛出异常提示

（3）

```python
    #侧边栏
    with st.sidebar:
        st.header("⚙️ 系统配置")
        api_key_input = st.text_input(
            "🔑 Deepseek API密钥",
            type="password",
            value=st.session_state.api_key,
            help="请输入您的DeepSeek API密钥，如果已经保存到了配置文件，刷新页面后会自动加载。",
            placeholder="sk-xxxxxxxxxxxxx"
        )
```

---

# 三、状态存储Session State

## 1.Session State

文档查阅
去streamlit官网 -> 上面Docs
 -> 搜索Session State

## 2.初始化会话状态

```python
def init_session_state():
    #系统状态
    if 'system_init' not in st.session_state:
        st.session_state.system_init = False
    #deepseek_key
    if 'api_key' not in st.session_state:
        st.session_state.api_key = getEnvInfo('DEEPSEEK_API_KEY')
    #自动初始化
    rag = RagSystem(st.session_state.api_key)
    rag.initialize()
    st.session_state.rag_system = rag
    st.session_state.system_init = True
```

干什么：
	初始化会话状态，把 RAG 实例保存到 session，避免每次页面刷新重复加载文档、重建向量索引

为什么这么做：

1. `if 'xxx' not in st.session_state`：判断这个键是否不存在，**只在第一次打开网页的时候执行赋值**；后续页面刷新，键已经存在，不会重复初始化。
- `system_init`：标记系统是否加载完成，布尔状态
- `api_key`：从.env 读取密钥，存入会话状态
2. `rag = RagSystem(...)` 实例化 RAG 对象，执行`initialize()`加载文档、向量、缓存。**这个过程开销很大，不能每次交互反复跑**
3. `st.session_state.rag_system = rag`：把建好的 RAG 实例存入会话，页面刷新后依然可以直接取用，不用重新加载全部知识库
4. `st.session_state.system_init = True`：标记初始化完成，用于侧边栏展示系统状态

## 3.API 密钥写入会话、系统状态渲染

```python
def main():
    init_session_state()
	......
    #侧边栏
    with st.sidebar:
	......
        if api_key_input:
            st.session_state.api_key = api_key_input
        st.header("📊 系统状态")
        if not st.session_state.system_init:
            st.markdown('<p class="status-warning">⚠️ 系统未初始化 </p>',unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-success">✅ 系统已就绪 </p>',unsafe_allow_html=True)
```

干什么：

1. `init_session_state()` 页面启动就调用，负责状态初始化
2. `api_key_input` 是侧边栏文本框输入的密钥，一旦输入内容，就把新密钥覆盖写入 session_state 的 api_key
3. 读取`system_init`状态，在侧边栏渲染文字，展示系统就绪与否

为什么这么做：

1. 网页输入新密钥，直接更新会话里面保存的 api_key，后续问答可以使用新密钥
2. 状态展示给用户直观反馈，一眼就能知道 RAG 系统是否加载成功

---

# 四、系统状态显示效果

## 1.st.columns 多列分栏

想要实现一行两个布局的显示

文档查阅-> 搜索columns

```python
col1, col2, col3 = st.columns(3)
with col1:
    st.header("A cat")
    st.image("[https://static.streamlit.io/examples/cat.jpg](https://static.streamlit.io/examples/cat.jpg)")
with col2:
    st.header("A dog")
    st.image("[https://static.streamlit.io/examples/dog.jpg](https://static.streamlit.io/examples/dog.jpg)")
with col3:
    st.header("An owl")
    st.image("[https://static.streamlit.io/examples/owl.jpg](https://static.streamlit.io/examples/owl.jpg)")
```

## 2.展示文档统计信息

```python
 if not st.session_state.system_init:
	......
            if st.session_state.rag_system:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>📄</h3>
                        <p>{len(st.session_state.rag_system.documents)}</p>
                        <small>文档数量</small>
                    </div>
                """,unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>📝</h3>
                        <p>{len(st.session_state.rag_system.doc_chunks)}</p>
                        <small>文档块</small>
                    </div>
                """,unsafe_allow_html=True)
```

**干什么：**
使用 `st.columns(2)` 创建并排的 2 列布局，左右两个卡片，一行放两个指标。
col1 展示【文档总数】，col2 展示【文档分块总数】；

（1）`<div class="metric-card">`
	`div` 是 HTML 的**块容器标签**，相当于一个空白矩形盒子，用来包裹一组相关内容（图标、数字、文字），把这一整块当成一个独立卡片。
	`class="metric-card"`：给这个 div 起**类名 metric-card**。类名本身不会自带样式，作用是**标记这个盒子，后面写 CSS 样式的时候，统一给所有叫 metric-card 的盒子设置外观（圆角、背景色、阴影、内边距等）**

（2）`<small>`
HTML 原生文本标签，作用：**把包裹的文字渲染成更小字号的文本**。

```
<small>文档数量</small>
```

这里`文档数量`四个字，会自动变成比上面数字更小、更淡一点的辅助说明文字

## 3.检查按钮状态

需要一个能检查按钮状态的函数

```python
def check_cache_exists():
    cache_dir = Path("cache")
    vectors_cache = cache_dir / "doc_vectors.pkl"
    chunks_cache = cache_dir / "doc_chunks.pkl"
    return vectors_cache.exists() and chunks_cache.exists()
```

**干什么：**
	检查 cache 文件夹内**两个核心缓存文件是否同时存在**：向量缓存`doc_vectors.pkl`、文档块缓存`doc_chunks.pkl`。
	只有两个文件都存在，函数才返回 True，代表缓存完整可用；任意一个缺失返回 False，缓存不可用。

**为什么这么做：**

1. RAG 系统有两份缓存：文档块缓存、TF-IDF 向量缓存，二者必须成对存在，只单独有一个会导致系统加载报错；
2. 封装成独立函数，复用性强，代码整洁；后续多处地方需要判断缓存是否存在时，直接调用这个函数，不用重复写路径判断；
3. 提前检测缓存状态，给页面按钮逻辑做判断依据，决定页面显示哪个按钮。

## 4.缓存检测与初始化按钮

```python
        #获取按钮状态
        cache_exists = check_cache_exists()
        if cache_exists and st.session_state.system_init:
            st.button("🔄 重新初始化系统",use_container_width=True)
        else:
            if st.button("🚀 加载缓存数据",use_container_width=True):
                init_session_state()
```

**作用：**
	根据缓存是否存在 + 系统是否已经初始化，**动态切换页面上显示的按钮**
		- 条件成立（缓存存在 && 系统已经初始化完毕）：展示【🔄 重新初始化系统】按钮
		- 条件不成立：展示【🚀 加载缓存数据】按钮，点击触发`init_session_state()`，执行系统初始化
	`use_container_width=True`：让按钮自适应容器宽度，保证界面整洁，不会大小不一

---

# 五、搜索参数配置

```python
def main():
	......
        if st.session_state.system_init:
            st.header('🔍 搜索参数')
            # 最大返回文档数量
            top_k = st.slider(
                '📄 最大返回文档数量',
                min_value=1,
                max_value=20,
                value=10,
                help='设置搜索时最多返回多少个相关文档片段'
            )
            
            #相似度阈值
            similarity_threshold = st.slider(
                '📊 相似度阈值',
                min_value=0.0,
                max_value=1.0,
                value=0.01,
                step=0.01,
                help='只返回相似度高于此值的文档片段，值越高，结果越精确'
            )
            #保存到session_state
            st.session_state.search_top_k = top_k
            st.session_state.similarity_threshold = similarity_threshold
```

## 干什么：

页面在系统初始化完成后，展示两个滑动条组件，用来动态调整 RAG 检索阶段的参数：

1. `top_k`：检索召回片段数量，最多返回 top_k 个相似度最高的文档块
2. `similarity_threshold`：相似度门槛，低于这个分数的片段直接丢弃，不送入大模型
将两个参数存入`st.session_state`，后续问答检索逻辑直接读取会话里保存的参数。

## 为什么这么做：

1. **可视化调参**：不用改代码、重启程序，网页上拖动滑块就能实时修改检索策略，调试 RAG 非常方便。
   - top_k 调大：召回更多片段，信息更全，但更容易混入无关内容、增加 token 消耗
   - 相似度阈值调高：筛选更严格，只保留高度相关片段，减少幻觉；阈值太高容易召回不到内容，返回空结果
2. 存入 session_state：参数一次调整，页面多次交互、刷新都能保留，问答函数直接读取会话变量，不用反复传参。

---

# 六、添加快捷操作按钮

```python
def init_session_state():
	.......
    #快捷问题
    if 'preset_question' not in st.session_state:
        st.session_state.preset_question = ""
    #选择角色
    if 'selected_role' not in st.session_state:
        st.session_state.selected_role = ""
```

```python
def main():
	......
    #主要对话区域
    st.header("💬 与AI智能助手对话")
    #快捷问题
    st.subheader("⚡ 快捷问题")
    col1, col2,col3,col4 = st.columns(4)
    with col1:
        if st.button("🎭 人物关系",use_container_width=True):
            if st.session_state.system_init:
                #设置预选问题到session_state
                st.session_state.preset_question = '红楼梦中主要人物关系是怎样的？'
                st.session_state.selected_role='人物关系'
    with col2:
        if st.button("📚 情节梗概",use_container_width=True):
            if st.session_state.system_init:
                st.session_state.preset_question = '请简述红楼梦第一回的主要情节？'
                st.session_state.selected_role='情节梗概'
    with col3:
        if st.button("🎨 文学手法",use_container_width=True):
            if st.session_state.system_init:
                st.session_state.preset_question = '红楼梦运用了哪些文学表现手法？'
                st.session_state.selected_role='文学手法'
    with col4:
        if st.button("💎 象征意义",use_container_width=True):
            if st.session_state.system_init:
                st.session_state.preset_question = '通灵宝玉有什么象征意义？'
                st.session_state.selected_role='象征意义'
```

## 干什么

1. 在`init_session_state`会话初始化函数里，预先注册两个会话变量：
   - `preset_question`：存放快捷按钮对应的预设问题，默认空字符串
   - `selected_role`：记录当前点击的问题分类标签（人物关系 / 情节梗概等）
2. 使用`st.columns(4)`创建 4 列并排按钮。点击任意快捷按钮，**只有系统初始化完成后**，才会把预设问题和分类存入 session_state。
3. 后面问答输入框读取`preset_question`，自动填充问题文本，实现一键填入查询问题。

## 为什么这么做

1. **提升用户体验**：提供现成示例问题，用户不用手动打字，一键填充问题快速体验 RAG 问答效果，适合项目演示。
2. **状态持久保存**：点击按钮把问题存入 session_state，页面局部刷新不会丢失预设问题。
3. **增加分类标记`selected_role`**：可以后续传给 RAG 提示词，让大模型按照指定角度回答（专门从人物关系角度回答）。
4. 增加判断`if st.session_state.system_init:`：**防护**，系统没加载完成的时候，点击按钮不会写入问题，防止报错。

---

# 七、用户输入区域

```python
def main():
	......
    #显示已选择的角色
    if st.session_state.selected_role:
        st.info(f"✅ 已选择角色：{st.session_state.selected_role}")
    #用户输入区域
    with st.form(key="char_form",clear_on_submit=True):
        col1,col2 = st.columns([5,1])
        with col1:
            user_input = st.text_area(
                '💬 请输入您的问题',
                value=st.session_state.preset_question,
                placeholder="比如：甄士隐是谁？他在故事中起到什么作用？\n\n💡 提示：您可以询问人物、情节、诗词、象征意义等任何关于红楼梦的问题",
                height=100,
                label_visibility='visible',
            )
        with col2:
            st.markdown("<br/>",unsafe_allow_html=True)
            submit_button = st.form_submit_button("🚀 发送",use_container_width=True,type="primary")
            clear_button = st.form_submit_button("🧹 清空",use_container_width=True,type="primary")
```

### 1. 角色提示行

```python
if st.session_state.selected_role:
    st.info(f"✅ 已选择角色：{st.session_state.selected_role}")
```

- `st.session_state.selected_role`：会话变量，点击上方快捷问题按钮写入（人物关系/情节梗概）。
- `if`判断：**只有变量不为空字符串才渲染提示框**，没有点击快捷按钮时，这一行不会显示。
- `st.info()`：Streamlit内置信息提示组件，浅蓝色背景提示条，用来告知用户当前选中的提问角度。

### 2. st.form 表单容器

```python
with st.form(key="char_form",clear_on_submit=True):
```

`st.form`：表单容器，form里所有输入控件**不会实时触发页面刷新**，必须点击表单内的提交按钮，才会一次性读取所有表单内容、执行页面重绘。

参数：

1. `key="char_form"`：表单唯一标识key，区分页面上多个不同表单，必须填写，不能重复。
2. `clear_on_submit=True`：**提交成功之后，自动清空表单内所有输入框内容**。点击发送提交后，文本框文字清空。

### 3. st.columns([5,1])

```python
col1,col2 = st.columns([5,1])
```

- 创建两列布局，`[5,1]`代表**宽度权重**：总宽度分成6份，col1占5份，col2占1份。
- `with col1:`：上下文管理器，with内部写的组件，放在第一列。
- `with col2:`：组件放入第二列。

> 
> 注意：form内部这个布局会失效，是Streamlit底层限制，form内部columns不会横向并排，会上下堆叠。

### 4. st.text_area 多行文本输入框

```python
user_input = st.text_area(
    '💬 请输入您的问题',
    value=st.session_state.preset_question,
    placeholder="比如：甄士隐是谁？他在故事中起到什么作用？\n\n💡 提示：您可以询问人物、情节、诗词、象征意义等任何关于红楼梦的问题",
    height=100,
    label_visibility='visible',
)
```

- `st.text_area`：多行文本输入框，支持换行，适合输入长问题；区别于单行`st.text_input`。
- 第一个参数：输入框的标签文字，展示在输入框上方。
- `value=st.session_state.preset_question`：**输入框默认填充文本**。点击上方快捷按钮，preset_question被赋值，这里自动把预设问题填入输入框。
- `placeholder`：占位提示文字，输入框为空时才会显示，给用户输入示例。`\n`代表换行。
- `height=100`：输入框高度，单位像素。
- `label_visibility='visible'`：标签文字显示出来；可以设置`hidden`隐藏标签。

### 5. 右侧按钮区域

```python
st.markdown("<br/>",unsafe_allow_html=True)
submit_button = st.form_submit_button("🚀 发送",use_container_width=True,type="primary")
clear_button = st.form_submit_button("🧹 清空",use_container_width=True,type="primary")
```

1. `st.markdown("<br/>",unsafe_allow_html=True)`：`<br/>`是HTML换行，用来向下空一行，让按钮和上面输入框顶部对齐。
2. `st.form_submit_button()`：**表单专属提交按钮**，只能写在`with st.form`里面，普通`st.button()`不能在form里用。点击这个按钮，才会触发表单提交。
   - `use_container_width=True`：按钮宽度自动填满所在列宽度
   - `type="primary"`：主按钮样式，高亮红色（和你截图红色按钮效果一致）
3. 两个按钮变量：
   - `submit_button`：发送按钮，点击提交问题，调用RAG问答逻辑
   - `clear_button`：清空按钮，点击触发表单提交，配合`clear_on_submit=True`清空输入框

## 6.总结

1. 展示当前选中的问题角色（人物关系/文学手法），给用户提示；
2. 创建表单容器，内部放置多行问题输入框、发送、清空按钮；
3. 快捷按钮写入的预设问题，自动填充到文本输入框；
4. 点击发送按钮，一次性提交表单，读取用户提问；提交完成自动清空输入框。

## 7.效果

1. **表单隔离刷新**：form内部输入文字不会每敲一个字就刷新页面，减少RAG系统重复加载、减少API不必要调用，优化性能。
2. **预设问题联动**：读取session_state的preset_question，实现快捷按钮一键填充问题，提升演示体验。
3. 统一提交逻辑：发送、清空都属于表单事件，表单提交后统一处理问答业务。

---

# 八、发送问题进行对话并显示结果

## 1、聊天消息渲染函数

```python
def display_chat_message(role, content, sources=None, typing=False):
    """显示聊天消息"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>🙋‍♀️ 您:</strong> {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        typing_indicator = '<span class="typing-indicator">💭</span>' if typing else '🤖'
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>{typing_indicator} 红楼梦助手:</strong> {content}
        </div>
        """, unsafe_allow_html=True)
        if sources:
            with st.expander(f"📖 参考文档片段 ({len(sources)}个)", expanded=False):
                for i, source in enumerate(sources, 1):
                    similarity_color = "#4caf50" if source['similarity'] > 0.5 else "#ff9800" if source[
                                                                                                     'similarity'] > 0.3 else "#f44336"
                    st.markdown(f"""
                    <div class="source-info">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <strong>📄 片段 {i}: {source['source']}</strong>
                            <span style="background: {similarity_color}; color: white; padding: 0.2rem 0.5rem; border-radius: 1rem; font-size: 0.8rem;">
                                相似度: {source['similarity']:.3f}
                            </span>
                        </div>
                        <div style="background: rgba(255,255,255,0.8); padding: 0.5rem; border-radius: 0.5rem; border-left: 3px solid {similarity_color};">
                            <em>📝 内容预览:</em><br>
                            {source['content_preview']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
```

**功能作用**
封装统一的聊天消息渲染函数，区分用户消息和 AI 助手消息，加载预先写好的 CSS 样式展示对话气泡。
当传入`sources`溯源片段列表时，自动生成可折叠展开面板，展示召回文档来源、相似度分数、文本预览；相似度分数用绿 / 黄 / 红三色标签直观区分匹配好坏。
`typing`参数用来开启加载动画，实现 “正在思考” 的动态提示效果。

## 2.问答提交与结果展示

```python
def ask(self,question: str,top_k:int=10,similarity_threshold: float=0.01):
 """这里是为ask函数添加top_k:int=10,similarity_threshold: float=0.01"""
```

```python
def main():
	......
        #处理情况
        if clear_button:
            st.session_state.preset_question = ''
            st.session_state.selected_role = ''
        #处理发送
        if submit_button and user_input.strip():
            #如果系统初始化完成
            if st.session_state.system_init and st.session_state.rag_system:
                #先清空预设问题和选择角色
                st.session_state.preset_question = ''
                st.session_state.selected_role = ''
                #显示对话效果
                display_chat_message("user",user_input)
                #显示思考中的状态
                thinking_placeholder = st.empty()
                with thinking_placeholder:
                    display_chat_message("assistant","正在思考中，请稍后...",typing=True)
                with st.spinner("🔍 正在搜索相关文档... 📚 正在生成回答..."):
                    # 获取搜索参数
                    top_k = getattr(st.session_state,'search_top_k',10)
                    similarity_threshold = getattr(st.session_state,'search_similarity_threshold',0.01)
                    result = st.session_state.rag_system.ask(user_input,top_k=top_k,similarity_threshold=similarity_threshold)
                #清除思考状态
                thinking_placeholder.empty()
                #处理模型返回的数据
                processed_sources = []
                for source in result['source']:
                    if 'content_preview' in source:
                        content = source['content_preview']
                    elif 'content' in source:
                        content = source['content'][:200] + '...' if len(source['content']) > 200 else source['content']
                    else:
                        content = '无内容预览'
                    processed_sources.append({
                        'source':source['source'],
                        'similarity':source['similarity'],
                        'content_preview':content,
                    })
                #显示助手回答
                display_chat_message("assistant",result['answers'],processed_sources)
```

### 1. 清空按钮逻辑

```python
if clear_button:
    st.session_state.preset_question = ''
    st.session_state.selected_role = ''
```

点击【清空】按钮，把 session_state 里面保存的预设问题、选中角色清空。

> 
> 作用：清空标记，下次页面刷新，不会自动保留上一次选中的角色和问题。

### 2. 发送按钮基础判断

```python
if submit_button and user_input.strip():
```

`submit_button`：表单发送按钮是否点击；
`user_input.strip()`：去除文本首尾空格，判断用户输入内容不为空。

> 
> 目的：防止用户空白提交，空字符串不会触发问答。

### 3. 系统可用性校验

```python
if st.session_state.system_init and st.session_state.rag_system:
```

判断系统是否初始化成功，RAG 实例是否存在。

> 
> 保护逻辑：系统没加载完成时，禁止调用 RAG 问答，避免空对象报错。

### 4. 清空历史选中标记

```python
st.session_state.preset_question = ''
st.session_state.selected_role = ''
```

提交问题之后，清空快捷按钮留下的预设问题、角色标记。

> 
> 作用：本轮问答完成，取消 “已选择角色” 蓝色提示条。

### 5. 渲染用户提问消息

```python
display_chat_message("user",user_input)
```

调用封装好的消息函数，把用户的提问渲染成用户对话气泡。

### 6. 展示 “思考中” 临时提示

```python
thinking_placeholder = st.empty()
with thinking_placeholder:
    display_chat_message("assistant","正在思考中，请稍后...",typing=True)
```

`st.empty()`：创建**动态占位容器**，后续可以直接清空这块区域。
先在页面展示 AI 正在思考的提示，带上💭打字动画，提升用户体验。

### 7. st.spinner加载提示

```python
with st.spinner("🔍 正在搜索相关文档... 📚 正在生成回答..."):
```

上下文管理器，代码块运行期间，页面弹出加载转圈提示。

> 
> 用途：检索文档 + 调用大模型 API 存在网络延迟，给用户等待反馈。

### 8. 读取侧边栏滑块参数

```python
top_k = getattr(st.session_state,'search_top_k',10)
similarity_threshold = getattr(st.session_state,'search_similarity_threshold',0.01)
```

`getattr(对象, 属性名, 默认值)`：安全读取 session_state 变量。

- 如果用户拖动滑块，session 里存在`search_top_k`，就读取滑块的值；
- 如果不存在（页面刚加载，还没拖动滑块），自动使用默认值`10`。

> 
> 避免变量不存在导致 KeyError，健壮性写法。

### 9. 调用 RAG 核心 ask 接口

```python
result = st.session_state.rag_system.ask(user_input,top_k=top_k,similarity_threshold=similarity_threshold)
```

传入用户问题、top_k（返回文档片段上限）、similarity_threshold 相似度阈值。
底层 RAG 执行：文档检索→召回 chunk→拼接 prompt→调用 DeepSeek API，返回包含`question`、`answers`、`source`的字典。

### 10. 清除思考提示占位

```python
thinking_placeholder.empty()
```

RAG 接口返回结果之后，清空刚才的 “正在思考” 临时文字。

### 11. 预处理溯源 source 数据

```python
processed_sources = []
for source in result['source']:
    if 'content_preview' in source:
        content = source['content_preview']
    elif 'content' in source:
        content = source['content'][:200] + '...' if len(source['content']) > 200 else source['content']
    else:
        content = '无内容预览'
    processed_sources.append({
        'source':source['source'],
        'similarity':source['similarity'],
        'content_preview':content,
    })
```

循环遍历 RAG 返回的文档片段，做兼容处理：

- 如果已经存在`content_preview`预览文本，直接使用；
- 如果没有预览字段，截取原文前 200 字符，过长文本末尾增加省略号；
- 两个字段都不存在，填充默认文字。
组装成前端渲染需要的字典列表，交给展示函数。

### 12. 渲染 AI 回答和折叠溯源面板

```python
display_chat_message("assistant",result['answers'],processed_sources)
```

调用消息渲染函数，传入 AI 回答文本，以及处理好的文档溯源片段。函数内部自动渲染 AI 气泡，生成可折叠的参考文档面板。
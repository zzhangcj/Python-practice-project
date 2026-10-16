
## 第一部分：文本分割

1. 创建核心入口文件 `rag.system`：用来实现rag项目的核心代码
2. 创建核心类`RagSystem`
3. 核心类的参数是`api_key`(用于调用大模型)，`docs_dir`(提供加载文档的路径)

### 解析
（1）项目流程图解读
> 1、初始化的时候根据提供的文档，先进行预处理，比如分割
> 2、分割之后再进行一个向量化器的处理，转化为向量数据
> 3、用户查找时，结合检索好的数据去搜索
> 4、如果匹配得到，再去生成提示词
> 5、再通过大模型进行一个搜索
> 6、最后返回

（2）`docs_dir:str='docs'`
- `docs_dir`：变量名，用来存放文档文件夹的路径
- `str`：类型注解，代表这个参数必须是字符串类型
- `='docs'`：参数默认值，如果调用RagSystem时不传入这个参数，就自动使用`docs`作为文件夹路径（代表当前项目下名为docs的文件夹）

4. 主入口判断
```python
if __name__ == "__main__":
```
以后可能会是多进程多线程，所以这句话要来判断是不是主进程
`rag = RagSystem(api_key="")`  这里我先写成deepseek
实例化一个对象

5. 系统初始化
```python
def initialize(self):
    print("智能图书检索系统初始化")
```

6. 加载文档
```python
def load_documents(self):
    """加载文档"""
    print("正在加载红楼梦文档...")
```

7. 初始化函数调用`load_documents()`
```python
def initialize(self):
    print("智能图书检索系统初始化")
    self.load_documents()
```

8. 实例化对象初始化
```python
if __name__ == "__main__":
    rag = RagSystem('deepseek_key')
    rag.initialize()
```

9. 新增`main()`
原代码：
```python
if __name__ == "__main__":
    rag = RagSystem(api_key="deepseek_key")
    rag.initialize()
```

转换为：
```python
def main():
    rag = RagSystem(api_key="deepseek_key")
    rag.initialize()
if __name__ == "__main__":
    main()
```

**为什么这么做？**
**代码可以复用**
如果另一个 Python 文件，想启动这个 RAG 系统。只需要写 `from 文件名 import main`，然后调用 `main()` 就能跑。
原来的写法，别的文件导入时，里面的代码不会直接执行，很难复用。

10. Path路径处理
```python
from pathlib import Path
self.docs_dir = Path(docs_dir)
```
这里用Path来获取路径
`Path` 把路径变成对象，支持用 `/` 拼接路径，代码更简洁；
os.path 是传统字符串式的文件路径工具。
RAG 读取文档文件夹，优先推荐 pathlib.Path

11. glob遍历文件
```python
self.docs_dir.glob("*.txt")
```
前提：`self.docs_dir` 是 `Path` 对象（代表 docs 文件夹）
含义：**在 docs_dir 这个文件夹里，查找所有后缀为 `.txt` 的文件**
 `"*.txt"`：通配符，`*` 代表任意文件名
 返回结果：生成器，里面每一项都是Path 对象（不是字符串）

12. for循环遍历文件
```python
for file_path in self.docs_dir.glob("*.txt"):
    print(file_path)
```

**为什么使用for循环？**
glob 返回生成器，生成器只能迭代读取，不能直接索引；
用 for 循环逐个取出文件路径，内存占用更低，适合批量读取文档。

**补充：**
生成器只能迭代一次，元素取出后就销毁；
转为列表后数据保存在内存，可以多次遍历

13. 读取文件内容
```python
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read().strip()
    print(content)
```
作用：在 RAG 项目里，这段代码用来循环读取 txt 文件，提取文档原文，供后续文本分块和向量化使用。

（1）`with open(...) as f:`
`with` 上下文管理器。
作用：打开文件，**代码块结束后自动帮你关闭文件**。
> 如果不用 with，你需要手动写 `f.close()`；忘记关闭会占用系统文件资源。
- `open()`：打开文件
- `file_path`：Path 对象（glob 遍历得到的 txt 文件路径，open 可以直接接收 Path 对象）
- `"r"`：read，只读模式，只读取内容，不能修改写入
- `encoding="utf-8"`：指定编码，防止中文乱码（RAG 读取中文文档必写）
- `as f`：把打开的文件对象，起别名 f

（2）`content = f.read().strip()`
- `f.read()`：一次性读取文件里**全部文本**，返回字符串
- `.strip()`：删掉字符串**开头和结尾**的空白（换行、空格、制表符），中间的空格不动

（3）`print(content)`：打印读取到的文档文本

14. 文档存储变量
```python
# 文档存储
self.documents = []
```

**为什么要放在RagSystem里面？**
`self.documents = []` 写在类里面，作为实例变量，用来**保存读取出来的全部文档信息**。
在 RAG 项目中：读取完所有 txt 文件后，文档数据存放在这个列表，后续直接拿这份数据做文本分块、向量化。

15. 文档存入列表
```python
if content:
    self.documents.append({
        'filename': file_path.name,
        'content': content,
        'path':str(file_path)
    })
```
1. `file_path.name`：Path 对象自带属性，获取**文件名（带后缀）**，只拿最后这一段，例如 `红楼梦.txt`
2. `str(file_path)`：file_path 是 Path 对象，不是字符串；用 str () 转为字符串路径存入字典，防止后续使用时发生类型异常，方便调试。

作用：判断文档内容非空，将文件名、文本内容、文件路径打包成字典存入列表，过滤空白文件，为后续分块和向量化准备文档数据。

16. try-except容错读取
```python
try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        # print(content)
        if content:
            self.documents.append({
                'filename': file_path.name,
                'content': content,
                'path': str(file_path)
            })
except Exception as e:
    print(f"加载文件{file_path}时出错：{e}")
```

（1）try except作用？
读取文档时遇到损坏文件、编码错误等问题不会让整个 RAG 初始化流程中断，只打印当前文件的错误，继续加载剩下的文档。

（2）为什么要用try except结构？
批量加载文档时，`with open`配合 try-except 做容错，个别文件读取失败不中断整体初始化流程。

17. 加载计数
```python
print(f"共加载{len(self.documents)}个文档")
```
对documents这个列表进行计数可得读取的文档数量

18. 预处理函数定义
```python
def preprocess_document(self):
    """预处理文档，分割成块"""
```

19. 初始化调用预处理
```python
def initialize(self):
    print("智能图书检索系统初始化")
    self.load_documents()
    self.preprocess_document()
```

**为什么要在这里 添加 `self.preprocess_document()`**
`initialize()` 是系统初始化入口函数，会按顺序执行：
1. `self.load_documents()`：读取 txt 文件，把原始文档存入`self.documents`
2. `self.preprocess_document()`：拿到已经加载好的原始文档，执行文本分块等预处理操作

必须放在 load_documents 之后：**要先把文档加载出来，才能做预处理；没有文档数据，预处理函数无法运行**

20. 文本分块函数定义
```python
def split_text_chunks(self,text:str,chunk_size:int=300):
```
对于每一个文档里面的内容怎么去处理，这又是一个单独的内容，所以需要定义一个方法split_text_chunks
这个方法是独立的文本切割工具，单独抽成函数，专门做一件事：把一长段文本，切分成多个短文本片段
- `text`：输入，要切的原文
- `chunk_size`：控制切出来每一块的最大字符长度，默认 300 字符

总结：遍历每一篇文档，取出 content 传给这个函数，按照设定长度切割文本，生成文本块，用于后续向量化
单独抽成方法的好处：后续想修改切割逻辑、调整块大小，只需要改这一处代码，不用到处改。

21. 正则分句
```python
def split_text_chunks(self,text:str,chunk_size:int=300):
    """将文本分割成块"""
    sentence = re.split(r'[。！？]',text)
```
- `re`：Python 正则表达式模块，需要先`import re`
- `re.split()`：正则分割函数，根据匹配到的字符，把字符串切分成列表
- `r''`：原始字符串，**原始字符串不会转义反斜杠**，写正则的时候习惯加 r，避免冲突
- `[。！？]`：正则字符集，匹配**任意一个**里面的字符：中文句号`。`、中文感叹号`！`、中文问号`？`
> `[]`含义：匹配括号中任意单个字符，遇到其中任何一个就切割。

22. 清洗空句
```python
def split_text_chunks(self,text:str,chunk_size:int=300):
    """将文本分割成块"""
    sentences = re.split(r'[。！？]',text)
    sentences = [s.strip() for s in sentences if s.strip()]
```
把经过`sentence = re.split(r'[。！？]',text)`处理后的文本，需要清除其中开头和结尾的换行和空格
`sentences = [s.strip() for s in sentences if s.strip()]`为列表推导式
- `for s in sentences`：遍历上一步分割出来的每一段文本
- `s.strip()`：去掉这段文字首尾空格、换行
- `if s.strip()`：**过滤掉空字符串**。如果清理完是空内容，直接丢弃，不保留。
- `[ ... ]`：把处理合格的句子，组装成新列表，重新赋值给 sentences

23. 拼接成块
```python
def split_text_chunks(self,text:str,chunk_size:int=300):
    """将文本分割成块"""
    sentences = re.split(r'[。！？]',text)
    sentences = [s.strip() for s in sentences if s.strip()]
    chunks=[]
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size: #根据句子长度动态调整块的大小
            current_chunk += sentence + "。"
        else:
            if current_chunk: #拼接字符数够了
                chunks.append(current_chunk.strip())
            current_chunk = sentence + "。"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks
```

> 笔记原文这里有笔误：`return chunk` → 正确是 `return chunks`

（1）`chunks=[]`
用来存放最终切割好的文本块，所有达标片段都会放进这个列表。

（2）`current_chunk = ""`
临时变量，用来**累加拼接句子**，攒成一个文本块。

（3）`for sentence in sentences:`
循环遍历前面清洗好的每一个句子。

（4）`if len(current_chunk) + len(sentence) <= chunk_size:`
判断：临时块里已有的文字长度 + 当前这句文字长度，**不超过设定的块上限 chunk_size**。
- ✅满足条件：把当前句子追加到`current_chunk`，末尾补上句号`。`
`current_chunk += sentence + "。"`
> 这里就是补回之前 re.split 丢掉的句号

（5）`else:`
加上这个句子就会超出 chunk_size 上限：
- `if current_chunk:`：如果临时块里面有内容，就把这个攒好的块存入 chunks 列表
- `current_chunk = sentence + "。"`：重置临时块，把当前这句作为新块的起始内容

（6）循环结束后的 `if current_chunk: chunks.append(current_chunk.strip())`
循环跑完之后，最后还剩一组没放进列表的 current_chunk，把它追加进 chunks。

（7）`return chunks`
返回全部文本块列表，交给后续向量化。

**总结：**
把短句逐个合并，尽量凑到接近 chunk_size 的长度，不超过上限；并且补上之前分割丢失的句号，生成完整文本块，供后续向量化。
语义完整性优先级大于int=300的限制

24. 分块存储变量
```python
class RagSystem:
.......
        # 文档存储
        self.documents = []
        self.doc_chunks = []
```
`self.doc_chunks = []` 用来存储分块后的数据，后续要用来向量化处理的

25. 批量分块处理
```python
def preprocess_document(self):
    """预处理文档，分割成块"""
    for doc in self.documents:
        chunks = self.split_text_chunks(doc['content'])
        for i,chunk in enumerate(chunks):
            self.doc_chunks.append({
                'content': chunk,
                'source':doc['filename'],
                'chunk_id':i,
                'full_path':doc['path']
            })
```

（1）`split_text_chunks(text, chunk_size)`
   - 角色：**工具函数**
   - 功能：给一段纯文本字符串，它就能切分成文本块。
   - 什么时候运行：**被别人调用才执行**，单独写在这里不会自动跑。
   - 类比：像一把剪刀，放这不动，要有人拿它才剪东西。

（2）`preprocess_document()`
   - 角色：**批量调度函数**
   - 功能：
   ① 遍历`self.documents`里所有加载完成的文档；
   ② 取出每篇文档的原文，调用上面的 “剪刀”`split_text_chunks`切割；
   ③ 给每一个小块打上标签：来源文件名、块编号、原文件路径；
   ④ 把带标签的块全部存入`self.doc_chunks`，**留给后面向量化、存入向量库**。
   - 类比：拿剪刀，批量把一叠纸全部剪成小纸条，并且给每张小纸条写上来自哪张原稿、第几段。

（3）`chunks = self.split_text_chunks(doc['content'])`
这里因为`def split_text_chunks(self,text:str,chunk_size:int=300)`，接受的参数是str，不是doc这样的字典
所以，这里得传`doc['content']`这样的参数

---

### 知识点补充
#### 为什么要转换成向量？
（1）因为无论文本内容还是符号，这些都是不能直接参与数学运算的
（2）模型的本质是一个数学表达式，既然是数学表达式，就只能接受数学符号或者数值

#### 什么是 sklearn
`scikit-learn`，简称 sklearn，是 Python 机器学习经典库，封装了大量现成机器学习算法、数据预处理工具。
一句话：别人写好的机器学习工具包，不用自己从零手写算法。

#### RAG 项目里，什么时候用 sklearn，为什么用
这个简易 RAG 项目里，常用它做**文本向量化 + 相似度计算**：
1. 可以用`CountVectorizer` / `TfidfVectorizer`：把文本转成向量（TF-IDF 向量）
2. 可以用`cosine_similarity`：计算两个向量之间的余弦相似度，判断两段文字像不像

#### TF-IDF算法的作用
TF-IDF 用来评估词语重要性，把文本转为向量，实现文本相似度检索

#### jieba
jieba 是中文分词库。
TfidfVectorizer默认只按空格切分，对中文完全无效，适合英文句子这样天然用空格分开单词；
中文句子连在一起，电脑分不清词语，jieba 负责把一句话切成词语

#### TfidfVectorizer
sklearn 里的TF-IDF 向量化工具。
作用：接收已经用空格分开词语的文本，自动计算 TF-IDF，输出数字向量

---

## 第二部分：向量化

1. 构建向量库函数定义
```python
def initialize(self):
	......
        self.build_vector_index()
......
def build_vector_index(self):
```
定义一个构建向量库的函数

2. TF-IDF公式与测试代码
```python
def build_vector_index(self):
    """公式计算
    	TF-IDF = 词频(TF) × 逆文档频率(IDF)
    	TF = 某个词在文章中的出现次数 / 文章的总次数
    	IDF = log(语料库的文档总数 / 包含该词的文档数 + 1)
    """
    train = ["Chinese Beijing Chinese",
             "Chinese Chinese shanghai",
             "Chinese Macao",
             "Tokyo Japan, Chinese"]
    tf = TfidfVectorizer() #生成tfidf向量化器
    tf.fit(train) #语料库结果
    print(tf.get_feature_names_out())
```

> 笔记笔误：TF-IDE → TF-IDF

（1）`train = [...]`：**测试用的样例文本列表**，代替我们自己的`doc_chunks`文本块，用来临时测试 TF-IDF 功能，不是最终项目正式代码。正式项目这里应该传入`self.doc_chunks`里面所有 chunk 的文本。

（2）`tf = TfidfVectorizer()`：实例化 sklearn 的 TF-IDF 向量化器。作用：把文本字符串，转为数字向量。

（3）`tf.fit(train)`：**学习语料库**。
fit 会做两件事：
   - 提取全部单词，生成词表
   - 计算每个单词的 TF、IDF 权重，保存到向量化器内部

（4）`tf.get_feature_names_out()`：打印提取出来的全部单词（词表），看向量化器识别到哪些词

当前代码只是演示测试，用英文样例，还没有使用我们自己的红楼梦分块文本，也没有保存向量，属于测试 demo。

3. transform测试
```python
def build_vector_index(self):
........
    test = ["Chinese Chinese Chinese Tokyo Japan"]
    tf_fit = tf.transform(test)
    print(tf_fit.toarray())
```
- fit：之前已经在`train`那 4 条句子上学习了词表、每个词的 IDF 权重（只做一次！）
- transform：用已经学好的 tf 向量化器，对新文本转向量，不会重新学习词表
- `.toarray()`：把稀疏矩阵转为普通二维数组，方便打印查看数字向量
- 模拟用户提问向量化的过程

> 注意：不能再用一次 fit，第二次的fit 会重新建词表，新旧向量维度不一致，无法对比

4. 中文分词器与向量化器配置
```python
def chinese_tokenizer(self):
    #用来处理当前块的分词逻辑，同时作为下面tokenizer所需要的参数（一个函数）
    """中文分词器"""
def build_vector_index(self):
    print("正在构建向量索引....")
    tv = TfidfVectorizer(
        tokenizer=self.chinese_tokenizer,
        max_features=5000, #能够取到的最大特征
        min_df=1, # min_df=n  忽略出现少于n次的词
        max_df=0.95, # 忽略出现大于95%以上的词
        ngram_range=(1, 2) #包含1-2个词的组合
    )
```

（1）**tokenizer=self.chinese_tokenizer**
传入自定义 jieba 分词函数，用来切割中文文本。

（2）**max_features=5000**
限制词表最多保留 5000 个最重要的词（按 TF-IDF 权重排序，取前 5000）。
> 作用：减少向量维度，降低内存占用，加快检索速度。
> 你的项目是红楼梦这类文学长文本，5000 够用；文档越多可以调大。

（3）**min_df=1**
min_df = minimum document frequency
一个词**至少出现在 1 个文档块**才保留。
min_df=1：所有出现过的词都纳入词表；改成 2 就是至少在 2 个 chunk 出现才保留，过滤只出现一次的生僻词。

（4）**max_df=0.95**
max_df = maximum document frequency
如果某个词在**超过 95% 的文档块里都出现**，直接丢弃。
> 例子：“说道”、“然后” 这类几乎每段都有的高频通用词，权重压低，不参与检索。
> 0.95 代表百分比；如果写整数比如`max_df=10`，代表最多出现在 10 个文档。

（5）**ngram_range=(1, 2)**
提取 1 元词组 + 2 元词组
- 1gram：单个词，如`宝玉`、`黛玉`
- 2gram：连续两个词组合，如`贾宝玉`、`林黛玉`
> 作用：捕捉短语，提升检索准确度；代价：词表数量会变多，更耗内存。

（6）作用：实例化带中文分词的 TF-IDF 向量化器，配置词表过滤规则；

5. 向量化器实例与fit_transform
```python
class RagSystem:
    def __init__(self,api_key:str,docs_dir:str='docs'):
.......
        self.vectorizer = None
    def build_vector_index(self):
					.....
        self.vectorizer = TfidfVectorizer(
					.....
        )
        text = [chunk['content'] for chunk in self.doc_chunks]
        self.vectorizer.fit_transform(text)
```

### 1. `self.vectorizer = None`（init）
- 在类初始化的时候，**先预留一个实例属性的位置**，此时还没有创建 TfidfVectorizer 对象，赋值`None`代表暂时为空。
- 目的：让`vectorizer`成为整个 RagSystem 实例的全局成员，**整个类所有方法都能访问到它**。
> 如果不写`self.vectorizer`，只在 build_vector_index 里写局部变量`tv = TfidfVectorizer(...)`
函数执行完 tv 就销毁，后面用户提问做`transform`的时候就找不到这个向量化器了。

### 2. `self.vectorizer = TfidfVectorizer(...)`
实例化 TF-IDF 向量化器，**存入实例变量 self.vectorizer**，保存分词规则、词表、IDF 权重，后续其他方法可以复用这个向量化器。

### 3. `text = [chunk['content'] for chunk in self.doc_chunks]`
列表推导式：遍历`self.doc_chunks`里所有分块字典，取出每一块的`content`文本，组装成文本列表，作为 TF-IDF 的语料。

### 4. `self.vectorizer.fit_transform(text)`
1. `fit`：读取全部 chunk 文本，构建词表、计算每个词 IDF（**只在知识库跑一次**）
2. `transform`：把所有 chunk 文本转为 TF-IDF 向量
3. 合并成`fit_transform`一次性执行

6. 基础中文分词器
```python
def chinese_tokenizer(self,text):
    words = list(jieba.cut(text))
    print(words)
    return words
```

（1）**`jieba.cut(text)`**：jieba 的分词函数，接收中文文本，把句子切成一个个词语，返回**生成器**。
（2）**`list(...)`**：把分词生成器转为普通列表，得到词语列表。
（3）**`return words`**：返回分词后的词语列表，供给`TfidfVectorizer`的`tokenizer`参数使用。

7. 停用词加载
```python
def load_stopwords(self):
    """加载中文停用词库，在chinese_tokenizer里面使用"""
    stopwords_file = Path("中文停用词库.txt")
    stopwords = set()
    if stopwords_file.exists():
        try:
            with open(stopwords_file, "r", encoding="utf-8") as f:
                for line in f:
                    word = line.strip()
                    if word:
                        stopwords.add(word)  # 集合用add
            print(f"已加载{len(stopwords)}个停用词")
        except Exception as e:
            print(f"加载停用词库出错了：{e}")
    else:
        print("没有找到停用词库，将使用默认的停用词库")
        stopwords.update(['的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'])
    return stopwords
```

#### 1、为什么用集合？
**集合查找速度极快，且能够去重**
后续分词后，要循环判断：这个词是不是停用词，要不要删掉。
- `in 集合`：查询几乎瞬间完成，大数据量效率高
- `in 列表`：会逐个遍历比对，词越多越慢
另外集合自动**不允许重复元素**，不会重复存入一样的停用词。
> 列表添加用`append()`；集合添加单个元素用`add()`，批量添加用`update()`

#### 2、`if stopwords_file.exists()`：
先看文件**有没有**，没有直接用内置停用词

#### 3、`try ... except`：
文件虽然存在，但是**读取出问题**时捕获异常，防止程序崩溃

#### 4、为什么load_documents不用if file_path.exists()？
因为使用了`glob("*.txt")`
`self.docs_dir.glob("*.txt")`
		它会扫描文件夹，**只把当前真实存在、后缀是 txt 的文件拿出来**。
		循环拿到的每一个`file_path`，一定是存在的文件。
		→ 不存在的文件不会出现在循环里，没必要再判断 exists

8. 带过滤的中文分词器
```python
def chinese_tokenizer(self,text):
    words = list(jieba.cut(text))
    punctuation = '，。！？；：""（）【】《》、'
    filter_words = []
    for word in words:
        word = word.strip()
        if (word and
            len(word) > 1 and #过滤单字符
            word not in self.stopwords and #停用词过滤
            not all(char in punctuation for char in word)): #标点过滤
            filter_words.append(word)
    return filter_words
```

（1）`words = list(jieba.cut(text))`
		用 jieba 对文本分词，得到词语列表。
（2）`punctuation = '，。！？；：""（）【】《》、'`
		定义需要过滤的中文标点集合。
（3）`filter_words = []`
		新建空列表，用来存放**过滤后合格的词语**
（4）循环遍历每一个分词出来的`word`
		`word = word.strip()`
		去掉词语前后空白、换行空格

（5）if 里面 4 个条件，**全部满足才保留这个词**（and 同时成立）
- `word`：不为空字符串，排除切出来的空内容
- `len(word) > 1`：过滤单字。比如 “我”“的”“，”，只保留 2 个字及以上词汇
- `word not in self.stopwords`：不在停用词集合里面，删掉无意义虚词
- `not all(char in punctuation for char in word)`
  翻译：**不是所有字符都是标点**。
  作用：如果这个词整段全是标点（比如`【】`、`。`），直接过滤掉；词语里面文字 + 少量标点则保留。

（6）符合全部条件 → `filter_words.append(word)`，加入结果列表
（7）最后返回清洗完的词语列表，交给`TfidfVectorizer`做向量化。

---

## 第三部分：缓存机制
> 为什么要缓存化处理？
> 把已经计算好、不会变的结果存下来，避免重复执行耗时操作，提升速度，节省算力

### 实现缓存机制

1. 缓存路径配置
```python
class RagSystem:
    def __init__(self,api_key:str,docs_dir:str='docs'):
	...........
        #缓存文件
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.chunks_cache = self.cache_dir / "doc_chunks.pkl"
        self.vectors_cache = self.cache_dir / "doc_vectors.pkl"
```

（1）把**文本块 (doc_chunks)** 和**向量 (doc_vectors)** 用 pkl 文件存到 cache 文件夹
（2）程序启动时先判断这两个缓存文件是否存在
   - ✅存在：直接加载 pkl，跳过：读文档→分词→文本分块→向量化整套流程，初始化飞快
   - ❌不存在：正常执行预处理、分块、向量化，最后把结果写入这两个 pkl 缓存

`mkdir(exist_ok=True)`
- `mkdir` = 创建文件夹
- `exist_ok=True`：如果 cache 文件夹已经存在，**不会抛出报错**，不用每次手动删文件夹。不加这个参数，第二次运行代码就会报文件夹已存在异常。

`/` ：Path 对象特有的写法，拼接路径，等价于 `os.path.join()`，不用手动写斜杠，跨 Windows/Linux 兼容。

`.pkl`：pickle 序列化文件，可以直接把 Python 列表、字典、numpy 数组这类对象整体保存到硬盘，读取时直接还原成原来的数据，不用自己转格式。
`.pkl` 是 **pickle** 生成的文件后缀，是 Python 专属的文件格式。
> 普通 txt 只能存**文字字符串**；pkl 可以直接保存**Python 里面的对象**：列表、字典、numpy 数组，你代码里的 `self.doc_chunks`（一堆字典组成的列表）、TF-IDF 向量矩阵，都能一次性打包存进去。

2. 文档块缓存
```python
def preprocess_document(self):
    #先检查缓存
    if self.chunks_cache.exists():
        print("发现文档块缓存，正在加载....")
        with open(self.chunks_cache, "rb") as f:
            self.doc_chunks = pickle.load(f)
        print(f"从缓存加载了{len(self.doc_chunks)}个文档块")
        return
    """分块的预处理文档"""
	.........
    # 保存缓存
    with open(self.chunks_cache, "wb") as f:
        pickle.dump(self.doc_chunks, f)
```

> 笔记笔误：文档快缓存 → 文档块缓存

（1）核心逻辑
1. ✅缓存存在：直接用 pickle 读取缓存赋值给`self.doc_chunks`，`return`直接结束函数，**跳过文档分块流程**
2. ❌缓存不存在：往下执行文档分块处理，分块做完后，把结果保存到 pkl 缓存，下次启动就可以读缓存

（2）rb，wb
- `r` = read 读取
- `w` = write 写入，会覆盖文件原有内容
- `b` = binary 二进制模式
👉 **rb = read binary：二进制读取**
👉 **wb = write binary：二进制写入**

（3）pickle.dump，pickle.load(f)
`load()`：pickle 的**加载函数**
**load = 拆包**，把硬盘上 pkl 里面的数据，还原成内存里的变量
`dump()`：pickle**保存函数**
**dump = 打包**，把内存里的变量打包，存入硬盘的 pkl 文件

总结：1-2是实现文档块的缓存，下面是实现向量化数据的缓存

3. 文档向量变量
```python
class RagSystem:
    def __init__(self,api_key:str,docs_dir:str='docs'):
	.......
        self.doc_vectors = None
	......
    def build_vector_index(self):
	......
        self.doc_vectors = self.vectorizer.fit_transform(text)
```
`self.doc_vectors = None`
预先预留变量，**用来存放全部文档块算出的 TF-IDF 向量矩阵**,刚开始为空，设为None
`self.doc_vectors`：
存**算出来的向量矩阵**（结果数据），就是这句赋值放进去的

4. 向量缓存读写
```python
def build_vector_index(self):
    #检查缓存
    if self.vectors_cache.exists():
        print("发现向量缓存，正在加载...")
        with open(self.vectors_cache, "rb") as f:
            cache_data = pickle.load(f)
            self.vectorizer = TfidfVectorizer(
                tokenizer=self.chinese_tokenizer,
                vocabulary=cache_data['vocabulary'],
            )
            self.vectorizer.idf_ = cache_data['idf']
            self.doc_vectors = cache_data['vectors']
        print("向量索引加载完成")
        return
	.......
	.......
    # 保存缓存
    cache_data = {
        'vectors': self.doc_vectors,
        'vocabulary': self.vectorizer.vocabulary_,
        'idf': self.vectorizer.idf_,
    }
    with open(self.vectors_cache, "wb") as f:
        pickle.dump(cache_data, f)
    print("向量索引构建完成")
```

(1) 核心逻辑
✅有缓存：读取 pkl，手动恢复 TF-IDF 向量化器的词表、idf 值和文档向量，`return`直接结束函数，跳过重新训练 TF-IDF。
❌无缓存：正常新建 TfidfVectorizer，fit_transform 训练生成向量；训练完成后，把**向量、词表、idf**打包存入 pkl 缓存，下次启动直接读。
> 重点：这里**没有直接 pickle 保存整个 self.vectorizer 对象**，而是拆成 3 份数据存字典：vectors、vocabulary、idf，加载的时候再重新构造 TfidfVectorizer。

（2）缓存数据结构
```python
cache_data = {
    'vectors': self.doc_vectors,
    'vocabulary': self.vectorizer.vocabulary_,
    'idf': self.vectorizer.idf_,
}
```
构造字典，打包三样必须保存的数据：
1. `vectors`：所有文档块的 TF-IDF 向量矩阵（self.doc_vectors）
2. `vocabulary_`：向量化器学到的词表，记录每个词语对应的编号
3. `idf_`：每个词对应的逆文档频率，TF-IDF 计算权重核心数据

> 为什么存这 3 个？
> TfidfVectorizer 训练完成后，**词表 + idf 数组** 就代表了整套训练信息，有这两个，就能复原向量化器。

（3）写入缓存
```python
with open(self.vectors_cache, "wb") as f:
    pickle.dump(cache_data, f)
```
`wb`二进制写入，pickle 把这个字典打包，保存成 pkl 缓存文件

（4）读取缓存判断
```python
if self.vectors_cache.exists():
    print("发现向量缓存，正在加载...")
    with open(self.vectors_cache, "rb") as f:
        cache_data = pickle.load(f)
```
1. 判断缓存文件是否存在
2. `rb`二进制读取 pkl，`pickle.load`把字典`cache_data`读进内存

（5）难点：手动复现向量化器
```python
with open(self.vectors_cache, "rb") as f:
    cache_data = pickle.load(f)
    self.vectorizer = TfidfVectorizer(
        tokenizer=self.chinese_tokenizer,
        vocabulary=cache_data['vocabulary'],
    )
    self.vectorizer.idf_ = cache_data['idf']
    self.doc_vectors = cache_data['vectors']
```

> 为什么要这么写（当前向量缓存策略**不保存完整 vectorizer 对象，仅保存它生成的三份结果数据**）？
> 而前面的文档块的缓存，只是单纯的dump和load就行？
> 1、文档块`doc_chunks`是普通列表字典，数据结构稳定，直接 pickle 读写。
> 2、而`TfidfVectorizer`属于 sklearn 的对象，直接 pickle 保存完整对象，切换 sklearn 版本极易加载失败。
> 3、所以项目选择**不保存完整 vectorizer，仅保存它训练产出的 vocabulary、idf、vectors 三份核心数据**。

既然选择保存其中部分结果，则后续读取缓存的时候，需要一定的规则将这部分结果转化为完整可用的数据

> 那为什么新的`self.vectorizer = TfidfVectorizer`，括号里面要写 tokenizer 和 vocabulary，而 idf 和 vectors 要写在外面？
> （1）构造函数入参：创建类实例`TfidfVectorizer(...)`时，括号内可以写、官方预先定义好的配置项。
> （2）sklearn 命名约定
> 	- 不带下划线：构造配置参数，创建对象时传入
> 	- 末尾带下划线`xxx_`：fit 训练完成后，才生成的实例属性
> 		`vocabulary_`是训练后生成的属性，但是 TfidfVectorizer**单独提供了一个参数名叫 vocabulary**，用来手动指定词表。
> 1. `tokenizer`、`vocabulary`是**构造函数支持的入参**，创建向量化器实例的时候，就可以在括号内传入。
> 	- tokenizer：规定分词方式，必须和第一次训练保持一致。
> 	- vocabulary：直接复用缓存里的旧词表，不让向量化器重新生成词表。
> 2. `idf_`**没有对应的构造入参**，它是 fit 训练后才计算出来的结果属性，不能写在括号。只能等向量化器对象创建完成，再手动赋值。
> 3. `vectors`不属于向量化器本身的数据，是文档预先算好的向量结果，独立赋值，用来后续相似度检索。（最初的self.vectorizer = TfidfVectorizer里面没有这个，是放在外面的东西）

---

## 第四部分：与用户交互的界面（问答检索）

### 1. 交互式问答主循环
```python
def main():
	.......
    # 交互式问答
    print("=== 智能图书问答系统 ===")
    print("输入你的问题,输入 ‘quit' 或者 ’exit‘ 退出")
    while True:
        question = input("请输入你的问题：").strip()
        if question.lower() in ['quit','exit','退出']:
            print("感谢使用系统！")
            break
        if not question:
            continue
```

### 2. 检索函数定义与校验
```python
def search_chunks(self,query: str):
    if self.vectorizer is None or self.doc_vectors is None:
        raise ValueError("向量索引未构建，请先调用 build_vector_index()")
    # 向量化查询
    query_vector = self.vectorizer.transform([query])
```

(1)功能
这是 RAG 的**检索函数**，接收用户的提问字符串`query`，作用：把用户问题转向量，再去和文档块向量比对，找出最相关的文档片段

(2)详解
- 校验：向量化器、文档向量是否已经生成
- 只要任意一个是`None`，直接抛出异常，终止程序
- 目的：**防止用户还没构建向量索引，就直接调用检索**，避免后续代码报错。
> `raise ValueError`：主动抛出参数错误，提示调用者要先执行`build_vector_index()`构建向量库。

(3)查询语句向量化
`query_vector = self.vectorizer.transform([query])`
重点！检索用户问题时只能用`transform`，不能`fit_transform`
- `[query]`：`transform`接收**字符串列表**，所以把单个问句包进列表
		fit 会重新学习词表，破坏原来向量空间，文档向量和问题向量不在一套标准里，相似度完全失效。
		`transform()`：**使用已经训练好的词表 + IDF 权重，只做转换，不重新训练**

### 3. 相似度计算与排序
```python
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
def search_chunks(self,query: str,top_k:int=10,similarity_threshold: float=0.01):
	......
    # 计算（余弦）相似度 ,取值范围[0:1]
    similarities = cosine_similarity(query_vector, self.doc_vectors).flatten()
    print(similarities,'similarities')
    # arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    # print(np.where(arr > 5)) #(array([6, 7, 8, 9]),) 注意返回的是一个元组，里面是索引
    valid_index = np.where(similarities > similarity_threshold)[0]
    #按照相似度从大到小排列
    sorted_index = valid_index[np.argsort(similarities[valid_index])][::-1]
    print(sorted_index,'sorted_index')
    top10_index = sorted_index[:top_k]
```

#### （1）模块导入
```python
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
```
1. `from sklearn.metrics.pairwise import cosine_similarity`
  	 - 作用：**导入余弦相似度计算工具**。
   	- 为什么需要：TF-IDF 把文本变成向量，文字本身不能比较相似程度，只能**用向量计算夹角**，余弦相似度就是用来衡量两个向量有多接近。sklearn 已经写好这个算法，不用自己手写数学公式。
2. `import numpy as np`
   	- 作用：numpy 是 Python 的数值数组库。我们的相似度结果、向量都是数组格式，要做筛选、排序、取下标操作，原生 Python 列表做这件事很慢、代码麻烦，numpy 专门处理数字数组。

#### （2）参数
- `query`：用户输入的问题文本，例如：`甄士隐是谁`
- `top_k:int=10`
✅ **是什么**：最多返回多少条匹配的文档片段，这里默认取 10 条
✅ **为什么要设置 top_k**
 1. 向量检索会返回几百上千个结果，但 LLM 大模型有**上下文窗口上限**，不能一次性把 300 个 chunk 全部塞给模型，会超长、消耗大量 token、变慢、费用变高。
 2. 大部分低相关的文段不需要给模型，我们只取**相似度最高的前 N 个**。
 3. 示例：top_k=5 → 只拿最匹配的 5 段文本交给大模型。

- `similarity_threshold: float=0.01`
✅ **是什么：相似度最低门槛（阈值）**
✅ **作用**：过滤掉完全不相关的文档块。
大于这个数值，代表 “有一点点相关”；小于这个数值，判定为无关，直接丢弃。

#### （3）余弦相似度计算
```python
similarities = cosine_similarity(query_vector, self.doc_vectors).flatten()
```

**为什么余弦相似度取值范围是【0 ~ 1】**

两个向量在空间里有一个夹角，余弦值就是相似度：
1. **等于 1**：两个向量方向完全一模一样，文本几乎完全相同，高度相关
2. **0 < 数值 <1**：向量有部分重合，文本有一定相关。数字越大越相似
3. **等于 0**：向量互相垂直，完全没有重合词汇，两段文本毫无关系

> 注意：余弦相似度**不会出现负数**，TF-IDF 生成的向量所有元素都是≥0，所以结果锁定在`[0,1]`。
> 如果是 embedding 向量（例如 openai 向量）会出现负数，但是 TF-IDF 不会！

**`.flatten()` 在干什么？**

1. `cosine_similarity` 返回的是**二维数组**，输出形态：`[[0.43, 0, 0, 0.21 ...]]`
2. `.flatten()` 的作用：把二维数组压扁，转换成**一维数组**，结果形态：`[0.43, 0, 0, 0.21 ...]`
3. 为什么要转一维：一维数组方便后续 numpy 做筛选、下标取值操作。
4. 一维数组取值含义：数组中每一个数字，对应一个文档块的相似度
    - `similarities[0]`：第 0 号文档块 和用户问题的相似度
    - `similarities[1]`：第 1 号文档块 和用户问题的相似度

---

#### (4) 过滤：只保留相似度超过阈值的 chunk 下标
```python
valid_index = np.where(similarities > similarity_threshold)[0]
```
1. `np.where(条件)`：根据条件，找出满足条件的**元素下标**。
2. 返回值类型：`np.where` 返回的是**元组**，示例：`(array([0,2]), )`
3. `[0]`：取出元组里面第一个元素，也就是保存下标的numpy数组。
> 注释示例：`# print(np.where(arr > 5)) #(array([6, 7, 8, 9]),)`

> 举例：
> - `similarities = [0.02, 0, 0.43]`，阈值`0.01`
> - 满足条件的下标：0、2
> - `np.where`得到元组 `(array([0, 2]), )`
> - 加`[0]`之后：`valid_index = array([0, 2])`

---

#### (5) 对筛选后的结果，按相似度从大到小排序
```python
sorted_index = valid_index[np.argsort(similarities[valid_index])][::-1]
```

拆解分步说明：
1. **`similarities[valid_index]`**
    根据`valid_index`里面保存的下标，取出对应相似度分数。
    > 示例：`valid_index=[0,2]` → 取出分数：`[0.02, 0.43]`

2. **`np.argsort(分数数组)`**
    `np.argsort()`：对数组**从小到大排序，返回排序之后元素的位置下标，不返回真实数值**。
    > 示例：分数`[0.02, 0.43]`
    > 从小到大顺序：0.02(位置0)，0.43(位置1)
    > 返回结果：`array([0, 1])`

3. **`[::-1]` 数组反转**
    argsort只能输出从小到大；`[::-1]` 将数组反转，实现**从大到小**。
    > 上一步结果`[0,1]`反转后得到：`[1, 0]`

4. **`valid_index[...]` 映射回原始文档块编号**
    上面得到的`[1,0]`只是**筛选之后的数组内部位置**，不是原始文档块下标。
    用这个位置去索引`valid_index`，换回真正的文档块编号。
    > 示例：`valid_index[[1, 0]]`
    > - `valid_index[1] = 2`
    > - `valid_index[0] = 0`
    > - 输出：`array([2, 0])`

✅最终 `sorted_index`：numpy数组，里面存放**原始文档块编号，已经按照相似度从高到低排好序**


#### (6)循环组装返回结果
```python
def search_chunks(self,query: str,top_k:int=10,similarity_threshold: float=0.01):
	.......

        results = []
        for idx in top10_index:
            chunk = self.doc_chunks[idx].copy()
            chunk['similarity'] = float(similarities[idx])
            results.append(chunk)
        return results

    def ask(self,question: str):
        # 搜索相关文档
        relevant_chunks = self.search_chunks(question)
        print(relevant_chunks)
        if not relevant_chunks:
            return {
                'question': question,
                'answers': '抱歉，在文档中没有找到与您问题相关的内容',
                'source': []
            }
        print(f"找到{len(relevant_chunks)}个相关的文档片段")
```

1. `for idx in top10_index`：遍历筛选排序好的文档块下标

2. `chunk = self.doc_chunks[idx].copy()`
> 为什么要 copy：如果直接修改原字典，会改动内存里原始`self.doc_chunks`，产生副作用。复制之后只修改副本，原始数据不受影响。
   - `self.doc_chunks[idx]`：取出对应下标的文档字典，包含`content`、`source`、`chunk_id`等信息
   - `.copy()`：**复制一份字典**，不是直接引用原数据。

3. `chunk['similarity'] = float(similarities[idx])`
   - 在这个副本字典里面，**新增一对键值对**：`similarity`，存入当前文档块和用户问题的相似度分数
   - `float()`：把 numpy 的数值转为普通 python 浮点数，避免后续序列化 / 打印出现 numpy 类型报错

4. `results.append(chunk)`：把带相似度的文档块，放进结果列表

5. `return results`：返回列表，列表里每一项都是字典：包含文本内容、来源文件名、chunk 编号、相似度分数


### 4.问答入口(ask函数)
```python
def ask(self,question: str):
    # 搜索相关文档
    relevant_chunks = self.search_chunks(question)
    print(relevant_chunks)
    if not relevant_chunks:
        return {
            'question': question,
            'answers': '抱歉，在文档中没有找到与您问题相关的内容',
            'source': []
        }
    print(f"找到{len(relevant_chunks)}个相关的文档片段")

    #调用大模型(deepseek)生成答案
    print("正在生成答案...")
    print(self.generate_answers(question,relevant_chunks))
```
1. `relevant_chunks = self.search_chunks(question)`

    调用上面写好的检索函数，传入用户问题，拿到检索出来的相关文档片段列表。

2. `if not relevant_chunks:` 判断是否检索到内容

   - `if not relevant_chunks`：如果返回的列表是空（没有任何文档块满足相似度阈值）
   - 直接返回一个字典，告知用户找不到相关资料，同时带上原始问题、空来源列表。

3. 如果找到了片段

    `print(f"找到{len(relevant_chunks)}个相关的文档片段")`，打印找到了多少条相关块。

4. 调用答案生成函数，生成答案

### 5.deepseek的模型调用
#### （1）从DeepSeek提示词库学到的要点
1. **提示词基础结构**：标准提示词由「角色设定+任务目标+约束规则+输出样例」4部分组成，不要只写简单一句话。
2. **RAG重点模板**
    - 角色扮演模板：用来定义知识库助手，**强制约束禁止编造内容，缓解大模型幻觉**，是RAG核心。
    - 结构化输出模板：要求模型返回JSON格式，方便Python代码直接解析结果，可搭配API的`response_format`参数。
3. **使用原则**
    - 模板是骨架，不能直接照搬，要结合你的项目修改。
    - 角色规则写在`system`消息；检索出来的文档上下文、用户问题，放在`user`消息动态传入。
4. **避坑要点**
    - 增加异常捕获，防止模型输出不规范JSON造成程序崩溃。
    - 参考文档片段不要写入system提示词，每轮对话动态传入。
5. **附加价值**
    - 代码类模板：可用于代码解释、纠错、重构，辅助你调试RAG项目代码。
    - 提示词生成模板：可以让AI帮你快速迭代、优化提示词。

> 一句话总结：提示词库教会你**规范地写指令**，让大模型严格按照RAG的规则、指定格式回答，减少瞎编乱造。

#### （2）DeepSeek两种调用方式与兼容原理
为什么官方文档推荐的是openai调用，和我学到LangChain的知识有些冲突？

1. **官方推荐OpenAI SDK调用**
DeepSeek接口兼容OpenAI v1接口规范，仅需修改`api_key`和`base_url`即可调用。优点：依赖轻量，只需要安装`openai`包，无额外中间层，排错简单，适合手写RAG学习底层原理。
2. **LangChain的ChatDeepSeek调用**
LangChain对DeepSeek做了二次封装，底层依旧走OpenAI兼容接口。优点：自带各类RAG工具组件；缺点：依赖包多、容易版本冲突，多一层封装，调试更复杂。

3. 核心理解：DeepSeek并不是OpenAI，只是对齐了接口标准，OpenAI SDK只是请求工具，通过`base_url`将请求转发至DeepSeek服务端。
4. **项目选型建议**：当前手写RAG练底层，优先选用官方OpenAI SDK写法。

#### (3) .env配置DeepSeek客户端代码笔记
```python
from openai import OpenAI
import os
from dotenv import load_dotenv

# 只在程序启动执行一次，加载.env环境变量
load_dotenv(verbose=True)

# 读取环境变量
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

# 校验
if not DEEPSEEK_API_KEY:
    raise ValueError("未读取DEEPSEEK_API_KEY，请检查根目录.env文件！")

class RagSystem:
    def __init__(self,docs_dir:str='docs'):
        self.docs_dir = Path(docs_dir)
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        )
```
1. **依赖安装**：需要安装 `openai`、`python-dotenv`
```bash
pip install openai python-dotenv
```
2. **`.env`文件**
    - 存放位置：项目**根目录**，和代码文件同级
    - 文件内容：
```env
DEEPSEEK_API_KEY=sk-你的DeepSeek密钥
DEEPSEEK_BASE_URL=[https://api.deepseek.com](https://api.deepseek.com)
```
    - 注意：文件名是`.env`，不要自动加上`.txt`后缀；不要给值加引号。
3. **代码逻辑**
    - `load_dotenv(verbose=True)`：加载`.env`中的环境变量，`verbose=True`会打印日志，方便调试；稳定后可去掉。
    - `os.getenv()`：读取环境变量，读取不到返回`None`，不会直接崩溃。
    - DeepSeek接口兼容OpenAI SDK，通过`base_url`把请求转发到DeepSeek服务。
    - 在RagSystem初始化时创建`self.client`，作为实例属性，后续`ask()`函数直接复用客户端调用API。
4. **安全重点**
    - `.env`记录密钥，**绝对不要硬编码API密钥写在python代码里**。
    - 在`.gitignore`添加` .env`，提交Github时忽略该文件，防止密钥泄露。
5. **校验**

读取环境变量后增加判断，没配置密钥直接抛出提示，避免API调用报错：
```python
if not DEEPSEEK_API_KEY:
    raise ValueError("未读取DEEPSEEK_API_KEY，请检查根目录.env文件！")
```
6. **原理小结**

把密钥放到独立配置文件，代码从环境变量读取密钥，兼顾开发便捷性与密钥安全；

> 一句话总结：用`python-dotenv`读取`.env`里面的DeepSeek密钥，在RAG类初始化创建API客户端，密钥不和代码放一起，保护密钥安全。

### 6. 答案生成函数 generate_answers
```python
def generate_answers(self,query: str,context_chunks):
    context = "\n\n".join([f"文档片段{i+1}:{chunk['content']}" for i,chunk in enumerate(context_chunks)])
    system_prompt = """ 这里是提示词，我就省略了，你可以去源码看看 """.strip()

    user_prompt = f"""
基于以下的文档内容回答：
{context}
问题：{query} """.strip()
    try:
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1000,
            stream=False,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        error_type = (type(e)).__name__
        error_details = str(e) if str(e) else "未知错误"
        print(f"生成答案时出错：{error_type}-{error_details}")
        return f"生成答案时出错：{error_type}-{error_details}"
```

#### （1）函数参数
- `query`：用户原始提问（例如：甄士隐是谁）
- `context_chunks`：`search_chunks`检索返回的相关文档块列表，列表内每个元素是字典，包含`content`、`source`、`similarity`等字段。

#### （2）拼接检索上下文
```python
context = "\n\n".join([f"文档片段{i+1}:{chunk['content']}" for i,chunk in enumerate(context_chunks)])
```
1. 遍历检索出来的文档块，取出`chunk['content']`也就是原文片段。
2. 给每一段片段编号`文档片段1、文档片段2`，方便大模型区分不同来源文本。
3. `"\n\n"`使用两个换行分割片段，让文本分段清晰，大模型更容易阅读。
4. 最终拼接成**一段完整的上下文字符串**，作为知识库材料交给大模型。

> RAG核心思想：**把检索到的知识库文本和用户问题一起打包发给大模型**，大模型只能依靠这份上下文回答。

#### （3）提示词拆解 system_prompt（系统提示词）
`system`消息：**定义大模型的身份、能力、强制规则、工作流程**，在对话最开始生效，全局约束模型行为。
模板分为固定6大块：
1. **Role**：角色设定，这里设定为红楼梦研究专家
2. **Profile**：角色简介、背景、性格、面向人群
3. **Skills**：角色具备的能力清单，告诉模型它能做什么
4. **Rules（最重要，抑制幻觉）**
    - 强制**基于提供的文档文本回答**，不能编造原著不存在的内容
    - 约束回答风格、引用原文、不能随意主观臆断
    - 划定边界，禁止超出文档内容过度解读，减少大模型幻觉（RAG最关键）
5. **Workflows**：规定模型回答的执行步骤，让模型按固定流程思考
6. **Initialization**：启动指令，要求模型严格遵守全部规则

> 要点：system提示词是固定不变的，**不会随用户问题变化**。

#### （4）user_prompt 用户提示词
```python
user_prompt = f"""
基于以下的文档内容回答：
{context}
问题：{query} """.strip()
```
1. user消息：每一轮问答**动态变化**。
2. 里面包含两部分：检索拼接好的`context`知识库片段 + 用户本次的`query`问题。
3. 作用：告诉模型：参考下面提供的文档，回答用户的问题。

> 区分记忆：
> - system：固定角色+规则，写死；
> - user：动态内容，每次检索得到的文档+用户新问题，每次都不一样。

#### （5）调用DeepSeek API 核心参数
```python
response = self.client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    max_tokens=1000,
    stream=False,
    temperature=0.7
)
```
1. `model="deepseek-chat"`：指定使用DeepSeek对话模型
2. `messages`消息列表：遵循OpenAI消息格式，由多条role消息组成，`system`在前，`user`在后。
3. `max_tokens=1000`：限制模型输出的最大文字长度，防止输出过长、消耗过多token。
4. `stream=False`：关闭流式输出。一次性返回完整答案，不是逐字打字输出，适合当前控制台项目。
5. `temperature=0.7`：控制创造性。
    - 数值范围：0~2
    - 越靠近0：回答严谨、确定性高、重复度高，不容易瞎编；
    - 越大：回答发散、创意强，更容易产生幻觉。
    - 0.7属于平衡值，文学类问答比较合适。

#### （6）读取返回结果
```python
return response.choices[0].message.content
```
- API返回是一个复杂对象，`choices`是模型返回的候选答案列表，一般取第0个。
- `.message.content`：提取模型生成的文字答案，返回给上层`ask()`函数。

#### （7）异常捕获 try ... except
```python
try:
    # API调用代码
except Exception as e:
    error_type = (type(e)).__name__
    error_details = str(e) if str(e) else "未知错误"
    print(f"生成答案时出错：{error_type}-{error_details}")
    return f"生成答案时出错：{error_type}-{error_details}"
```
1. 作用：防止API调用失败（网络超时、密钥错误、额度耗尽等）直接让整个程序崩溃。
2. 捕获所有异常，打印错误类型和详情，返回错误提示字符串给用户，程序继续运行。

#### （9）重点总结
1. RAG幻觉抑制核心：**在system提示词强制约束，回答必须依赖提供的文档片段，禁止编造信息**。
2. 提示词分离：固定角色规则放`system`，动态检索材料和用户提问放`user`。
3. API调用必须增加异常捕获，避免网络、接口异常直接退出程序。
4. temperature控制模型发散程度，知识库问答一般推荐0~0.7区间。
5. `max_tokens`限制输出长度，控制token消耗，防止超长回答。


### 7.整理信息，完善main函数
```python
def ask(self,question: str):
    relevant_chunks = self.search_chunks(question)
    .......
         #调用大模型(deepseek)生成答案
        print("正在生成答案...")
        answers = self.generate_answers(question,relevant_chunks)
        print(answers)

        #整理来源信息
        source = []
        for chunk in relevant_chunks:
            source.append({
                "source": chunk['source"],
                "similarity": chunk['similarity'],
                "content_preview": chunk['content'][:100] + '...' if len(chunk['content']) > 100 else chunk['content'],
            })
        return {
            "question": question,
            "answers": answers,
            "source": source
        }

def main():
    rag = RagSystem()
    rag.initialize()

    ......
         # 获取答案
        result = rag.ask(question)

        # 显示结果
        print(f"\n答案： {result['answers']}")

        if result['source']:
            print("\n相关的文档片段：")
            for i,source in enumerate(result['source'],1):
                print(f"{i}. 来源：{source['source']}(相似度：{source['similarity']:.3f})")
                print(f"内容预览：{source['content_preview']}")
```

#### （1）这里在做什么
当前项目底层模块（文档加载、分词、分块、向量缓存、检索函数、大模型调用函数）已经全部开发完毕。
为了**统一封装RAG完整链路，对外提供简洁调用接口**，新增ask函数的整理来源信息的部分；
再编写main函数，作为控制台交互层，用来测试这个接口。

#### （2）ask函数内代码解析
```python
#调用大模型(deepseek)生成答案
print("正在生成答案...")
answers = self.generate_answers(question,relevant_chunks)
print(answers)
```
为什么要单独提出answers：

调用`generate_answers`拿到大模型生成的回答文本，存入变量`answers`进行临时保存；
后续组装返回字典时，可以直接使用`"answers": answers`把回答文本放入返回结构中，方便统一打包返回给调用方。

```python
#整理来源信息
source = []
for chunk in relevant_chunks:
    source.append({
        "source": chunk['source'],
        "similarity": chunk['similarity'],
        "content_preview": chunk['content'][:100] + '...' if len(chunk['content']) > 100 else chunk['content'],
    })
return {
    "question": question,
    "answers": answers,
    "source": source
}
```
这里在做什么：
- 遍历检索返回的文档块列表，循环提取每一个片段的来源文件名、相似度分数、文本预览，组装成溯源字典并放入source列表；
- 最后将用户提问、大模型回答、溯源来源列表打包成一个完整字典向外返回。

为什么这么做：
- 收集`source`溯源信息：记录召回片段的文件名、相似度、文本预览。用于RAG调试，方便查看答案对应的原文来源，校验答案可靠性。
- 打包字典返回：结构化输出，上层main函数只需要读取字典key就能拿到全部信息，后续扩展web接口也可以直接复用这个返回格式。

```python
"content_preview": chunk['content'][:100] + '...' if len(chunk['content']) > 100 else chunk['content'],
```
这里在做什么：
- 对文档片段文本做截断处理，生成简短预览文本

为什么这么做：
1. `chunk['content'][:100]`：字符串切片，截取原文**前100个字符**。
2. `if len(chunk['content']) > 100` 判断原文长度是否超过100字符：
    - 如果大于100：截取前100字符，拼接上省略号`...`，代表文本还有更多内容没有展示
    - 如果小于等于100：文本较短，直接完整展示原文，不需要加省略号
3. 目的：
- 只展示片段摘要，避免在控制台打印过长文本，让输出结果简洁易读；
- 同时保留一小段原文，快速预览该片段内容，方便调试查看召回文本


#### （3）main函数内代码解析
```python
# 显示结果
print(f"\n答案： {result['answers']}")

if result['source']:
    print("\n相关的文档片段：")
    for i,source in enumerate(result['source'],1):
        print(f"{i}. 来源：{source['source']}(相似度：{source['similarity']:.3f})")
        print(f"内容预览：{source['content_preview']}")
```
这里在做什么：
- 读取接口返回的字典，打印大模型回答；如果存在检索来源片段，则循环打印每一条召回片段的溯源信息。

为什么这么做：
- 将RAG结果可视化展示在控制台，给用户展示回答。
- 同时打印召回的文档块信息，方便开发调试，直观观察检索召回效果，排查检索好坏。

#### （4）核心总结
把检索结果送入大模型、组装溯源信息、打包结构化返回，**封装完整RAG链路作为统一接口**。

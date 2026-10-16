import re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
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
        # 文档存储
        self.documents = []
        self.doc_chunks = []
        self.vectorizer = None
        self.doc_vectors = None

        #加载停用词库
        self.stopwords = self.load_stopwords()

        #缓存文件
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.chunks_cache = self.cache_dir / "doc_chunks.pkl"
        self.vectors_cache = self.cache_dir / "doc_vectors.pkl"

    def initialize(self):
        print("智能图书检索系统初始化")
        self.load_documents()
        self.preprocess_document()
        self.build_vector_index()
        print("系统已经初始化完成")

    def load_stopwords(self):
        """加载中文停用词库，在chinese_tokenizer里面使用"""
        stopwords_file = Path("中文停用词库.txt")
        stopwords = set()#为什么用集合？

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



    def load_documents(self):
        """加载文档"""
        print("正在加载红楼梦文档...")
        for file_path in self.docs_dir.glob("*.txt"):
            # print(file_path,type(file_path))
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
        print(f"共加载{len(self.documents)}个文档")

    def split_text_chunks(self,text:str,chunk_size:int=300):
        """将文本分割成块，这就是一个工具"""
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

    def preprocess_document(self):
        #先检查缓存
        if self.chunks_cache.exists():
            print("发现文档快缓存，正在加载....")
            with open(self.chunks_cache, "rb") as f:
                self.doc_chunks = pickle.load(f)
            print(f"从缓存加载了{len(self.doc_chunks)}个文档块")
            return

        """分块的预处理文档"""
        for doc in self.documents:
            chunks = self.split_text_chunks(doc['content'])
            for i,chunk in enumerate(chunks):
                self.doc_chunks.append({
                    'content': chunk,
                    'source':doc['filename'],
                    'chunk_id':i,
                    'full_path':doc['path']
                })

        # 保存缓存
        with open(self.chunks_cache, "wb") as f:
            pickle.dump(self.doc_chunks, f)


        print(f"文档预处理完成，共生成{len(self.doc_chunks)}个文档")

    def chinese_tokenizer(self,text):
        #用来处理当前块的分词逻辑，同时作为参数（一个函数）传入下面的向量化器tokenizer
        """中文分词器"""
        #1、使用jieba库来进行分词
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


        #一个构建向量库的函数
        """公式计算
        	TF-IDE = 词频(TF) × 逆文档频率(IDF)
        	TF = 某个词在文章中的出现次数 / 文章的总次数
        	IDF = log(语料库的文档总数 / 包含该词的文档数 + 1)
        """
        # train = ["Chinese Beijing Chinese",
        #          "Chinese Chinese shanghai",
        #          "Chinese Macao",
        #          "Tokyo Japan, Chinese"]
        # tf = TfidfVectorizer() #生成tfidf向量化器
        # tf.fit(train) #语料库结果
        # print(tf.get_feature_names_out())
        # test = ["Chinese Chinese Chinese Tokyo Japan"]
        # tf_fit = tf.transform(test)
        # print(tf_fit.toarray())
        """构建向量索引"""
        print("正在构建向量索引....")
        self.vectorizer = TfidfVectorizer(
            tokenizer=self.chinese_tokenizer,
            max_features=5000, #能够取到的最大特征
            min_df=1, # min_df=n  忽略出现少于n次的词
            max_df=0.95, # 忽略出现大于95%以上的词
            ngram_range=(1, 2) #包含1-2个词的组合
        )
        """特征的判断（max_features该取多大？）
        1.较短：评论，推文
        2.中等：新闻文章，产品描述
        3.较长：学术性论文，技术文档，文学作品
        """
        text = [chunk['content'] for chunk in self.doc_chunks]
        self.doc_vectors = self.vectorizer.fit_transform(text)

        # 保存缓存
        cache_data = {
            'vectors': self.doc_vectors,
            'vocabulary': self.vectorizer.vocabulary_,
            'idf': self.vectorizer.idf_,
        }

        with open(self.vectors_cache, "wb") as f:
            pickle.dump(cache_data, f)

        print("向量索引构建完成")

    def search_chunks(self,query: str,top_k:int=10,similarity_threshold: float=0.01):
        if self.vectorizer is None or self.doc_vectors is None:
            raise ValueError("向量索引未构建，请先调用 build_vector_index()")

        # 向量化查询
        query_vector = self.vectorizer.transform([query])

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

        results = []
        for idx in top10_index:
            chunk = self.doc_chunks[idx].copy()
            chunk['similarity'] = float(similarities[idx])
            results.append(chunk)
        return results

    def generate_answers(self,query: str,context_chunks):
        context = "\n\n".join([f"文档片段{i+1}:{chunk['content']}" for i,chunk in enumerate(context_chunks)])
        system_prompt = """
# Role: 红楼梦研究专家

## Profile
- language: 中文
- description: 精通《红楼梦》文本及红学研究，能够深入解析作品的人物、情节、诗词及文化内涵
- background: 多年从事《红楼梦》研究与教学，参与过多项红学课题研究
- personality: 严谨细致，富有文人气质，善于引经据典
- expertise: 文本分析、人物研究、诗词鉴赏、文化解读
- target_audience: 红学爱好者、文学研究者、学生群体

## Skills

1. 文本解析能力
   - 情节梳理: 能准确还原小说情节脉络
   - 细节把握: 对文本细节有敏锐洞察力
   - 人物分析: 深入剖析人物性格与命运
   - 诗词解读: 精准解析书中诗词内涵

2. 学术研究能力
   - 文献考证: 熟悉各类红学研究成果
   - 文化阐释: 揭示作品背后的文化内涵
   - 比较研究: 能与其他文学作品进行对比
   - 版本鉴别: 了解不同版本差异

## Rules

1. 回答原则：
   - 基于文本: 所有回答必须严格依据原著文本
   - 严谨准确: 不妄加猜测，不传播未经考证的观点
   - 深度解析: 透过表面现象揭示深层含义
   - 客观公正: 避免个人主观臆断

2. 行为准则：
   - 引经据典: 重要观点需引用原文佐证
   - 语言典雅: 保持与原著相称的文雅风格
   - 层次分明: 回答要有逻辑性和条理性
   - 深入浅出: 复杂问题要解释得通俗易懂

3. 限制条件：
   - 不涉争议: 避免介入红学争议性话题
   - 不妄评续作: 对后四十回保持审慎态度
   - 不越文本: 不脱离文本过度解读
   - 不代作者: 不以作者口吻发表观点

## Workflows

- 目标: 提供专业准确的红楼梦解读
- 步骤 1: 仔细理解用户问题，明确询问重点
- 步骤 2: 检索相关文本段落，确认信息准确性
- 步骤 3: 组织回答内容，适当引用原文
- 步骤 4: 以典雅文风呈现完整解答
- 预期结果: 用户获得权威、深入的红楼梦知识

## Initialization
作为红楼梦研究专家，你必须遵守上述Rules，按照Workflows执行任务。
""".strip()

        user_prompt = f"""
基于以下的文档内容回答：
{context}
问题：{query}
""".strip()
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
        answers = self.generate_answers(question,relevant_chunks)
        print(answers)

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

def main():
    rag = RagSystem()
    rag.initialize()

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

        # 获取答案
        result = rag.ask(question)

        # 显示结果
        print(f"\n答案： {result['answers']}")

        if result['source']:
            print("\n相关的文档片段：")
            for i,source in enumerate(result['source'],1):
                print(f"{i}. 来源：{source['source']}(相似度：{source['similarity']:.3f})")
                print(f"内容预览：{source['content_preview']}")


if __name__ == "__main__":
    main()
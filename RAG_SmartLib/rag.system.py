import re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RagSystem:
    def __init__(self,api_key:str,docs_dir:str='docs'):
        self.api_key = api_key
        self.docs_dir = Path(docs_dir)
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

    def ask(self,question: str):
        # 搜索相关文档
        self.search_chunks(question)




def main():
    rag = RagSystem(api_key="deepseek_key")
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
        rag.ask(question)

if __name__ == "__main__":
    main()
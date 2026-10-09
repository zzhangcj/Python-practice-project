import re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer

class RagSystem:
    def __init__(self,api_key:str,docs_dir:str='docs'):
        self.api_key = api_key
        self.docs_dir = Path(docs_dir)
        # 文档存储
        self.documents = []
        self.doc_chunks = []
        self.vectorizer = None

    def initialize(self):
        print("智能图书检索系统初始化")
        self.load_documents()
        self.preprocess_document()
        self.build_vector_index()


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
        print(f"文档预处理完成，共生成{len(self.doc_chunks)}个文档")

    def chinese_tokenizer(self):
        #用来处理当前块的分词逻辑，同时作为下面tokenizer所需要的参数（一个函数）
        """中文分词器"""


    def build_vector_index(self):
        # #一个构建向量库的函数
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
        self.vectorizer.fit_transform(text)


def main():
    rag = RagSystem(api_key="deepseek_key")
    rag.initialize()

if __name__ == "__main__":
    main()
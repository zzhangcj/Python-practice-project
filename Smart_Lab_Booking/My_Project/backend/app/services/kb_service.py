import os

# 【关键：自动配置HF镜像，任何人拿到代码不用手动设置】
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

"""实现知识库的加载和搜索,kb的意思就是knowledge base"""

from chromadb.api.models.Collection import Collection
from chromadb.utils import embedding_functions
import chromadb
from app.config import BASE_DIR

KB_DIR = BASE_DIR / "data" / "kb"
CHROMA_DIR = BASE_DIR / "data" / "chroma"

# 全局变量，缓存embedding实例、向量集合，只初始化一次
_collection = None
_embedding_fn = None
EMBEDDING_MODEL_NAME = "BAAI/bge-small-zh-v1.5"


def get_embedding_fn():
    """懒加载 embedding 模型：只加载一次，之后复用同一个实例"""
    global _embedding_fn
    if _embedding_fn is not None:
        return _embedding_fn
    # SentenceTransformerEmbeddingFunction 自带类级缓存，同名模型也不会重复加载
    _embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL_NAME
    )
    return _embedding_fn


def get_collection() -> Collection:
    """向量库的初始化，懒加载实现"""
    global _embedding_fn, _collection

    # 懒加载：向量集合第一次使用才初始化
    if _collection is None:
        KB_DIR.mkdir(parents=True, exist_ok=True)
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        col = client.get_or_create_collection(
            name="lab_kb", embedding_function=get_embedding_fn()
        )
        # 向量库为空时，读取md文档入库
        if col.count() == 0:
            ids = []
            docs = []
            metas = []
            for path in sorted(KB_DIR.glob("*.md")):
                text = path.read_text(encoding="UTF-8").strip()
                if not text:
                    continue
                docs.append(text)
                ids.append(path.stem)
                metas.append({"source": path.name})
            if docs:
                col.add(ids=ids, documents=docs, metadatas=metas)
        _collection = col
    return _collection


def warmup():
    """启动时预热：把模型加载 + 首次检索的开销付在启动阶段，别落在第一个用户请求上"""
    col = get_collection()
    if col.count() > 0:
        col.query(query_texts=["预热"], n_results=1)


def search(query: str):
    """根据关键字去检索向量库"""
    col = get_collection()
    if col.count() == 0:
        return ""
    limit = min(5, col.count())
    res = col.query(query_texts=[query], n_results=limit)
    docs = (res.get("documents") or [[]])[0]
    metas = (res.get("metadatas") or [[]])[0]
    distances = (res.get("distances") or [[]])[0]

    """
    以下是检索出来的资料：
    [预约规则.md]

    # 实验室预约规则...

    
    [安全规范.md]

    安全规范....
    """
    score_parts = []
    for doc, metas, dist in zip(docs, metas, distances):
        # 0-1 越接近1表示越相关
        score = 1 / (1 + dist)
        if score < 0.5:
            continue
        name = metas.get("source") or ""
        score_parts.append({"score": score, "content": f"[{name}]\n{doc}"})
    print(f"检索出来的 score_parts：{score_parts}")
    score_parts.sort(key=lambda x: x["score"], reverse=True)
    final_parts = [item["content"] for item in score_parts[:2]]
    return "\n\n".join(final_parts)

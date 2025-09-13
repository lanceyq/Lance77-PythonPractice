import uuid
import requests
import chromadb


def ollama_embedding_by_api(text):
    res = requests.post(
        url="http://127.0.0.1:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )
    embedding = res.json()['embedding']
    return embedding

client = chromadb.PersistentClient(path="RAG/db/chroma_demo")            # 数据库 类似于=文件夹
collection = client.get_or_create_collection(name="collection_v1")   # 集合   类似于=表格


# 构造数据
documents = ["风寒感冒", "寒邪客胃", "心脾两虚"]                        # [ "风寒感冒", "寒邪客胃", "心脾两虚"]
ids = [str(uuid.uuid4()) for _ in documents]                        # [ "xx",      "yy",       "bb"]
embeddings = [ ollama_embedding_by_api(text) for text in documents]                # [ [-0.24,-0.12], [-0.4,-0.2], [0.89,-0.2]

# 插入数据
collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings
)

# 关键字搜索
qs = "感冒胃疼"
qs_embedding = ollama_embedding_by_api(qs)
res = collection.query(query_embeddings=[qs_embedding, ],query_texts=qs, n_results=2)

# n_results 表示相似度匹配前两个拿过来
print(res)

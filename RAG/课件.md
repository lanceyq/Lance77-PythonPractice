# 1.分块处理

```python
# 1.读取文件内容
with open("knowledge/中医v1.txt", encoding='utf-8', mode='r') as fp:
    data = fp.read()

# 2.根据换行切割
chunk_list = data.split("\n\n")
chunk_list = [chunk for chunk in chunk_list if chunk]
print(chunk_list)
```

```
风寒感冒
症状：恶寒重，发热轻，无汗，头痛，肢节酸痛，鼻塞声重，或鼻痒喷嚏，时流清涕，咽痒，咳嗽，咳痰稀薄色白，口不渴或渴喜热饮，舌苔薄白而润，脉浮或浮紧。
药方：荆防败毒散。药物组成包括荆芥、防风、羌活、独活、柴胡、前胡、川芎、枳壳、茯苓、桔梗、甘草等，具有辛温解表的功效。

风热感冒
症状：发热，微恶风，有汗，头胀痛，鼻塞流黄涕，咳嗽，痰黏或黄，咽燥，或咽喉红肿疼痛，口渴，舌尖边红，苔薄黄，脉浮数。
药方：银翘散。主要药物有金银花、连翘、桔梗、薄荷、竹叶、生甘草、荆芥穗、淡豆豉、牛蒡子等，能辛凉解表，清热解毒。

痰湿蕴肺
症状：咳嗽反复发作，咳声重浊，痰多，因痰而嗽，痰出咳平，痰黏腻或稠厚成块，色白或带灰色，每于早晨或食后则咳甚痰多，进甘甜油腻食物加重，胸闷，脘痞，呕恶，食少，体倦，大便时溏，舌苔白腻，脉象濡滑。
药方：二陈平胃散合三子养亲汤。二陈平胃散由半夏、陈皮、茯苓、甘草、苍术、厚朴组成，三子养亲汤由紫苏子、白芥子、莱菔子组成，可燥湿化痰，理气止咳。

胃痛
症状：胃痛暴作，恶寒喜暖，得温痛减，遇寒加重，口淡不渴，或喜热饮，舌淡苔薄白，脉弦紧。
药方：良附丸。由高良姜、香附组成，能温胃散寒，理气止痛。

脾胃虚寒
症状：胃痛隐隐，绵绵不休，喜温喜按，空腹痛甚，得食则缓，劳累或受凉后发作或加重，泛吐清水，神疲纳呆，四肢倦怠，手足不温，大便溏薄，舌淡苔白，脉虚弱或迟缓。
药方：黄芪建中汤。药物包含黄芪、桂枝、芍药、炙甘草、生姜、大枣、饴糖，可温中健脾，和胃止痛。

失眠
症状：不易入睡，多梦易醒，心悸健忘，神疲食少，伴头晕目眩，四肢倦怠，腹胀便溏，面色少华，舌淡苔薄，脉细无力。
药方：归脾汤。由白术、茯神、黄芪、龙眼肉、酸枣仁、人参、木香、炙甘草、当归、远志等组成，有补益心脾，养血安神之效。
```



# 2.向量化

- 下载并安装ollama

  ```
  参考视频：https://www.bilibili.com/video/BV1X5NreGEku/?p=2&vd_source=034d40dbd70722fa67fc0433747ea6b4
  ```

- 下载`nomic-embed-text`模型

  ```
  ollama pull nomic-embed-text
  ```

- 启动ollama服务

- 向量化

  ```
  pip install requests
  ```

  ```python
  import requests
  
  text = "感冒发烧"
  
  res = requests.post(
      url="http://127.0.0.1:11434/api/embeddings",
      json={
          "model": "nomic-embed-text",
          "prompt": text
      }
  )
  
  embedding_list = res.json()['embedding']
  
  print(text)
  print(len(embedding_list), embedding_list)
  ```

  

# 3.分块+向量化

```python
import requests
import functools


def file_chunk_list():
    # 1.读取文件内容
    with open("knowledge/中医v1.txt", encoding='utf-8', mode='r') as fp:
        data = fp.read()

    # 2.根据换行切割
    chunk_list = data.split("\n\n")
    return [chunk for chunk in chunk_list if chunk]


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


def run():
    chunk_list = file_chunk_list()
    for chunk in chunk_list:
        vector = ollama_embedding_by_api(chunk)
        print(len(vector), vector)


if __name__ == '__main__':
    run()
```



# 4.向量数据库

向量数据库有很多：chromadb、Faiss、Qdrant、Elasticsearch等等...



以 chromadb来做向量数据库。

```
pip install chromadb
```

```python
import uuid

import chromadb

client = chromadb.PersistentClient(path="db/chroma_demo")            # 数据库 类似于=文件夹
collection = client.get_or_create_collection(name="collection_v1")   # 集合   类似于=表格


# 构造数据
documents = ["风寒感冒", "寒邪客胃", "心脾两虚"]                        # [ "风寒感冒", "寒邪客胃", "心脾两虚"]
ids = [str(uuid.uuid4()) for _ in documents]                        # [ "xx",      "yy",       "bb"]
embeddings = [ 向量化函数(text) for text in documents]                # [ [-0.24,-0.12], [-0.4,-0.2], [0.89,-0.2]

# 插入数据
collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings
)

# 关键字搜索
qs = "感冒胃疼"
qs_embedding = 向量化函数(qs)
res = collection.query(query_embeddings=[qs_embedding, ],query_texts=qs, n_results=2)
```





```python
import uuid
import chromadb
import requests


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


def run():
    client = chromadb.PersistentClient(path="db/chroma_demo")

    # 创建集合
    if client.get_collection("collection_v1"):
        client.delete_collection("collection_v1")
    collection = client.get_or_create_collection(name="collection_v1")

    # 构造数据
    documents = ["风寒感冒", "寒邪客胃", "心脾两虚"]
    ids = [str(uuid.uuid4()) for _ in documents]
    embeddings = [ollama_embedding_by_api(text) for text in documents]

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
    # print(res)

    result = res["documents"][0]
    print(result)


if __name__ == '__main__':
    run()

```



# 5.文本生成模型（推理）

本实例以本地基于ollama部署的deepseek为例。

```
ollama pull deepseek-r1:1.5b
```

参考视频：https://www.bilibili.com/video/BV1X5NreGEku/?p=2&vd_source=034d40dbd70722fa67fc0433747ea6b4





```python
import requests

prompt = "今天天气怎么样？"

response = requests.post(
    url="http://127.0.0.1:11434/api/generate",
    json={
        "model": "deepseek-r1:1.5b",
        "prompt": prompt,
        "stream": False
    }
)
res = response.json()['response']
print(res)

```



# 6.集成

将所有功能集成到一起。



```python
import uuid
import chromadb
import requests


def file_chunk_list():
    # 1.读取文件内容
    with open("knowledge/中医v1.txt", encoding='utf-8', mode='r') as fp:
        data = fp.read()

    # 2.根据换行切割
    chunk_list = data.split("\n\n")
    return [chunk for chunk in chunk_list if chunk]


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


def ollama_generate_by_api(prompt):
    response = requests.post(
        url="http://127.0.0.1:11434/api/generate",
        json={
            "model": "deepseek-r1:1.5b",
            "prompt": prompt,
            "stream": False,
            'temperature': 0.1
        }
    )
    res = response.json()['response']
    return res


def initial():
    client = chromadb.PersistentClient(path="db/chroma_demo")

    # 创建集合
    client.delete_collection("collection_v2")
    collection = client.get_or_create_collection(name="collection_v2")

    # 构造数据

    documents = file_chunk_list()
    ids = [str(uuid.uuid4()) for _ in range(len(documents))]
    embeddings = [ollama_embedding_by_api(text) for text in documents]

    # 插入数据
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings
    )


def run():
    # 关键字搜索
    qs = "感冒"
    qs_embedding = ollama_embedding_by_api(qs)

    client = chromadb.PersistentClient(path="db/chroma_demo")
    collection = client.get_collection(name="collection_v2")
    res = collection.query(query_embeddings=[qs_embedding, ], query_texts=qs, n_results=2)
    result = res["documents"][0]
    context = "\n".join(result)
    print(context)
    prompt = f"""你是一个中医问答机器人，任务是根据参考信息回答用户问题，如果参考信息不足以回答用户问题，请回复不知道，不要去杜撰任何信息，请用中文回答。
    参考信息：{context}，来回答问题：{qs}，
    """
    result = ollama_generate_by_api(prompt)
    print(result)


if __name__ == '__main__':
    initial()
    run()

```








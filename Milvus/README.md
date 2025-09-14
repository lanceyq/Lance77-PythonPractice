# Milvus Docker部署指南

本目录包含在Docker中部署Milvus向量数据库的配置文件。

## 组件说明

部署的Milvus包含以下组件：
- Milvus 2.2.14（独立模式）
- ETCD 3.5.5（元数据存储）
- MinIO（对象存储）

## 端口映射

- Milvus服务端口：19530
- Milvus监控端口：9091
- MinIO控制台端口：9001

## 使用方法

### 启动Milvus

1. 确保已安装Docker和Docker Compose
2. 在当前目录下运行以下命令：

```bash
docker-compose up -d
```

### 查看服务状态

```bash
docker-compose ps
```

### 查看日志

```bash
docker-compose logs milvus-standalone
```

### 停止Milvus

```bash
docker-compose down
```

### 数据持久化

数据将保存在以下目录中：
- ETCD数据：`./volumes/etcd`
- MinIO数据：`./volumes/minio`
- Milvus数据：`./volumes/milvus`

## 客户端连接

可以使用官方Python SDK（pymilvus）或其他语言的SDK连接到Milvus服务：

```python
from pymilvus import connections

connections.connect(
  alias="default",
  host='localhost',
  port='19530'
)
```
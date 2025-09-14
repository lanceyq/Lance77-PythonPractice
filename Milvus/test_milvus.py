#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Milvus向量数据库测试脚本
"""

from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
import numpy as np


def connect_to_milvus():
    """连接到Milvus服务"""
    print("正在连接到Milvus服务...")
    try:
        connections.connect(
            alias="default",
            host='localhost',
            port='19530'
        )
        print("Milvus服务连接成功！")
        return True
    except Exception as e:
        print(f"Milvus服务连接失败: {e}")
        return False


def create_collection():
    """创建集合"""
    # 定义字段
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=128)
    ]
    
    # 定义schema
    schema = CollectionSchema(fields, "测试集合")
    
    # 创建集合
    collection = Collection("test_collection", schema)
    print("集合创建成功！")
    
    # 创建索引
    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 128}
    }
    collection.create_index("vector", index_params)
    print("索引创建成功！")
    
    return collection


def insert_data(collection):
    """插入数据"""
    # 生成随机向量
    vectors = [[np.random.random() for _ in range(128)] for _ in range(1000)]
    
    # 插入数据
    collection.insert([vectors])
    print("数据插入成功！")
    
    # 加载集合到内存
    collection.load()
    print("集合加载到内存成功！")


def search_data(collection):
    """搜索数据"""
    # 生成查询向量
    query_vector = [[np.random.random() for _ in range(128)]]
    
    # 执行搜索
    search_params = {
        "metric_type": "L2",
        "params": {"nprobe": 10}
    }
    
    results = collection.search(
        data=query_vector,
        anns_field="vector",
        param=search_params,
        limit=5,
        expr=None,
        output_fields=["id"]
    )
    
    print("搜索结果:")
    for hits in results:
        for hit in hits:
            print(f"ID: {hit.id}, 距离: {hit.distance}")


def clean_up(collection):
    """清理资源"""
    # 释放集合
    collection.release()
    # 删除集合
    utility.drop_collection("test_collection")
    print("集合已删除！")


def main():
    """主函数"""
    # 连接到Milvus
    if not connect_to_milvus():
        print("请确保Milvus服务已启动，然后再运行此脚本。")
        return
    
    # 创建集合
    collection = create_collection()
    
    try:
        # 插入数据
        insert_data(collection)
        
        # 搜索数据
        search_data(collection)
    finally:
        # 清理资源
        clean_up(collection)
        
        # 断开连接
        connections.disconnect("default")
        print("已断开与Milvus服务的连接。")


if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
"""
@Time ： 2026/6/10
@Auth ： 冯成
@File ： factory.py
@IDE ： PyCharm
"""
import os
import sys

def get_project_root() -> str:
    """自动向上递归查找项目根目录（依据存在utils文件夹判断）"""
    current = os.path.abspath(__file__)
    while True:
        parent_dir = os.path.dirname(current)
        # 判断当前父目录下是否存在utils文件夹，找到就返回
        utils_dir = os.path.join(parent_dir, "utils")
        if os.path.isdir(utils_dir):
            return parent_dir
        # 到磁盘根目录还没找到，抛出异常
        if parent_dir == current:
            raise FileNotFoundError("未找到包含utils文件夹的项目根目录")
        current = parent_dir

# 注入路径
root_path = get_project_root()
if root_path not in sys.path:
    sys.path.append(root_path)
print("项目根目录：", root_path)

from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import BaseChatModel
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from utils.config_handler import rag_conf



class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatTongyi(model=rag_conf["chat_model_name"])


class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"])

chat_model = ChatModelFactory().generator()
embed_model = EmbeddingsFactory().generator()
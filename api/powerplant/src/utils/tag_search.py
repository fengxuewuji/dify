"""
标签名称搜索工具
"""
import yaml
import re
import difflib
from typing import Dict, List


class TagSearchUtil:
    """标签搜索工具类"""
    
    def __init__(self, tag_names_file: str):
        self.tag_names_file = tag_names_file
        self._tag_names = None
    
    def _load_tag_names(self) -> Dict[str, str]:
        """加载标签名称"""
        if self._tag_names is None:
            try:
                with open(self.tag_names_file, "r", encoding="utf-8") as f:
                    self._tag_names = yaml.safe_load(f)
            except Exception as e:
                print(f"Error loading tag names file: {e}")
                self._tag_names = {}
        return self._tag_names
    
    def search_tag_names(self, keywords: str, similarity_threshold: float = 0.6) -> Dict[str, str]:
        """
        根据关键词搜索标签名称
        
        Args:
            keywords: 搜索关键词，支持逗号分隔多个关键词
            similarity_threshold: 相似度阈值
            
        Returns:
            匹配的标签名称字典
        """
        if not keywords:
            return {}
        
        tag_names = self._load_tag_names()
        if not tag_names:
            return {}
        
        # 解析关键词
        keyword_list = [kw.strip() for kw in re.split('[,，]', keywords)]
        scored_results = []
        
        for tag_key, tag_value in tag_names.items():
            max_score = 0
            for keyword in keyword_list:
                # 计算与标签键和值的相似度，取最大值
                key_score = difflib.SequenceMatcher(None, keyword, tag_key).ratio()
                value_score = difflib.SequenceMatcher(None, keyword, tag_value).ratio()
                score = max(key_score, value_score)
                
                if score > max_score:
                    max_score = score
            
            if max_score > similarity_threshold:
                scored_results.append((tag_key, tag_value, max_score))
        
        # 按相似度降序排序
        scored_results.sort(key=lambda x: x[2], reverse=True)
        
        # 返回相似度最高的那一组（可能有多个并列）
        if scored_results:
            top_score = scored_results[0][2]
            top_results = {k: v for k, v, s in scored_results if s == top_score}
            return top_results
        
        return {}
    
    def get_all_tag_names(self) -> Dict[str, str]:
        """获取所有标签名称"""
        return self._load_tag_names()
    
    def refresh_tag_names(self) -> None:
        """刷新标签名称缓存"""
        self._tag_names = None

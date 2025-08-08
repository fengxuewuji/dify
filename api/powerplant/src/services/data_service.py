"""
数据处理服务
处理耗差分析相关的业务逻辑
"""
from typing import Dict, Any, Optional
from sqlalchemy import text
from ..models import HCFX, DatabaseManager
from ..config import HCFX_COLUMN_NAMES, HCFX_TAG_NAMES_REVERSE
from .external_api import ExternalAPIService


class DataService:
    """数据服务类"""
    
    def __init__(self, db_manager: DatabaseManager, external_api: ExternalAPIService):
        self.db_manager = db_manager
        self.external_api = external_api
    
    def execute_sql_query(self, sql_query: str) -> list:
        """执行SQL查询"""
        if not sql_query:
            raise ValueError("SQL query is required")
        
        with self.db_manager.get_engine().connect() as connection:
            result = connection.execute(text(sql_query))
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
    
    def get_latest_hcfx_mock(self) -> Optional[Dict[str, Any]]:
        """从数据库获取最新的耗差分析数据（模拟数据）"""
        session = self.db_manager.get_session()
        try:
            latest_record = session.query(HCFX).order_by(HCFX.id.desc()).first()
            if latest_record:
                result = {col.name: getattr(latest_record, col.name) 
                         for col in HCFX.__table__.columns}
                # 转换列名并排除id字段
                result = {HCFX_COLUMN_NAMES.get(k, k): v 
                         for k, v in result.items() if k != 'id'}
                return result
            return None
        finally:
            session.close()
    
    def get_real_hcfx_data(self, tag_names: Dict[str, str]) -> Dict[str, Any]:
        """获取实时耗差分析数据"""
        return self.external_api.get_realtime_value(tag_names)
    
    def get_top_hcfx_value(self, tag_names: Dict[str, str]) -> Dict[str, Any]:
        """获取耗差分析中的最大值"""
        real_data = self.external_api.get_realtime_value(tag_names)
        # 过滤掉值为None的数据
        real_data = {k: v for k, v in real_data.items() if v is not None}
        
        if not real_data:
            return {}
        
        # 找到最大值
        max_value = max(real_data.values())
        max_values = {k: v for k, v in real_data.items() if v == max_value}
        
        # 转换回标签名
        max_values = {HCFX_TAG_NAMES_REVERSE[k]: v for k, v in max_values.items()}
        
        return max_values
    
    def get_history_hcfx_data(self, tag_name: str, days: int = 3) -> Dict[str, Any]:
        """获取历史耗差分析数据"""
        return self.external_api.get_history_data_by_days(tag_name, days)
    
    def get_common_history_data(self, tag_name: str, end_time_str: str, 
                              time_span: int, data_num: int = 12) -> Dict[str, Any]:
        """获取通用历史数据"""
        return self.external_api.get_common_history_data(
            tag_name, end_time_str, time_span, data_num
        )

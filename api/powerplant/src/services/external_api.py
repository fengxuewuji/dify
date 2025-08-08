"""
外部API服务
处理与外部数据源的交互
"""
import requests
import json
import time
import pandas as pd
from typing import Dict, Any, Optional, List


class ExternalAPIService:
    """外部API服务类"""
    
    def __init__(self, base_url: str, db_name: str, username: str, password: str):
        self.base_url = base_url
        self.db_name = db_name
        self.username = username
        self.password = password
        self._token = None
        self._token_expires = 0
    
    def _parse_json_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """解析JSON响应"""
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return None
    
    def _get_token(self) -> Optional[str]:
        """获取认证token"""
        # 如果token还未过期，直接返回
        if self._token and time.time() < self._token_expires:
            return self._token
            
        url = f'{self.base_url}/v1/login'
        headers = {'Content-Type': 'application/json'}
        data = {
            "dbName": self.db_name,
            "userName": self.username,
            "password": self.password
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            self._token = result.get('token')
            # 假设token有效期为1小时
            self._token_expires = time.time() + 3600
            return self._token
        except requests.RequestException as e:
            print(f"Error getting token: {e}")
            return None
    
    def get_realtime_value(self, tag_names: Dict[str, str]) -> Dict[str, Any]:
        """获取实时数据"""
        token = self._get_token()
        if not token:
            return {}
        
        url = f'{self.base_url}/v1/getRealtimeValue'
        headers = {
            'Content-Type': 'application/json',
            'token': token,
        }
        data = {
            "dbName": self.db_name,
            "tagNames": list(tag_names.keys()),
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            parsed_response = self._parse_json_response(response.text)
            
            if not parsed_response or 'data' not in parsed_response:
                return {}
            
            # 合并所有数据
            all_data = {}
            for item in parsed_response['data']:
                all_data.update(item)
            
            # 根据tag_names映射返回结果
            real_data = {}
            for tag_key, display_name in tag_names.items():
                real_data[display_name] = all_data.get(tag_key)
            
            return real_data
            
        except requests.RequestException as e:
            print(f"Error getting realtime value: {e}")
            return {}
    
    def get_history_resample_value(self, tag_name: str, start_time: int, end_time: int, 
                                 resample_period_ms: int) -> Dict[str, Any]:
        """获取历史重采样数据"""
        token = self._get_token()
        if not token:
            return {}
        
        url = f'{self.base_url}/v1/getHisResampleValue'
        headers = {
            'Content-Type': 'application/json',
            'token': token,
        }
        data = {
            "dbName": self.db_name,
            "tagName": tag_name,
            "startMsTime": start_time,
            "endMsTime": end_time,
            "resampleMode": 1,
            "resamplePriodMs": resample_period_ms,
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            parsed_response = self._parse_json_response(response.text)
            
            if not parsed_response or 'data' not in parsed_response or not parsed_response['data']:
                return {}
            
            # 组织返回数据
            real_data = {}
            for item in parsed_response['data']:
                real_data[item['t']] = item[tag_name]
            
            return real_data
            
        except requests.RequestException as e:
            print(f"Error getting history resample value: {e}")
            return {}
    
    def get_common_history_data(self, tag_name: str, end_time_str: str, 
                              time_span: int, data_num: int = 12) -> Dict[str, float]:
        """获取通用历史数据"""
        if data_num < 1 or data_num > 100:
            raise ValueError("dataNum must be between 1 and 100")
        
        # 时间转换
        end_time = int(time.mktime(time.strptime(end_time_str, '%Y-%m-%d %H:%M:%S'))) * 1000
        start_time = end_time - time_span
        
        # 计算重采样周期
        resample_period_ms = max((end_time - start_time) // data_num, 1000)
        
        # 获取历史数据
        real_data = self.get_history_resample_value(
            tag_name, start_time, end_time, resample_period_ms
        )
        
        if not real_data:
            return {}
        
        # 只返回最后data_num条数据并格式化
        sorted_data = sorted(real_data.items())[-data_num:]
        
        # 转换为DataFrame进行时间格式化
        df = pd.DataFrame(sorted_data, columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'] + 8 * 3600 * 1000, unit='ms').dt.strftime('%Y-%m-%d %H:%M')
        df.set_index('timestamp', inplace=True)
        df = df.round(2)
        
        return df.to_dict()['value']
    
    def get_history_data_by_days(self, tag_name: str, days: int = 3) -> Dict[str, float]:
        """根据天数获取历史数据"""
        now = int(time.time() * 1000)
        start_time = now - days * 24 * 3600 * 1000
        resample_period_ms = 5 * 60 * 1000  # 5分钟重采样
        
        real_data = self.get_history_resample_value(
            tag_name, start_time, now, resample_period_ms
        )
        
        if not real_data:
            return {}
        
        # 格式化时间戳
        df = pd.DataFrame(list(real_data.items()), columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'] + 8 * 3600 * 1000, unit='ms').dt.strftime('%Y-%m-%d %H:%M')
        df.set_index('timestamp', inplace=True)
        df = df.round(2)
        
        return df.to_dict()['value']

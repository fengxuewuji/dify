"""
数据库模型定义
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymysql

Base = declarative_base()

class HCFX(Base):
    """耗差分析数据表模型"""
    __tablename__ = 'HCFX'
    
    id = Column(Integer, primary_key=True)
    boiler_eff = Column(Float)  # 锅炉效率耗差
    turbine_base_heat_rate = Column(Float)  # 汽轮机基础热耗率耗差
    hp_valve = Column(Float)  # 高调阀运行方式耗差
    sh_temp = Column(Float)  # 主汽温度耗差
    rh_temp = Column(Float)  # 再热汽温度耗差
    sh_de_water = Column(Float)  # 过热减温水流量耗差
    rh_de_water = Column(Float)  # 再热减温水流量耗差
    back_pres_ = Column(Float)  # 运行背压耗差
    hp_heater_1_up = Column(Float)  # 1号高加上端差耗差
    hp_heater_1_down = Column(Float)  # 1号高加下端差耗差
    hp_heater_2_up = Column(Float)  # 2号高加上端差耗差
    hp_heater_2_down = Column(Float)  # 2号高加下端差耗差
    hp_heater_3_up = Column(Float)  # 3号高加上端差耗差
    hp_heater_3_down = Column(Float)  # 3号高加下端差耗差
    lp_heater_5_up = Column(Float)  # 5号低加上端差耗差
    lp_heater_5_down = Column(Float)  # 5号低加下端差耗差
    lp_heater_6_up = Column(Float)  # 6号低加上端差耗差
    lp_heater_6_down = Column(Float)  # 6号低加下端差耗差
    lp_heater_7_up = Column(Float)  # 7号低加上端差耗差
    lp_heater_7_down = Column(Float)  # 7号低加下端差耗差
    inner_leakage = Column(Float)  # 热力系统内漏耗差
    makeup_water = Column(Float)  # 发电补水率耗差
    industrial_heat_supply = Column(Float)  # 工业供汽供热比耗差
    life_heat_supply = Column(Float)  # 采暖供热比耗差
    air_heater = Column(Float)  # 暖风器投运耗差
    butterfly_valve = Column(Float)  # 连通管蝶阀节流损失耗差
    output_coef = Column(Float)  # 出力系数耗差
    peak_vally_diff = Column(Float)  # 峰谷差耗差

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, database_uri):
        self.database_uri = database_uri
        self.engine = None
        self.Session = None
        
    def initialize(self):
        """初始化数据库连接"""
        try:
            self.engine = create_engine(self.database_uri)
            self.Session = sessionmaker(bind=self.engine)
            return True
        except pymysql.Error as e:
            print(f"Error connecting to the database: {e}")
            return False
    
    def get_session(self):
        """获取数据库会话"""
        if self.Session is None:
            self.initialize()
        return self.Session()
    
    def get_engine(self):
        """获取数据库引擎"""
        if self.engine is None:
            self.initialize()
        return self.engine

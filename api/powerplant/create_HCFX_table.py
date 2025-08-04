import pandas as pd
import numpy as np
import sqlalchemy as sa
from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建文件的绝对路径
file_path = r'/home/zyp/power/shouguang/HCFX.csv'

# 创建数据库连接
# 请根据你的实际情况修改连接字符串（用户名、密码等）
engine = create_engine('mysql+pymysql://root:MS_zyp1121@localhost:3306/dify_db')

# 创建基类
Base = declarative_base()

# 定义表结构
class HCFX(Base):
    __tablename__ = 'HCFX'
    
    id = Column(Integer, primary_key=True)
    boiler_eff = Column(Float)
    turbine_base_heat_rate = Column(Float)
    hp_valve = Column(Float)
    sh_temp = Column(Float)
    rh_temp = Column(Float)
    sh_de_water = Column(Float)
    rh_de_water = Column(Float)
    back_pres_ = Column(Float)
    hp_heater_1_up = Column(Float)
    hp_heater_1_down = Column(Float)
    hp_heater_2_up = Column(Float)
    hp_heater_2_down = Column(Float)
    hp_heater_3_up = Column(Float)
    hp_heater_3_down = Column(Float)
    lp_heater_5_up = Column(Float)
    lp_heater_5_down = Column(Float)
    lp_heater_6_up = Column(Float)
    lp_heater_6_down = Column(Float)
    lp_heater_7_up = Column(Float)
    lp_heater_7_down = Column(Float)
    inner_leakage = Column(Float)
    makeup_water = Column(Float)
    industrial_heat_supply = Column(Float)
    life_heat_supply = Column(Float)
    air_heater = Column(Float)
    butterfly_valve = Column(Float)
    output_coef = Column(Float)
    peak_vally_diff = Column(Float)

# 创建表
Base.metadata.create_all(engine)

# 将DataFrame数据转换为可插入数据库的格式
def df_to_db(df):
    # 创建一个数据副本，避免修改原始数据
    df_copy = df.copy()
    
    # 将所有的NaN值替换为None (Python的NULL)
    df_copy = df_copy.replace({np.nan: None})

    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # 遍历DataFrame的每一行
        for _, row in df_copy.iterrows():
            # 创建表记录
            record = HCFX(
                # 如果列名不完全匹配，请根据实际情况调整
                boiler_eff=row['锅炉效率'],
                turbine_base_heat_rate=row['汽轮机基础热耗率'],
                hp_valve=row['高调阀运行方式'],
                sh_temp=row['主汽温度'],
                rh_temp=row['再热汽温度'],
                sh_de_water=row['过热减温水流量'],
                rh_de_water=row['再热减温水流量'],
                back_pres_=row['运行背压'],
                hp_heater_1_up=row['1号高加上端差'],
                hp_heater_1_down=row['1号高加下端差'],
                hp_heater_2_up=row['2号高加上端差'],
                hp_heater_2_down=row['2号高加下端差'],
                hp_heater_3_up=row['3号高加上端差'],
                hp_heater_3_down=row['3号高加下端差'],
                lp_heater_5_up=row['5号低加上端差'],
                lp_heater_5_down=row['5号低加下端差'],
                lp_heater_6_up=row['6号低加上端差'],
                lp_heater_6_down=row['6号低加下端差'],
                lp_heater_7_up=row['7号低加上端差'],
                lp_heater_7_down=row['7号低加下端差'],
                inner_leakage=row['热力系统内漏'],
                makeup_water=row['发电补水率'],
                industrial_heat_supply=row['工业供汽供热比'],
                life_heat_supply=row['采暖供热比'],
                air_heater=row['暖风器投运'],
                butterfly_valve=row['连通管蝶阀节流损失'],
                output_coef=row['出力系数'],
                peak_vally_diff=row['峰谷差'],
            )
            session.add(record)
        
        # 提交事务
        session.commit()
        print("数据已成功导入到数据库")
    except Exception as e:
        session.rollback()
        print(f"导入数据时出错: {e}")
    finally:
        session.close()

df = pd.read_csv(file_path)

# 调用函数将数据导入数据库
df_to_db(df)
"""
常量配置文件
包含标签名称映射、公式定义等常量
"""

# 耗差分析标签名称映射
HCFX_TAG_NAMES = {
    'JCYY:U4_MH_GLXL': '锅炉效率耗差(g/kWh)',
    'JCYY:U4_MH_JCRH': '汽轮机基础热耗率耗差(g/kWh)',
    'JCYY:U4_MH_GTF': '高调阀运行方式耗差(g/kWh)',
    'JCYY:U4_MH_ZZQWD': '主汽温度耗差(g/kWh)',
    'JCYY:U4_MH_ZRZQWD': '再热汽温度耗差(g/kWh)',
    'JCYY:U4_MH_GRJWS': '过热减温水流量耗差(g/kWh)',
    'JCYY:U4_MH_ZRJWS': '再热减温水流量耗差(g/kWh)',
    'JCYY:U4_MH_YXBY': '运行背压耗差(g/kWh)',
    'JCYY:U4_MH_1GJSDC': '1号高加上端差耗差(g/kWh)',
    'JCYY:U4_MH_1GJXDC': '1号高加下端差耗差(g/kWh)',
    'JCYY:U4_MH_2GJSDC': '2号高加上端差耗差(g/kWh)',
    'JCYY:U4_MH_2GJXDC': '2号高加下端差耗差(g/kWh)',
    'JCYY:U4_MH_3GJSDC': '3号高加上端差耗差(g/kWh)',
    'JCYY:U4_MH_3GJXDC': '3号高加下端差耗差(g/kWh)',
    'JCYY:U4_MH_5DJSDC': '5号低加上端差耗差(g/kWh)',
    'JCYY:U4_MH_5DJXDC': '5号低加下端差耗差(g/kWh)',
    'JCYY:U4_MH_6DJSDC': '6号低加上端差耗差(g/kWh)',
    'JCYY:U4_MH_6DJXDC': '6号低加下端差耗差(g/kWh)',
    'JCYY:U4_MH_7DJSDC': '7号低加上端差耗差(g/kWh)',
    'JCYY:U4_MH_7DJXDC': '7号低加下端差耗差(g/kWh)',
    'inner_leakage': '热力系统内漏耗差(g/kWh)',
    'JCYY:U4_MH_FDBSL': '发电补水率耗差(g/kWh)',
    'JCYY:U4_MH_GYGQGRB': '工业供汽供热比耗差(g/kWh)',
    'JCYY:U4_MH_CNGRB': '采暖供热比耗差(g/kWh)',
    'JCYY:U4_MH_NFQTY': '暖风器投运耗差(g/kWh)',
    'JCYY:U4_MH_LTGJLSS': '连通管蝶阀节流损失耗差(g/kWh)',
    'JCYY:U4_MH_CLXS': '出力系数耗差(g/kWh)',
    'JCYY:U4_MH_FGC': '峰谷差耗差(g/kWh)',
}

# 反向映射
HCFX_TAG_NAMES_REVERSE = {v: k for k, v in HCFX_TAG_NAMES.items()}

# 损失数据标签名称
LOSS_TAG_NAMES = {
    'JCYY:U4_BOILER_Q2': 'q2',
    'JCYY:U4_BOILER_Q3': 'q3',
    'JCYY:U4_BOILER_Q4': 'q4',
    'JCYY:U4_BOILER_Q5': 'q5',
    'JCYY:U4_BOILER_Q_OTHER': 'q6',
}

# 性能指数标签名称
XNJS_TAG_NAMES = {
    'JCYY:U4_BOILER_EFF': '锅炉计算效率(%)',
    'JCYY:U4_GYGXL': '汽轮机高压缸效率(%)',
}

# 耗差公式（TODO: 需要根据实际情况进行调整，可考虑移到yaml文件）
HCFX_FORMULA = {
    '锅炉效率耗差(g/kWh)': '锅炉计算效率 - 锅炉设计效率',
}

# 数据库列名映射
HCFX_COLUMN_NAMES = {
    'boiler_eff': '锅炉效率耗差(g/kWh)',
    'turbine_base_heat_rate': '汽轮机基础热耗率耗差(g/kWh)',
    'hp_valve': '高调阀运行方式耗差(g/kWh)',
    'sh_temp': '主汽温度耗差(g/kWh)',
    'rh_temp': '再热汽温度耗差(g/kWh)',
    'sh_de_water': '过热减温水流量耗差(g/kWh)',
    'rh_de_water': '再热减温水流量耗差(g/kWh)',
    'back_pres_': '运行背压耗差(g/kWh)',
    'hp_heater_1_up': '1号高加上端差耗差(g/kWh)',
    'hp_heater_1_down': '1号高加下端差耗差(g/kWh)',
    'hp_heater_2_up': '2号高加上端差耗差(g/kWh)',
    'hp_heater_2_down': '2号高加下端差耗差(g/kWh)',
    'hp_heater_3_up': '3号高加上端差耗差(g/kWh)',
    'hp_heater_3_down': '3号高加下端差耗差(g/kWh)',
    'lp_heater_5_up': '5号低加上端差耗差(g/kWh)',
    'lp_heater_5_down': '5号低加下端差耗差(g/kWh)',
    'lp_heater_6_up': '6号低加上端差耗差(g/kWh)',
    'lp_heater_6_down': '6号低加下端差耗差(g/kWh)',
    'lp_heater_7_up': '7号低加上端差耗差(g/kWh)',
    'lp_heater_7_down': '7号低加下端差耗差(g/kWh)',
    'inner_leakage': '热力系统内漏耗差(g/kWh)',
    'makeup_water': '发电补水率耗差(g/kWh)',
    'industrial_heat_supply': '工业供汽供热比耗差(g/kWh)',
    'life_heat_supply': '采暖供热比耗差(g/kWh)',
    'air_heater': '暖风器投运耗差(g/kWh)',
    'butterfly_valve': '连通管蝶阀节流损失耗差(g/kWh)',
    'output_coef': '出力系数耗差(g/kWh)',
    'peak_vally_diff': '峰谷差耗差(g/kWh)',
}

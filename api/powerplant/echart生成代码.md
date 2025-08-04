```python
import json
 
def main():
    option = {
        "title": {
            "text": 'Stacked Line'
        },
        "tooltip": {
            "trigger": 'axis'
        },
        "legend": {
            "data": ['Email', 'Union Ads', 'Video Ads', 'Direct', 'Search Engine']
        },
        "grid": {
            "left": '3%',
            "right": '4%',
            "bottom": '3%',
            "containLabel": True
        },
        "toolbox": {
            "feature": {
            "saveAsImage": {}
            }
        },
        "xAxis": {
            "type": 'category',
            "boundaryGap": False,
            "data": ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        "yAxis": {
            "type": 'value'
        },
        "series": [
            {
            "name": 'Email',
            "type": 'line',
            "stack": 'Total',
            "data": [120, 132, 101, 134, 90, 230, 210]
            },
        ]
    };
 
    # 将字典转换为格式化的 JSON 字符串
    option_json = json.dumps(option, indent=2)
    
    # 构建正确的 Markdown 代码块
    output = "```echarts\n" + option_json + "\n```"
    
    return {"result": output}

```
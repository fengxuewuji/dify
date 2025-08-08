# Dify工作流集成示例

## 在Dify中使用文档生成API

### 1. HTTP请求节点配置

#### Word文档生成节点
```yaml
节点类型: HTTP请求
请求方法: POST
URL: http://localhost:6002/generate/word
请求头:
  Content-Type: application/json
  
请求体示例:
{
  "filename": "{{filename}}.docx",
  "content": "{{report_content}}",
  "options": {
    "title": "{{report_title}}",
    "titleSize": 20,
    "font": "SimSun",
    "fontSize": 12,
    "lineSpacing": 1.5,
    "align": "JUSTIFY",
    "margins": {
      "left": 2.5,
      "right": 2.5,
      "top": 2.5,
      "bottom": 2.5
    },
    "header": "{{company_name}} • 内部资料",
    "footer": "{{current_date}} • 保密文档",
    "table": {{data_table}}
  }
}
```

#### PDF文档生成节点  
```yaml
节点类型: HTTP请求
请求方法: POST
URL: http://localhost:6002/generate/pdf
请求头:
  Content-Type: application/json
  
请求体示例:
{
  "filename": "{{filename}}.pdf",
  "content": "{{analysis_content}}",
  "options": {
    "title": "{{analysis_title}}",
    "font": "NotoSansCJKsc",
    "fontSize": 12,
    "pageSize": "A4",
    "marginLeft": 2.5,
    "marginRight": 2.5,
    "header": "{{department}} • {{year}}年度报告",
    "footer": "版权所有 © {{company_name}}"
  }
}
```

### 2. 工作流示例

#### 耗差分析报告生成工作流
```mermaid
graph LR
    A[用户输入] --> B[获取实时数据]
    B --> C[数据分析处理]
    C --> D[生成报告内容]
    D --> E[调用文档API]
    E --> F[返回文档文件]
```

#### 具体节点配置

**节点1: 获取耗差数据**
```yaml
节点类型: HTTP请求
URL: http://localhost:6002/hcfx/real
方法: GET
输出变量: hcfx_data
```

**节点2: 数据处理**
```yaml
节点类型: Code
代码:
def main(hcfx_data):
    # 找出最大耗差
    max_item = max(hcfx_data.items(), key=lambda x: x[1] if x[1] else 0)
    
    # 格式化表格数据
    table_data = [["项目", "数值", "单位"]]
    for key, value in hcfx_data.items():
        if value is not None:
            table_data.append([key, str(value), "g/kWh"])
    
    # 生成分析内容
    content = f"""
根据当前实时数据分析，设备运行状态如下：

最大耗差项目：{max_item[0]}
数值：{max_item[1]} g/kWh

详细分析：
各耗差分量中，{max_item[0]}数值最高，需要重点关注。
建议检查相关设备运行参数，分析产生耗差的原因。

数据采集时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """.strip()
    
    return {
        "report_content": content,
        "table_data": table_data,
        "max_item": max_item[0]
    }
```

**节点3: 生成Word报告**
```yaml
节点类型: HTTP请求
URL: http://localhost:6002/generate/word
方法: POST
请求体:
{
  "filename": "耗差分析报告_{{date}}.docx",
  "content": "{{report_content}}",
  "options": {
    "title": "机组耗差分析报告",
    "titleSize": 18,
    "font": "SimSun",
    "fontSize": 12,
    "lineSpacing": 1.5,
    "align": "JUSTIFY",
    "header": "发电厂运行部 • 耗差分析",
    "footer": "{{current_datetime}} • 内部资料",
    "table": {
      "data": {{table_data}},
      "style": "Table Grid"
    }
  }
}
```

### 3. 工作流模板

#### 模板1: 设备巡检报告
```json
{
  "workflow_name": "设备巡检报告生成",
  "trigger": "手动触发",
  "nodes": [
    {
      "id": "get_data",
      "type": "http_request",
      "config": {
        "url": "{{base_url}}/xnjs/real",
        "method": "GET"
      }
    },
    {
      "id": "generate_report",
      "type": "http_request", 
      "config": {
        "url": "{{base_url}}/generate/word",
        "method": "POST",
        "body": {
          "filename": "巡检报告_{{date}}.docx",
          "content": "{{inspection_content}}",
          "options": {
            "title": "设备巡检报告",
            "header": "运行部 • 巡检记录"
          }
        }
      }
    }
  ]
}
```

#### 模板2: 性能分析PDF
```json
{
  "workflow_name": "性能分析PDF生成",
  "nodes": [
    {
      "id": "performance_analysis",
      "type": "code",
      "config": {
        "code": "# 性能分析逻辑\nresult = analyze_performance(data)"
      }
    },
    {
      "id": "generate_pdf",
      "type": "http_request",
      "config": {
        "url": "{{base_url}}/generate/pdf", 
        "body": {
          "filename": "性能分析_{{timestamp}}.pdf",
          "options": {
            "title": "设备性能分析报告",
            "font": "NotoSansCJKsc",
            "pageSize": "A4"
          }
        }
      }
    }
  ]
}
```

### 4. 变量映射

在Dify工作流中，可以使用以下变量：

```yaml
# 系统变量
{{current_date}}      # 当前日期
{{current_datetime}}  # 当前日期时间
{{user_name}}         # 当前用户

# 自定义变量
{{company_name}}      # 公司名称
{{department}}        # 部门名称
{{report_title}}      # 报告标题
{{filename}}          # 文件名
{{base_url}}          # API基础URL

# 数据变量
{{hcfx_data}}         # 耗差数据
{{analysis_result}}   # 分析结果
{{table_data}}        # 表格数据
```

### 5. 错误处理

在工作流中添加错误处理节点：

```yaml
节点类型: Condition
条件: {{http_status}} == 200
成功分支: 继续处理
失败分支: 错误处理节点

错误处理节点:
  类型: Code
  代码: |
    def handle_error(error_response):
        return {
            "error_message": f"文档生成失败: {error_response.get('error', '未知错误')}",
            "success": False
        }
```

这样就可以在Dify中完整地使用文档生成功能了！

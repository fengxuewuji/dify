# 文档生成API使用说明

升级后的文档生成API支持丰富的排版格式控制，包括字体、对齐、页边距、表格、页眉页脚等功能。

## API接口

### 1. Word文档生成
**接口**: `POST /generate/word`

**基本参数**:
- `content`: 文档内容（支持\n换行）
- `filename`: 输出文件名（默认: document.docx）
- `options`: 排版选项（可选）

**排版选项 (options)**:

#### 基础设置
```json
{
  "title": "文档标题",
  "titleFont": "SimSun",      // 标题字体（宋体）
  "titleSize": 18,            // 标题字号
  "font": "SimSun",           // 正文字体
  "fontSize": 12,             // 正文字号
  "lineSpacing": 1.5,         // 行距
  "align": "JUSTIFY"          // 对齐方式: LEFT/CENTER/RIGHT/JUSTIFY
}
```

#### 页面设置
```json
{
  "margins": {                // 页边距（厘米）
    "left": 2.5,
    "right": 2.5,
    "top": 2.5,
    "bottom": 2.5
  },
  "header": "页眉内容",
  "footer": "页脚内容",
  "spaceBefore": 0,           // 段前间距（磅）
  "spaceAfter": 6,            // 段后间距（磅）
  "pageBreak": false          // 是否分页
}
```

#### 表格设置
```json
{
  "table": {
    "data": [                 // 二维数组
      ["列1", "列2", "列3"],
      ["数据1", "数据2", "数据3"]
    ],
    "style": "Table Grid",    // 表格样式
    "fontSize": 10            // 表格字号
  }
}
```

### 2. PDF文档生成
**接口**: `POST /generate/pdf`

**基本参数**:
- `content`: 文档内容
- `filename`: 输出文件名（默认: document.pdf）
- `options`: 排版选项（可选）

**排版选项 (options)**:

#### 字体设置
```json
{
  "font": "NotoSansCJKsc",                    // 字体名称
  "fontPath": "/usr/share/fonts/...",         // 字体文件路径
  "fontSize": 12,                             // 正文字号
  "titleSize": 18,                            // 标题字号
  "leading": 18                               // 行距
}
```

#### 页面设置
```json
{
  "pageSize": "A4",                           // 页面大小: A4/letter
  "marginLeft": 2,                            // 左边距（厘米）
  "marginRight": 2,                           // 右边距
  "marginTop": 2.5,                           // 上边距
  "marginBottom": 2.5,                        // 下边距
  "align": "LEFT"                             // 对齐: LEFT/CENTER/RIGHT/JUSTIFY
}
```

#### 页眉页脚
```json
{
  "header": "页眉内容",
  "footer": "页脚内容（支持页码变量）"
}
```

#### 表格设置
```json
{
  "table": {
    "data": [["列1", "列2"], ["数据1", "数据2"]],
    "fontSize": 10,
    "align": "CENTER"
  }
}
```

## 使用示例

### 示例1: 生成简单Word文档
```json
{
  "filename": "报告.docx",
  "content": "这是文档内容。\n\n这是第二段。"
}
```

### 示例2: 生成格式化Word文档
```json
{
  "filename": "设备报告.docx",
  "content": "设备运行正常。\n\n各项指标均在正常范围内。",
  "options": {
    "title": "设备运行报告",
    "titleSize": 20,
    "font": "SimSun",
    "fontSize": 12,
    "lineSpacing": 1.5,
    "align": "JUSTIFY",
    "margins": {"left": 3, "right": 3, "top": 2.5, "bottom": 2.5},
    "header": "内部资料",
    "footer": "保密文档",
    "table": {
      "data": [
        ["指标", "数值", "状态"],
        ["效率", "92%", "正常"],
        ["温度", "125℃", "正常"]
      ]
    }
  }
}
```

### 示例3: 生成PDF文档
```json
{
  "filename": "技术报告.pdf",
  "content": "技术分析报告内容...",
  "options": {
    "title": "技术分析报告",
    "font": "NotoSansCJKsc",
    "fontSize": 12,
    "pageSize": "A4",
    "marginLeft": 2.5,
    "marginRight": 2.5,
    "header": "技术部文档",
    "footer": "第 {page} 页"
  }
}
```

## 中文字体支持

### Ubuntu系统中文字体
```bash
# 安装中文字体
sudo apt-get install fonts-noto-cjk

# 常用字体路径
/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc
/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
```

### Word文档中文字体
- SimSun (宋体)
- SimHei (黑体)
- KaiTi (楷体)
- FangSong (仿宋)

## 错误处理

API会返回详细的错误信息：
```json
{
  "error": "具体错误描述"
}
```

## 与Dify集成

可以在Dify工作流中使用HTTP请求节点调用这些API：

1. 设置请求URL: `http://localhost:6002/generate/word` 或 `/generate/pdf`
2. 设置请求方法: POST
3. 设置请求头: `Content-Type: application/json`
4. 配置请求体，包含content和options参数
5. 处理返回的文件流

这样就可以在Dify中生成格式丰富的Word和PDF文档了！

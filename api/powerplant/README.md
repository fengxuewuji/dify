# PowerPlant API

一个用于电厂数据管理和文档生成的Flask API应用。

## 项目结构

```
powerplant/
├── src/                          # 源代码目录
│   ├── config/                   # 配置模块
│   │   ├── __init__.py
│   │   ├── constants.py          # 常量定义
│   │   └── settings.py           # 应用配置
│   ├── models/                   # 数据模型
│   │   ├── __init__.py
│   │   └── database.py           # 数据库模型和管理器
│   ├── services/                 # 业务服务层
│   │   ├── __init__.py
│   │   ├── external_api.py       # 外部API服务
│   │   ├── data_service.py       # 数据处理服务
│   │   └── document_service.py   # 文档生成服务
│   ├── controllers/              # 控制器层
│   │   ├── __init__.py
│   │   ├── database_controller.py
│   │   ├── hcfx_controller.py
│   │   ├── common_controller.py
│   │   └── document_controller.py
│   ├── utils/                    # 工具类
│   │   ├── __init__.py
│   │   └── tag_search.py
│   ├── __init__.py
│   └── app_factory.py            # 应用工厂
├── main.py                       # 主应用入口
├── requirements.txt              # 依赖包
├── .env.example                  # 环境变量示例
└── README.md                     # 项目说明
```

## 功能特性

### 数据管理
- 数据库查询接口
- 耗差分析数据获取（实时和历史）
- 损失数据获取
- 性能指数数据获取
- 标签名称搜索

### 文档生成
- Word文档生成
- PDF文档生成
- 支持自定义样式和格式

## API接口

### 数据库查询
- `POST /api/database/query` - 执行SQL查询

### 耗差分析
- `GET /api/hcfx/mock` - 获取模拟耗差数据
- `GET /api/hcfx/real` - 获取实时耗差数据
- `GET /api/hcfx/top1` - 获取最大耗差值
- `POST /api/hcfx/history` - 获取历史耗差数据

### 损失数据
- `GET /api/loss/real` - 获取实时损失数据

### 性能指数
- `GET /api/xnjs/real` - 获取实时性能指数

### 通用接口
- `POST /api/common/real` - 获取历史数据
- `POST /api/common/getTagNames` - 搜索标签名称
- `GET /api/common/getReason` - 获取耗差公式（待实现）

### 文档生成
- `POST /api/generate/word` - 生成Word文档
- `POST /api/generate/pdf` - 生成PDF文档

## 安装和运行

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件设置相应的配置
```

### 3. 运行应用
```bash
python main.py
```

## 配置说明

应用支持多环境配置：
- `development` - 开发环境
- `production` - 生产环境  
- `testing` - 测试环境

通过环境变量 `FLASK_ENV` 来切换环境。

## 扩展功能

### 添加新的数据源
1. 在 `src/services/` 下创建新的服务类
2. 在相应的控制器中添加路由
3. 在 `app_factory.py` 中注册新的蓝图

### 添加新的文档格式
1. 在 `src/services/document_service.py` 中添加新的生成器类
2. 在 `document_controller.py` 中添加对应的路由

### 数据库模型扩展
1. 在 `src/models/database.py` 中添加新的模型类
2. 更新相关的服务类以支持新模型

## 注意事项

1. 确保数据库连接配置正确
2. 外部API服务地址和认证信息需要正确配置
3. 文档生成功能需要相应的字体文件支持中文
4. 标签名称文件 `tag_names.yaml` 需要存在且格式正确

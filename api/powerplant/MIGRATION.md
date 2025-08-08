# 代码重构迁移指南

## 重构概述

原来的 `test.py` 文件已经被重构为模块化的架构，提高了代码的可维护性和可扩展性。

## 主要变化

### 1. 文件结构变化

**原来：**
- 单个 `test.py` 文件包含所有功能

**现在：**
```
src/
├── config/          # 配置管理
├── models/          # 数据模型
├── services/        # 业务逻辑
├── controllers/     # 路由控制
├── utils/           # 工具类
└── app_factory.py   # 应用工厂
```

### 2. API路径变化

所有的API路径都增加了 `/api` 前缀：

| 原路径 | 新路径 |
|--------|--------|
| `/query` | `/api/database/query` |
| `/hcfx/mock` | `/api/hcfx/mock` |
| `/hcfx/real` | `/api/hcfx/real` |
| `/hcfx/top1` | `/api/hcfx/top1` |
| `/hcfx/history` | `/api/hcfx/history` |
| `/loss/real` | `/api/loss/real` |
| `/xnjs/real` | `/api/xnjs/real` |
| `/common/real` | `/api/common/real` |
| `/getTagNames` | `/api/common/getTagNames` |
| `/getReason` | `/api/common/getReason` |
| `/generate/word` | `/api/generate/word` |
| `/generate/pdf` | `/api/generate/pdf` |

### 3. 运行方式变化

**原来：**
```bash
python test.py
```

**现在：**
```bash
python main.py
```

### 4. 配置管理

新增了环境变量配置支持：
- 复制 `.env.example` 为 `.env`
- 配置数据库连接、API地址等参数
- 支持多环境配置（开发、测试、生产）

## 迁移步骤

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境
```bash
cp .env.example .env
# 编辑 .env 文件设置配置项
```

### 3. 更新客户端代码
如果有客户端调用API，需要更新API路径（添加 `/api` 前缀）

### 4. 启动新应用
```bash
python main.py
```

## 新功能特性

### 1. 更好的错误处理
- 统一的错误响应格式
- 详细的错误日志

### 2. 健康检查
- 新增 `/health` 接口用于服务监控

### 3. 模块化架构
- 易于添加新功能
- 更好的代码组织
- 便于单元测试

### 4. 配置管理
- 支持环境变量配置
- 多环境支持
- 敏感信息保护

## 扩展开发

### 添加新的API接口
1. 在 `src/services/` 中添加业务逻辑
2. 在 `src/controllers/` 中添加路由处理
3. 在 `app_factory.py` 中注册蓝图
r
### 修改配置
1. 修改 `src/config/constants.py` 中的常量
2. 修改 `src/config/settings.py` 中的配置类

### 添加新的数据模型
1. 在 `src/models/database.py` 中添加模型类
2. 更新相关服务类

## 注意事项

1. 确保 `tag_names.yaml` 文件存在且格式正确
2. 数据库连接配置需要正确
3. 外部API服务配置需要更新
4. 客户端代码需要更新API路径

## 回滚方案

如果新版本有问题，可以临时回滚到 `test.py`：
```bash
python test.py
```

但建议尽快修复问题并迁移到新架构。

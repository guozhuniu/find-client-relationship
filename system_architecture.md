# 客户组织架构和人脉管理系统架构设计

## 系统概述

本系统旨在帮助用户管理客户公司的组织架构和人脉关系，通过爬虫从网络获取数据，构建完整的公司组织架构树，并分析人员之间的亲密关系。

## 技术栈选择

### 前端
- **框架**：React + TypeScript
- **UI组件库**：Ant Design（提供组织架构树组件）
- **状态管理**：Redux Toolkit
- **API调用**：Axios
- **样式**：CSS Modules + Less

### 后端
- **语言**：Node.js
- **框架**：Express
- **数据库**：MongoDB
- **认证**：JWT
- **缓存**：Redis

### 爬虫
- **语言**：Python
- **框架**：Scrapy
- **数据处理**：Pandas
- **新闻抓取**：BeautifulSoup

## 系统架构

### 三层架构
1. **前端层**：负责用户界面展示和交互
2. **后端层**：负责数据处理和业务逻辑
3. **爬虫层**：负责从网络获取数据

### 数据流
1. 爬虫从网络抓取公司和人员信息
2. 后端处理和存储数据
3. 前端展示组织架构和人员信息
4. 后端计算人员之间的亲密指数
5. 前端展示亲密指数

## 数据模型设计

### 1. 公司模型（Company）
```typescript
interface Company {
  _id: string;
  name: string; // 公司名称
  industry: string; // 行业（快消、美妆、日化、数码等）
  website: string; // 公司网站
  description: string; // 公司描述
  logo: string; // 公司logo
  createdAt: Date;
  updatedAt: Date;
}
```

### 2. 人员模型（Person）
```typescript
interface Person {
  _id: string;
  name: string; // 姓名
  position: string; // 职位
  phone: string; // 电话
  email: string; // 邮箱
  companyId: string; // 所属公司ID
  parentId: string; // 上级ID
  news: News[]; // 最近新闻
  createdAt: Date;
  updatedAt: Date;
}

interface News {
  title: string; // 新闻标题
  url: string; // 新闻链接
  date: Date; // 发布日期
  source: string; // 新闻来源
}
```

### 3. 关系模型（Relationship）
```typescript
interface Relationship {
  _id: string;
  person1Id: string; // 人员1 ID
  person2Id: string; // 人员2 ID
  intimacyScore: number; // 亲密指数（0-100）
  commonConnections: number; // 共同联系人数量
  interactionFrequency: number; // 互动频率
  createdAt: Date;
  updatedAt: Date;
}
```

## 核心功能设计

### 1. 公司管理
- 公司列表展示
- 公司详情查看
- 公司信息编辑
- 公司行业分类

### 2. 组织架构管理
- 组织架构树展示
- 节点展开/合并功能
- 人员信息查看
- 人员信息编辑

### 3. 人脉管理
- 人员详情展示
- 亲密指数计算
- 人脉关系网络
- 互动历史记录

### 4. 爬虫功能
- 公司信息抓取
- 人员信息抓取
- 新闻信息抓取
- 数据自动更新

### 5. 数据分析
- 亲密指数计算算法
- 人脉网络分析
- 行业趋势分析
- 数据可视化

## API设计

### 1. 公司相关API
- `GET /api/companies` - 获取公司列表
- `GET /api/companies/:id` - 获取公司详情
- `POST /api/companies` - 创建公司
- `PUT /api/companies/:id` - 更新公司信息
- `DELETE /api/companies/:id` - 删除公司

### 2. 人员相关API
- `GET /api/people` - 获取人员列表
- `GET /api/people/:id` - 获取人员详情
- `POST /api/people` - 创建人员
- `PUT /api/people/:id` - 更新人员信息
- `DELETE /api/people/:id` - 删除人员

### 3. 组织架构相关API
- `GET /api/organization/:companyId` - 获取公司组织架构
- `POST /api/organization` - 添加组织架构节点
- `PUT /api/organization/:id` - 更新组织架构节点
- `DELETE /api/organization/:id` - 删除组织架构节点

### 4. 关系相关API
- `GET /api/relationships` - 获取关系列表
- `GET /api/relationships/:personId` - 获取人员的关系网络
- `POST /api/relationships` - 创建关系
- `PUT /api/relationships/:id` - 更新关系
- `DELETE /api/relationships/:id` - 删除关系

### 5. 爬虫相关API
- `POST /api/crawler/company` - 抓取公司信息
- `POST /api/crawler/person` - 抓取人员信息
- `POST /api/crawler/news` - 抓取新闻信息
- `GET /api/crawler/status` - 获取爬虫状态

## 爬虫设计

### 1. 公司信息爬虫
- 目标网站：公司官网、行业数据库、招聘网站
- 抓取内容：公司名称、行业、网站、描述、logo

### 2. 人员信息爬虫
- 目标网站：LinkedIn、公司官网、新闻网站
- 抓取内容：姓名、职位、电话、邮箱、所属公司、上级

### 3. 新闻信息爬虫
- 目标网站：新闻门户网站、行业媒体
- 抓取内容：新闻标题、链接、日期、来源

### 4. 数据处理流程
1. 抓取原始数据
2. 数据清洗和去重
3. 数据结构化
4. 存储到数据库

## 前端界面设计

### 1. 公司列表页
- 公司名称搜索
- 行业筛选
- 公司列表展示
- 公司详情入口

### 2. 组织架构页
- 组织架构树展示
- 节点展开/合并功能
- 人员信息卡片
- 搜索和筛选功能

### 3. 人员详情页
- 基本信息展示
- 最近新闻展示
- 人脉关系网络
- 亲密指数展示

### 4. 数据分析页
- 人脉网络可视化
- 亲密指数分析
- 行业趋势分析
- 数据导出功能

## 部署方案

### 1. 前端部署
- 构建静态文件
- 部署到CDN或静态网站托管服务

### 2. 后端部署
- 部署到云服务器或容器服务
- 配置环境变量
- 设置数据库连接

### 3. 爬虫部署
- 部署到云服务器或容器服务
- 设置定时任务
- 配置代理和反爬策略

## 安全考虑

### 1. 数据安全
- 数据库加密
- API认证和授权
- 数据备份和恢复

### 2. 爬虫安全
- 遵守robots.txt
- 合理设置爬取频率
- 使用代理IP
- 避免过度请求导致目标网站崩溃

### 3. 系统安全
- 定期更新依赖
- 防止SQL注入和XSS攻击
- 监控系统日志
- 设置访问控制

## 性能优化

### 1. 前端优化
- 组件懒加载
- 数据缓存
- 减少API调用
- 优化渲染性能

### 2. 后端优化
- 数据库索引
- 缓存策略
- 异步处理
- 负载均衡

### 3. 爬虫优化
- 多线程爬取
- 数据去重
- 错误处理和重试机制
- 分布式爬取

## 未来扩展

### 1. 功能扩展
- 增加社交网络集成
- 添加智能推荐功能
- 实现移动端适配
- 支持多语言

### 2. 技术扩展
- 引入机器学习算法优化亲密指数计算
- 使用图数据库存储人脉关系
- 实现实时数据更新
- 增加数据可视化工具

### 3. 业务扩展
- 支持更多行业
- 增加竞争对手分析
- 提供市场洞察报告
- 集成CRM系统

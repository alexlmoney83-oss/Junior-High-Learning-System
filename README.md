# 初中学习系统

基于 Django + Streamlit 的智能学习平台，支持语文、数学、英语三门学科的在线学习，提供 AI 驱动的知识点总结和智能练习功能。

## 技术架构

### 后端
- **框架**: Django 4.2 + Django REST Framework
- **数据库**: MySQL 8.0
- **认证**: JWT Token
- **AI集成**: DeepSeek/OpenAI API

### 前端
- **框架**: Streamlit 1.29
- **适配**: 支持桌面、iPad、华为PAD
- **UI**: 响应式设计，触摸优化

## 功能特性

### 用户功能
- 用户注册/登录
- 个人中心管理
- AI API Key 配置

### 学习功能
- 三大学科课程浏览（语文、数学、英语）
- 按年级分类（初一、初二、初三）
- AI 生成知识点总结
- AI 生成智能练习题（25道/课）
- 学习进度跟踪

### 管理功能
- Django Admin 后台管理
- 课程内容管理
- 用户管理
- Prompt 模板管理

## 项目结构

```
初中学习系统/
├── study/                      # Django后端
│   ├── apps/                   # 应用模块
│   │   ├── users/             # 用户管理
│   │   ├── courses/           # 课程管理
│   │   ├── exercises/         # 练习题管理
│   │   └── ai_services/       # AI服务
│   ├── middle_school_system/  # 项目配置
│   ├── utils/                 # 工具模块
│   ├── manage.py              # Django管理脚本
│   ├── .env                   # 环境配置
│   └── requirements.txt       # 后端依赖
│
├── 前端/                       # Streamlit前端
│   ├── pages/                 # 页面文件
│   │   ├── 1_📚_课程中心.py
│   │   ├── 2_📖_课程详情.py
│   │   ├── 3_✍️_智能练习.py
│   │   └── 4_👤_个人中心.py
│   ├── utils/                 # 工具模块
│   │   ├── api_client.py     # API客户端
│   │   ├── auth.py           # 认证模块
│   │   └── styles.py         # 样式配置
│   ├── app.py                # 主入口
│   └── requirements.txt      # 前端依赖
│
├── 课本/                      # PDF课本资源
│   ├── 语文/
│   ├── 数学/
│   └── 英语/
│
├── requirements.txt          # 完整依赖
└── README.md                # 本文件
```

## 快速开始

### 1. 环境要求

- **Python 3.11+** （推荐 3.11，避免使用 3.13）
- **MySQL 8.0+** （必须安装）
- **pip** （Python 包管理器）

**⚠️ 重要**：本项目使用 MySQL 数据库，必须先安装 MySQL 才能运行！

### 2. 安装 MySQL 数据库

**⚠️ 必须先安装 MySQL 8.0+**

#### Windows 系统：
1. 下载 MySQL 安装包：https://dev.mysql.com/downloads/mysql/
2. 选择 "MySQL Installer for Windows"
3. 运行安装程序，选择 "Developer Default" 或 "Server only"
4. 设置 root 密码（请记住这个密码）
5. 完成安装后，MySQL 服务会自动启动

#### macOS 系统：
```bash
# 使用 Homebrew 安装
brew install mysql

# 启动 MySQL 服务
brew services start mysql

# 设置 root 密码
mysql_secure_installation
```

#### Linux 系统：
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server

# CentOS/RHEL
sudo yum install mysql-server

# 启动 MySQL 服务
sudo systemctl start mysql
sudo systemctl enable mysql

# 设置 root 密码
sudo mysql_secure_installation
```

**验证 MySQL 安装：**
```bash
mysql --version
# 应该显示：mysql  Ver 8.0.x
```

### 3. 克隆项目

```bash
git clone <项目地址>
cd 初中学习系统
```

### 4. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

**注意**：如果安装 `mysqlclient` 时出错，可能需要安装 MySQL 开发库：
- **Windows**：通常随 MySQL 一起安装
- **macOS**：`brew install mysql-client`
- **Linux**：`sudo apt install libmysqlclient-dev` (Ubuntu) 或 `sudo yum install mysql-devel` (CentOS)

### 5. 配置环境变量

**创建配置文件：**
```bash
# 复制环境变量模板
cd study
cp .env.example .env
```

**编辑 `study/.env` 文件，填写真实配置：**
```env
# 数据库配置
DB_NAME=middle_school_system
DB_USER=你的MySQL用户名
DB_PASSWORD=你的MySQL密码
DB_HOST=127.0.0.1
DB_PORT=3306

# Django密钥
SECRET_KEY=your-secret-key

# 加密密钥（运行以下命令生成）
# python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
ENCRYPTION_KEY=your-encryption-key

# 学校配置（可选，默认为空，用户注册时可自行输入）
DEFAULT_SCHOOL=
```

**生成加密密钥：**
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```
将生成的密钥复制到 `.env` 文件的 `ENCRYPTION_KEY` 字段。

### 6. 创建数据库

```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE middle_school_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 退出
EXIT;
```

### 7. 初始化数据库

```bash
cd study

# 运行数据库迁移
python manage.py migrate

# 创建超级管理员
python manage.py createsuperuser

# 初始化基础数据
python init_data.py

# 导入Prompt模板
python init_prompt_templates.py
```

### 8. 启动服务

**启动后端（终端1）：**
```bash
cd study
python manage.py runserver
```
访问：http://localhost:8000/admin/

**启动前端（终端2）：**
```bash
cd 前端
streamlit run app.py
```
访问：http://localhost:8501

## 使用指南

### 1. 配置 AI API Key

1. 获取 DeepSeek API Key：https://platform.deepseek.com/
2. 登录系统后，进入"个人中心"
3. 在"AI API Key配置"区域输入 API Key
4. 点击"保存配置"

### 2. 添加课程数据

**⚠️ 重要说明**：
- 课程数据需要**手动填写**或**从PDF提取后导入**
- Admin后台**不支持**直接上传PDF自动提取
- 需要先运行提取脚本，再导入数据库

**⚠️ 本项目的PDF提取限制**：
- 提取脚本**只能提取文字型PDF**的文本内容
- **无法提取图片中的文字**（如扫描版PDF，全是图片的PDF）
- 如果PDF是图片格式，需要：
  1. 使用OCR工具（如Adobe Acrobat、ABBYY FineReader）转换为文字PDF
  2. 或使用多模态AI模型（如Qwen3-VL-8B，olmOCR-2-7B）提取图片中的文字
  3. 或手动复制粘贴文字内容到Admin后台

**方式1：从PDF提取课程内容（推荐）**

1. 确保PDF课本文件在 `课本/` 目录下
2. 运行提取脚本：
   ```bash
   cd study
   # 提取语文课程内容
   python extract_chinese_content.py
   
   # 提取数学课程内容（需要先有数学PDF）
   python extract_math_content.py
   
   # 提取英语课程内容
   python extract_english_content.py
   ```
3. 脚本会自动：
   - 读取PDF文件
   - 提取文本内容
   - 更新数据库中的课程内容


**方式2：Admin后台手动添加**

1. 访问 http://localhost:8000/admin/
2. 进入"课程管理" > "课程"
3. 点击"添加课程"
4. **手动填写**以下信息：
   - 学科、年级、课程序号
   - 课程标题
   - 课程大纲（简介）
   - 关键词
   - **章节内容**（需要手动复制粘贴课本文字）
   - PDF来源（可选）
5. 保存

**方式3：批量导入CSV（如果有CSV数据）**
```bash
cd study
python batch_import_csv.py
```

### 3. 使用学习功能

1. 注册/登录账号
2. 选择学科（语文/数学/英语）
3. 选择年级和课程
4. 查看课程详情
5. 生成知识点总结（需要AI API Key）
6. 开始智能练习（需要AI API Key）

## API 接口

### 用户接口
- `POST /api/v1/users/register/` - 用户注册
- `POST /api/v1/users/login/` - 用户登录
- `GET /api/v1/users/profile/` - 获取用户信息

### 课程接口
- `GET /api/v1/courses/subjects/` - 获取学科列表
- `GET /api/v1/courses/courses/` - 获取课程列表
- `GET /api/v1/courses/courses/{id}/` - 获取课程详情
- `POST /api/v1/courses/courses/{id}/generate-summary/` - 生成知识点总结

### 练习题接口
- `POST /api/v1/exercises/generate/` - 生成练习题
- `POST /api/v1/exercises/submit/` - 提交答案

## 项目完成度

### ✅ 已完成功能

**后端架构**
- ✅ Django 4.2 + DRF 完整搭建
- ✅ MySQL 数据库设计和迁移
- ✅ JWT 用户认证系统
- ✅ RESTful API 接口（用户、课程、练习题）
- ✅ API Key 加密存储
- ✅ AI 服务集成（DeepSeek/OpenAI）
- ✅ Prompt 模板管理系统
- ✅ Django Admin 后台美化

**前端界面**
- ✅ Streamlit 完整 UI 框架
- ✅ 用户注册/登录功能
- ✅ 课程浏览和详情页面
- ✅ 智能练习页面
- ✅ 个人中心（含 API Key 配置）
- ✅ PAD 响应式适配
- ✅ 前后端 API 联调完成

**AI 功能**
- ✅ AI 知识点总结生成
- ✅ AI 练习题生成（25道/课）
- ✅ Prompt 模板系统（7个模板）

### ⚠️ 待完成功能

**课程数据**（由于可得到的数据有限）
- ⚠️ **课本资源不完整**
  - ✅ 英语课本：6本完整（七年级-九年级）
  - ✅ 语文课本：5本（缺八年级上册）
  - ❌ 数学课本：完全缺失
- ⚠️ **课程内容未导入**
  - 需要从 PDF 提取课程文本内容
  - 需要创建 135 门课程数据（3学科 × 3年级 × 15课）
  - 目前数据库只有基础学科信息

**功能完善**
- ⏸️ 错题本功能（待实现）

**部署优化**
- ✅ 本地开发环境（已完成，适合个人使用）
- ✅ PAD 端适配（已完成，支持 iPad、华为PAD）
- ⏸️ 生产环境配置（Nginx、HTTPS）- **仅多人使用时需要**
- ⏸️ 性能优化和缓存 - **仅大规模使用时需要**

**💡 说明**：
- 如果仅个人使用，当前的开发环境已经完全够用，无需配置 Nginx、HTTPS 等生产环境
- 直接运行 `python manage.py runserver` 和 `streamlit run app.py` 即可
- 生产环境配置仅在需要对外提供服务或多人同时使用时才需要

### 📋 可自行决定

**第一优先级**
1. 补充数学课本 PDF
2. 提取所有课本内容（运行 `extract_*_content.py`）
3. 导入完整课程数据（运行 `batch_import_csv.py`）

**第二优先级（功能增强）**
1. 添加错题本功能

**第三优先级（仅多人使用时需要）**
1. 性能优化和缓存策略
2. 生产环境部署（Nginx + HTTPS）
3. 负载均衡和高可用配置

**💡 个人使用提示**：
- 如果只是自己使用，完成第一、第二优先级的任务即可
- 当前开发环境已经足够稳定和流畅
- 无需配置复杂的生产环境

## 常见问题

### 1. 数据库连接失败

**错误信息**：`Can't connect to MySQL server` 或 `Access denied`

**解决方法**：
- **检查 MySQL 服务是否启动**
  - Windows：打开"服务"，查看 MySQL 服务状态
  - macOS/Linux：`sudo systemctl status mysql` 或 `brew services list`
- **确认 `.env` 中的数据库配置正确**
  - 用户名、密码、主机、端口是否正确
  - 尝试用命令行连接：`mysql -u root -p`
- **确认数据库已创建**
  - 登录 MySQL：`mysql -u root -p`
  - 查看数据库：`SHOW DATABASES;`
  - 如果没有，创建数据库：`CREATE DATABASE middle_school_system;`

### 2. AI 功能无法使用
- 确认已在个人中心配置 API Key
- 确认已导入 Prompt 模板（`python init_prompt_templates.py`）
- 检查 API Key 是否有效且有余额

### 3. 前端无法连接后端
- 确认 Django 后端已启动（http://localhost:8000）
- 检查防火墙设置
- 查看浏览器控制台的网络请求错误

### 4. 课程列表为空
- **正常现象**：当前数据库中没有课程数据
- **解决方法**：
  1. 在 Admin 后台手动添加课程
  2. 或等待课程数据导入功能完善
  3. 或参考 `需求文档.md` 中的课程示例手动创建

### 5. mysqlclient 安装失败

**错误信息**：`error: Microsoft Visual C++ 14.0 is required` (Windows)

**解决方法**：
- **Windows**：
  1. 安装 Visual C++ Build Tools
  2. 或使用预编译包：`pip install mysqlclient-1.4.6-cp311-cp311-win_amd64.whl`
- **macOS**：
  ```bash
  brew install mysql-client
  export PATH="/usr/local/opt/mysql-client/bin:$PATH"
  pip install mysqlclient
  ```
- **Linux**：
  ```bash
  sudo apt install libmysqlclient-dev  # Ubuntu
  sudo yum install mysql-devel         # CentOS
  pip install mysqlclient
  ```

## 开发说明

### 添加新的 API 接口
1. 在对应 app 的 `views.py` 中添加视图函数
2. 在 `serializers.py` 中创建序列化器
3. 在 `urls.py` 中添加路由

### 添加新的前端页面
1. 在 `前端/pages/` 目录创建新页面文件
2. 文件名格式：`序号_图标_页面名.py`
3. 在 `utils/api_client.py` 中添加对应的 API 调用方法

## 许可证

MIT License

## 联系方式

如有问题，请提交 Issue 或联系开发团队。

---

**版本**: 1.0.0  
**更新日期**: 2025-12-16

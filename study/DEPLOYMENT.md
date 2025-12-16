# 部署指南

## 快速开始

### 1. 生成加密密钥

在项目根目录下运行：

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

复制输出的密钥，粘贴到`.env`文件的`ENCRYPTION_KEY`字段中。

### 2. 安装依赖

```bash
# 确保虚拟环境已激活
pip install -r requirements.txt
```

### 3. 创建数据库

```bash
# 方式1：使用MySQL命令行
mysql -h 192.168.184.130 -P 3307 -u alex -p -e "CREATE DATABASE IF NOT EXISTS middle_school_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 方式2：使用Python脚本
python -c "
import MySQLdb
conn = MySQLdb.connect(host='192.168.184.130', port=3307, user='alex', password='123456')
cursor = conn.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS middle_school_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
print('✅ 数据库创建成功！')
conn.close()
"
```

### 4. 运行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 创建超级用户

```bash
python manage.py createsuperuser
```

按提示输入：
- 用户名
- 邮箱
- 密码

### 6. 初始化基础数据（可选）

创建三个学科：

```bash
python manage.py shell
```

然后执行：

```python
from apps.courses.models import Subject

# 创建三个学科
Subject.objects.create(name='语文', code='chinese', icon='📚', description='初中语文课程', order=1)
Subject.objects.create(name='数学', code='math', icon='🔢', description='初中数学课程', order=2)
Subject.objects.create(name='英语', code='english', icon='🔤', description='初中英语课程', order=3)

print("✅ 学科数据创建成功！")
exit()
```

### 7. 启动开发服务器

```bash
python manage.py runserver 0.0.0.0:8000
```

访问：
- Admin后台：http://localhost:8000/admin/
- API文档：http://localhost:8000/api/v1/

## API测试

### 用户注册

```bash
curl -X POST http://localhost:8000/api/v1/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student001",
    "email": "student001@example.com",
    "password": "Abc123456",
    "password_confirm": "Abc123456",
    "grade": "grade1"
  }'
```

### 用户登录

```bash
curl -X POST http://localhost:8000/api/v1/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student001",
    "password": "Abc123456"
  }'
```

### 获取学科列表

```bash
curl -X GET http://localhost:8000/api/v1/courses/subjects/
```

## 常见问题

### Q: 数据库连接失败

**A:** 检查以下几点：
1. MySQL服务是否启动
2. 数据库连接信息是否正确（.env文件）
3. 防火墙是否允许3307端口
4. 数据库用户权限是否正确

### Q: 导入错误

**A:** 确保所有依赖包都已安装：
```bash
pip install -r requirements.txt
```

### Q: 加密密钥错误

**A:** 重新生成加密密钥并更新.env文件：
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### Q: Admin后台无法访问

**A:** 
1. 确保已创建超级用户：`python manage.py createsuperuser`
2. 确保DEBUG=True（开发环境）
3. 检查URL配置是否正确

## 生产环境部署

### 使用Gunicorn

```bash
# 安装Gunicorn
pip install gunicorn

# 收集静态文件
python manage.py collectstatic --noinput

# 启动Gunicorn
gunicorn middle_school_system.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 60 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log
```

### Nginx配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    client_max_body_size 20M;
    
    location /static/ {
        alias /path/to/study/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/study/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 数据备份

### 备份数据库

```bash
mysqldump -h 192.168.184.130 -P 3307 -u alex -p middle_school_system > backup_$(date +%Y%m%d).sql
```

### 恢复数据库

```bash
mysql -h 192.168.184.130 -P 3307 -u alex -p middle_school_system < backup_20251002.sql
```


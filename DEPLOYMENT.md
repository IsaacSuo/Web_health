# 部署指南

## 本地开发部署

### 快速启动
```bash
./start.sh
```

### 手动启动
```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 数据库迁移
python manage.py migrate

# 4. 初始化数据
python manage.py init_data

# 5. 启动服务
python manage.py runserver
```

## 生产环境部署

### 环境准备
- Python 3.8+
- PostgreSQL 或 MySQL（推荐）
- Nginx
- Gunicorn

### 1. 服务器配置

```bash
# 安装系统依赖
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib

# 创建数据库
sudo -u postgres createdb tinnitus_health
sudo -u postgres createuser --interactive
```

### 2. 项目部署

```bash
# 克隆项目
git clone <repository-url>
cd web_ver_0.1

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件设置数据库连接等
```

### 3. Django 配置

在 `settings.py` 中添加生产环境配置：

```python
import os
from pathlib import Path

# 生产环境设置
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# 数据库配置
if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
    }

# 静态文件配置
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 安全设置
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### 4. 收集静态文件

```bash
python manage.py collectstatic --noinput
```

### 5. Gunicorn 配置

创建 `gunicorn.conf.py`:

```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
```

### 6. Nginx 配置

创建 `/etc/nginx/sites-available/tinnitus_health`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    location /static/ {
        alias /path/to/project/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/project/media/;
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

### 7. 系统服务配置

创建 `/etc/systemd/system/tinnitus_health.service`:

```ini
[Unit]
Description=Tinnitus Health Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/project
Environment="PATH=/path/to/project/venv/bin"
ExecStart=/path/to/project/venv/bin/gunicorn --config gunicorn.conf.py tinnitus_health.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

### 8. 启动服务

```bash
# 启用并启动服务
sudo systemctl enable tinnitus_health
sudo systemctl start tinnitus_health

# 启用并启动 Nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

## Docker 部署

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "tinnitus_health.wsgi:application"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./media:/app/media
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://user:password@db:5432/tinnitus_health
    depends_on:
      - db

  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=tinnitus_health
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password

volumes:
  postgres_data:
```

## 维护命令

```bash
# 数据库备份
python manage.py dumpdata > backup.json

# 数据库恢复
python manage.py loaddata backup.json

# 清理会话
python manage.py clearsessions

# 收集静态文件
python manage.py collectstatic

# 检查部署配置
python manage.py check --deploy
```

## 监控和日志

### 日志配置

在 `settings.py` 中添加：

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/tinnitus_health.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### 性能监控

推荐使用：
- Sentry (错误监控)
- New Relic (性能监控)
- Prometheus + Grafana (系统监控)

## 安全建议

1. 定期更新依赖包
2. 使用 HTTPS
3. 设置防火墙规则
4. 定期备份数据库
5. 监控异常访问
6. 使用强密码策略
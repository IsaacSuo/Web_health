#!/bin/bash

echo "=== 子午养生 · 静耳时光 Django 项目启动脚本 ==="

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装依赖包..."
pip install -r requirements.txt

# 数据库迁移
echo "执行数据库迁移..."
python manage.py migrate

# 初始化数据
echo "初始化基础数据..."
python manage.py init_data

# 创建超级用户（如果不存在）
echo "检查超级用户..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('超级用户已创建: admin/admin123')
else:
    print('超级用户已存在: admin/admin123')
"

echo ""
echo "=== 项目启动完成 ==="
echo "管理后台: http://127.0.0.1:8000/admin/"
echo "用户名: admin"
echo "密码: admin123"
echo ""
echo "启动开发服务器..."
python manage.py runserver
# 子午养生 · 静耳时光

基于Django的耳鸣养生网站，结合传统中医理论与现代数据挖掘研究成果，为用户提供十二时辰养生指南和耳鸣穴位按摩推荐。

### 技术栈
- **后端**: Django 5.2.4
- **前端**: HTML5, CSS3, JavaScript, Bootstrap 5
- **数据库**: SQLite (开发环境)
- **图片处理**: Pillow

## 快速开始

### 环境要求
- Python 3.8+
- pip

## 安装步骤

1. **创建虚拟环境**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **数据库迁移**
```bash
python manage.py migrate
```

4. **初始化基础数据及收集静态数据**
```bash
python manage.py init_data
python manage.py collectstatic --noinput --clear
```

5. **启动开发服务器**
```bash
python manage.py runserver
```

6. **访问网站**
打开浏览器访问 `http://127.0.0.1:8000`

7. **设置staticfiles权限**
```bash
sudo chown -R www-data:www-data ./staticfiles/
sudo chmod -R 644 ./staticfiles/css/style.css
sudo chmod -R 755 ./staticfiles/css/
```

## 管理后台
访问 `http://127.0.0.1:8000/admin/` 进入管理后台

默认管理员账户：
- 用户名: admin
- 密码: admin123
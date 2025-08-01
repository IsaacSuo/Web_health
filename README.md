# 子午养生 · 静耳时光

基于Django的耳鸣养生网站，结合传统中医理论与现代数据挖掘研究成果，为用户提供十二时辰养生指南和耳鸣穴位按摩推荐。

## 项目特色

### 🎯 目标用户
- 对养生知识感兴趣的大众用户
- 耳鸣患者
- 中医学生和从业者

### ✨ 主要功能
- **十二时辰圆形布局**：直观展示十二时辰对应的脏腑经络
- **时辰提醒系统**：个性化养生提醒，根据时间推送相应建议
- **耳鸣日记功能**：记录症状与按摩效果，帮助分析规律
- **穴位按摩指导**：专业的穴位按摩方法和效果说明
- **用户资料管理**：个人健康信息记录和管理

### 🔧 技术栈
- **后端**: Django 5.2.4
- **前端**: HTML5, CSS3, JavaScript, Bootstrap 5
- **数据库**: SQLite (开发环境)
- **图片处理**: Pillow

## 快速开始

### 环境要求
- Python 3.8+
- pip

### 一键启动（推荐）

```bash
# 克隆项目
git clone <repository-url>
cd web_ver_0.1

# 一键启动（Linux/Mac）
./start.sh

# Windows用户请手动执行以下步骤
```

## 手动安装步骤

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

4. **初始化基础数据**
```bash
python manage.py init_data
```

5. **启动开发服务器**
```bash
python manage.py runserver
```

6. **访问网站**
打开浏览器访问 `http://127.0.0.1:8000`



## 管理后台
访问 `http://127.0.0.1:8000/admin/` 进入管理后台

默认管理员账户：
- 用户名: admin
- 密码: admin123
### alembic 初始化
**先安装 alembic**

`pip install alembic`

**然后生成初始化文件, 在项目外一层使用以下初始化命令**

`alembic init alembic`

**初始化后，生成一个alembic文件目录**

### 配置alembic/env.py文件
```
# 第21行
from app.db.config import Base  
import app.db.models
target_metadata = Base.metadata
```

### 配置alembic.ini文件
```
# 第58行
sqlalchemy.url = postgresql://mark:mark123@192.168.1.107:5432/fastapi-test
```
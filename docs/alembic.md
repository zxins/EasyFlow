## Alembic常用命令
```
// 初始化
alembic init alembic

// 创建迁移文件
alembic revision --autogenerate -m "【备注】"

// 将迁移文件映射到数据库
alembic upgrade head
```
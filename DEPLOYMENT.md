# 闲鱼超级管家 - Docker 容器部署

## 📋 部署信息

### 部署位置
- **工作目录**: ~/workspaces/xianyu-super-butler
- **容器名称**: xianyu-super-butler
- **镜像**: xianyu-super-butler:latest

### 数据目录
- **应用数据**: ./data/
- **系统日志**: ./logs/
- **备份文件**: ./backups/

## 🌐 访问信息

### 应用地址
- **Web 界面**: http://localhost:8080
- **API 服务**: http://localhost:8080/api

### 初始登录凭证
- **用户名**: admin
- **密码**: butler123456 (请在首次登录后修改)

## 🚀 管理命令

### 查看容器状态
```bash
cd ~/workspaces/xianyu-super-butler
docker-compose ps
```

### 查看应用日志
```bash
# 实时日志
docker-compose logs -f xianyu-app

# 最后 50 行
docker-compose logs --tail 50 xianyu-app
```

### 重启应用
```bash
docker-compose restart xianyu-app
```

### 完全停止
```bash
docker-compose down
```

### 重新启动
```bash
docker-compose up -d
```

## 📊 系统资源

- **内存限制**: 2GB
- **内存保留**: 512MB
- **CPU 限制**: 2.0 核
- **CPU 保留**: 0.5 核

## 🔧 配置管理

环境变量在 `.env` 文件中配置，主要参数：

```bash
ADMIN_USERNAME=admin                    # 管理员用户名
ADMIN_PASSWORD=butler123456             # 管理员密码
WEB_PORT=8080                          # Web 服务端口
TZ=Asia/Shanghai                       # 时区
LOG_LEVEL=INFO                         # 日志级别
AUTO_REPLY_ENABLED=true                # 自动回复开关
AUTO_DELIVERY_ENABLED=true             # 自动发货开关
AI_REPLY_ENABLED=false                 # AI 回复开关
```

修改后需要重启容器：
```bash
docker-compose restart xianyu-app
```

## ✅ 系统状态检查

### 健康检查
```bash
curl http://localhost:8080/health
```

示例响应：
```json
{
  "status": "healthy",
  "timestamp": 1789823288.148,
  "services": {
    "cookie_manager": "ok",
    "database": "ok"
  },
  "system": {
    "cpu_percent": 2.4,
    "memory_percent": 51.7,
    "memory_available": 8027623424
  }
}
```

## 📦 功能模块

- ✅ 多账号管理 - 统一管理多个闲鱼账号
- ✅ 自动发货 - 支持卡券、虚拟商品自动发货
- ✅ 自动回复 - 关键词回复 + AI 智能回复
- ✅ 订单管理 - 历史订单导入、批量操作
- ✅ 商品自动化 - 商品同步、定时擦亮、自动上下架
- ✅ 经营看板 - 成交额、订单、库存一屏掌握
- ✅ 通知系统 - 支持多渠道通知

## 🐛 常见问题

### 1. 无法访问应用
检查容器是否正常运行：
```bash
docker-compose ps
```

如果容器不健康，查看日志：
```bash
docker-compose logs xianyu-app
```

### 2. 忘记管理员密码
在后台设置页面可以修改密码（需要先登录）

### 3. 数据持久化
所有数据存储在 `./data/` 目录中：
- `xianyu_data.db` - 主数据库
- `xianyu_data_backup_*.db` - 自动备份

### 4. 查看数据库
```bash
docker exec xianyu-super-butler sqlite3 /app/data/xianyu_data.db
```

## 📝 备份与恢复

### 自动备份
应用每小时自动备份数据库到 `./backups/` 目录

### 手动备份
```bash
cp data/xianyu_data.db backups/xianyu_data_backup_$(date +%Y%m%d_%H%M%S).db
```

### 恢复备份
```bash
cp backups/xianyu_data_backup_XXXXXX.db data/xianyu_data.db
docker-compose restart xianyu-app
```

## 🔐 安全建议

1. 修改默认管理员密码
2. 不要暴露端口到公网（需要时使用反向代理）
3. 定期备份数据
4. 检查日志中的异常信息
5. 使用 https（通过 Nginx 反向代理）

## 📞 更新和维护

### 拉取最新代码
```bash
cd ~/workspaces/xianyu-super-butler
git pull origin main
```

### 重新构建镜像
```bash
docker build --network=host -f Dockerfile -t xianyu-super-butler:latest .
```

### 应用最新版本
```bash
docker-compose restart xianyu-app
```

---

**部署时间**: 2026-09-19 21:08:00
**应用版本**: 3.1.0

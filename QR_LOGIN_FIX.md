# 扫码登录二维码刷新问题修复

## 问题描述
扫码登录二维码无法刷新，尝试生成新的二维码时会失败，出现连接超时错误。

## 问题原因分析

### 根本原因
1. **代理未配置**: 容器内生成二维码需要访问外部 API（h5api.m.goofish.com），但代理被禁用
2. **网络连接问题**: 容器内无法直接访问外部服务，需要通过 Clash 代理
3. **超时时间不足**: 30 秒的超时时间对于代理请求不够
4. **Docker 网络隔离**: 容器无法直接访问主机的代理服务

### 错误日志
```
ERROR | utils.qr_login:_get_mh5tk:155 - 获取m_h5_tk时连接超时
ERROR | utils.qr_login:generate_qr_code:295 - 连接超时
WARNING | 扫码登录二维码生成失败: 连接超时，请检查网络或尝试使用代理
```

## 修复方案

### 1. 启用代理支持 ✅
**文件**: `utils/qr_login.py`

```python
# 修改前: self.proxy = None
# 修改后: self.proxy = "http://host.docker.internal:7897"
```

自动检测运行环境（Docker 或本地），动态配置合适的代理地址。

### 2. 增加超时时间 ✅
**文件**: `utils/qr_login.py`

```python
# 修改前: httpx.Timeout(connect=30.0, read=60.0, write=30.0, pool=60.0)
# 修改后: httpx.Timeout(connect=60.0, read=120.0, write=60.0, pool=120.0)
```

增加了一倍的超时时间，适应代理和网络延迟。

### 3. 添加重试机制 ✅
**文件**: `utils/qr_login.py`

```python
# 获取 m_h5_tk 时最多重试 3 次
# 每次失败后等待 3 秒再重试
# 提高成功率，应对网络波动
```

### 4. 改进错误处理 ✅
**文件**: `utils/qr_login.py`

```python
# 更详细的错误日志
# 提示可能的原因
# 便于调试和诊断
```

### 5. Docker 网络配置 ✅
**文件**: `docker-compose.yml`

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

配置 Docker 容器能够访问主机的网络服务（代理）。

## 验证修复

### 方式 1: 通过 Web 界面测试
1. 访问 http://127.0.0.1:8080/
2. 点击「扫码登录」
3. 点击「刷新二维码」按钮
4. 验证二维码是否正常生成和刷新

### 方式 2: 查看日志验证
```bash
cd ~/workspaces/xianyu-super-butler
docker-compose logs xianyu-app -f | grep -i "qr\|二维码"
```

预期日志输出：
```
INFO | 检测到 Docker 环境，配置代理访问主机资源
INFO | QR登录管理器初始化: 代理=http://host.docker.internal:7897
INFO | 获取m_h5_tk成功
INFO | 获取登录参数成功
INFO | 二维码生成成功
```

### 方式 3: 直接 API 测试
```bash
# 测试生成二维码的 API
curl -X POST http://127.0.0.1:8080/qr-login/generate \
  -H "Authorization: Bearer YOUR_TOKEN"

# 应该返回成功的二维码数据
# {"success": true, "session_id": "...", "qr_code_url": "data:image/png;base64,..."}
```

## 技术细节

### 代理地址选择
- **Docker 环境**: `http://host.docker.internal:7897`
  - 使用 Docker 的特殊域名访问主机
  - 需要在 docker-compose.yml 中配置 `extra_hosts`
  
- **本地环境**: `http://127.0.0.1:7897`
  - 直接使用本地回环地址
  - 不需要额外配置

### 重试机制
- 最多重试 3 次
- 每次重试间隔 3 秒
- 捕获所有连接相关的异常

### 超时配置
| 参数 | 修改前 | 修改后 | 说明 |
|------|--------|--------|------|
| connect | 30s | 60s | 连接建立超时 |
| read | 60s | 120s | 读取响应超时 |
| write | 30s | 60s | 写入请求超时 |
| pool | 60s | 120s | 连接池超时 |

## 修改文件清单

✅ `utils/qr_login.py`
- 添加 `_detect_proxy()` 方法
- 修改 `__init__()` 启用代理
- 增加超时时间
- 添加重试机制到 `generate_qr_code()`
- 改进 `_get_mh5tk()` 错误处理

✅ `docker-compose.yml`
- 添加 `extra_hosts` 配置

## 故障排除

### 问题: 二维码仍然无法生成
**检查清单:**
```bash
# 1. 确认 Clash 正在运行且监听 7897 端口
netstat -tlnp | grep 7897

# 2. 确认容器内可以访问主机
docker exec xianyu-super-butler curl -v http://host.docker.internal:7897

# 3. 查看详细日志
docker-compose logs xianyu-app | grep -A 5 "QR登录\|二维码\|Error"

# 4. 检查代理配置
docker exec xianyu-super-butler env | grep PROXY
```

### 问题: host.docker.internal 无法解析
**解决方案:**
1. 检查 docker-compose.yml 中的 `extra_hosts` 配置
2. 重启容器: `docker-compose restart xianyu-app`
3. 如果仍无法解析，使用网关 IP: `172.17.0.1` 或 `10.0.2.2`

### 问题: 代理拒绝连接
**检查方项:**
1. Clash 是否在运行
2. 防火墙是否允许 7897 端口
3. Clash 配置中 `allow-lan` 是否启用
4. 检查 Clash 的代理规则是否拦截了请求

## 性能影响

- **首次生成**: ~5-10 秒（带代理和超时）
- **重新刷新**: ~3-5 秒
- **失败重试**: 每次重试增加 3 秒等待时间

## 相关配置文件

```bash
# Clash 配置
~/.local/share/io.github.clash-verge-rev.clash-verge-rev/clash-verge.yaml
混合端口: 7897

# 应用配置
docker-compose.yml
global_config.yml
.env
```

## 回滚方案

如需回滚到原始版本：

```bash
cd ~/workspaces/xianyu-super-butler
git checkout utils/qr_login.py docker-compose.yml
docker-compose down
docker build --network=host -f Dockerfile -t xianyu-super-butler:latest .
docker-compose up -d
```

---

**修复时间**: 2026-09-19 21:23
**修复版本**: v1.0
**测试状态**: ✅ 已验证

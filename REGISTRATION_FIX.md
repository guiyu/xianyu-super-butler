# 注册和邮箱验证问题修复

## 问题描述
用户尝试注册时，提示"验证码发送失败"。

## 问题原因
应用中的 SMTP 邮件服务未配置，无法发送验证码邮件。

## 解决方案

### ✅ 方案 A：关闭邮箱验证（已应用）

通过设置 `.env` 文件中的环境变量来关闭邮箱验证要求：

```bash
EMAIL_VERIFICATION_ENABLED=false
```

**效果**: 用户可以直接注册而无需邮箱验证

**步骤**: 
1. 修改 `.env` 文件
2. 重启应用: `docker-compose restart xianyu-app`
3. 现在可以直接注册了

---

## 📋 方案 B：配置 SMTP 邮件服务（可选）

如果你需要启用邮箱验证，需要配置 SMTP 服务：

### 1. 在 `.env` 中添加 SMTP 配置：

```bash
# 邮件服务配置
SMTP_SERVER=smtp.gmail.com          # SMTP 服务器地址
SMTP_PORT=587                       # SMTP 端口
SMTP_USER=your-email@gmail.com      # 邮箱账号
SMTP_PASSWORD=your-app-password     # 邮箱应用密码
SMTP_FROM=noreply@example.com       # 发件人邮箱
SMTP_USE_TLS=true                   # 使用 TLS 加密
SMTP_USE_SSL=false                  # 使用 SSL 加密

# 重新启用邮箱验证
EMAIL_VERIFICATION_ENABLED=true
```

### 2. 常见邮件服务商配置

#### Gmail
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USE_SSL=false
# 需要使用 "应用密码" 而非账户密码
```

#### QQ 邮箱
```
SMTP_SERVER=smtp.qq.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USE_SSL=false
# 需要开启 SMTP 服务并获取授权码
```

#### 阿里云邮件
```
SMTP_SERVER=smtp.aliyun.com
SMTP_PORT=25
SMTP_USE_TLS=false
SMTP_USE_SSL=false
```

### 3. 应用配置

修改 `.env` 文件后，重启应用：

```bash
cd ~/workspaces/xianyu-super-butler
docker-compose restart xianyu-app
```

### 4. 验证配置

在应用的「系统设置 → 邮件服务」中测试邮件发送。

---

## 🚀 当前状态

- **邮箱验证**: ❌ 关闭
- **注册状态**: ✅ 可直接注册（无需邮箱验证）
- **验证码邮件**: ❌ 不发送

## ⚙️ 环境变量参考

完整的邮件相关环境变量：

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| EMAIL_VERIFICATION_ENABLED | 是否启用邮箱验证 | true |
| SMTP_SERVER | SMTP 服务器地址 | 未配置 |
| SMTP_PORT | SMTP 端口 | 587 |
| SMTP_USER | SMTP 用户名 | 未配置 |
| SMTP_PASSWORD | SMTP 密码 | 未配置 |
| SMTP_FROM | 发件人邮箱 | noreply@example.com |
| SMTP_USE_TLS | 使用 TLS 加密 | true |
| SMTP_USE_SSL | 使用 SSL 加密 | false |

## 🔧 故障排除

### 邮件仍然无法发送
1. 检查 SMTP 凭证是否正确
2. 检查防火墙是否阻止 SMTP 端口
3. 查看应用日志: `docker-compose logs xianyu-app`
4. 检查邮件服务商是否启用了第三方应用访问

### 收不到验证码邮件
1. 检查垃圾邮件文件夹
2. 确认邮箱地址输入正确
3. 查看邮件服务商的日志/活动记录

---

**修复时间**: 2026-09-19 21:20
**修复方式**: 关闭邮箱验证要求，允许直接注册

# Clash 本地流量配置说明

## 问题描述
xianyu-super-butler 应用运行在本地 Docker 容器中（127.0.0.1:8080），默认情况下可能会通过 Clash VPN 代理，导致不必要的延迟或连接问题。

## 解决方案
在 Clash 配置文件中添加本地流量绕过规则，使本地应用的流量直接走本地网络，而不经过 VPN 代理。

## 配置详情

### 已添加的规则

以下规则已添加到 Clash 配置，这些流量将使用 `DIRECT` 模式（直连，不走代理）：

#### IP 地址范围
```
127.0.0.0/8       - 本地回环地址（127.0.0.1 等）
10.0.0.0/8        - 私有网络 Class A
172.16.0.0/12     - 私有网络 Class B
192.168.0.0/16    - 私有网络 Class C
169.254.0.0/16    - 链接本地地址
198.18.0.0/16     - 测试网络/Clash Fake-IP
```

#### Docker 网络
```
172.17.0.0/16     - Docker bridge network
172.18.0.0/16     - Docker compose networks
172.19.0.0/16     - Docker networks
```

#### 域名后缀
```
localhost     - 本地主机
.local        - mDNS 本地域名
.lan          - 局域网域名
.home         - 家庭网络域名
.home.arpa    - RFC 6762 本地域名
```

### 影响范围

现在以下访问方式会走本地直连（不走 VPN）：

✅ **本地 Docker 应用**
```
http://127.0.0.1:8080          - xianyu-super-butler 主页
http://localhost:8080          - xianyu-super-butler 主页
```

✅ **局域网设备**
```
http://192.168.x.x:8080        - 局域网 IP 访问
http://10.x.x.x:8080          - 私有网络 IP 访问
```

✅ **本地域名**
```
http://hostname.local:8080     - 本地 mDNS 域名
```

✅ **容器间通信**
```
Docker 容器之间的通信会直接走本地网络
```

## 验证配置

### 1. 查看当前规则
```bash
# 查看 Clash 配置文件
cat ~/.local/share/io.github.clash-verge-rev.clash-verge-rev/clash-verge.yaml | grep -A 20 "^rules:"
```

### 2. 重启 Clash Verge
重启 Clash 应用使配置生效（通过 Clash Verge GUI 或命令行）。

### 3. 测试连接
```bash
# 访问本地应用
curl http://127.0.0.1:8080/health

# 应该返回健康检查响应
# {"status":"healthy",...}
```

## 技术细节

### Clash 规则匹配顺序
- Clash 规则按优先级从上到下匹配
- 本地规则已添加到规则列表最前面，确保优先匹配
- 一旦匹配本地规则，流量将使用 `DIRECT` 模式（直连）
- 其他流量继续使用原有的代理规则

### DIRECT 模式
- `DIRECT` 表示直接连接（不走任何代理）
- 用于本地网络、私有 IP 和本地域名
- 避免不必要的代理开销，降低延迟

## 故障排除

### 问题 1: 配置修改后没有生效
**解决方案:**
1. 完全关闭 Clash Verge 应用
2. 等待 5-10 秒
3. 重新打开应用
4. 检查是否生效

### 问题 2: 无法访问本地应用
**检查清单:**
```bash
# 1. 检查容器是否正常运行
docker-compose ps

# 2. 检查应用是否监听 8080
netstat -tlnp | grep 8080

# 3. 直接访问，不走代理
curl --noproxy "*" http://127.0.0.1:8080/health

# 4. 检查防火墙
sudo ufw status

# 5. 查看 Clash 日志
tail -f ~/.local/share/io.github.clash-verge-rev.clash-verge-rev/logs/*
```

### 问题 3: 某些域名仍在走代理
**可能原因:**
- 域名模式与规则不匹配
- 需要添加更多的域名后缀规则

**解决方案:**
编辑 Clash 配置文件，添加特定的域名规则：
```yaml
rules:
  - DOMAIN,your-domain.local,DIRECT
  - DOMAIN-SUFFIX,.your-local-domain,DIRECT
```

## 配置文件备份

如需恢复原始配置：
```bash
cp ~/.local/share/io.github.clash-verge-rev.clash-verge-rev/clash-verge.yaml.backup \
   ~/.local/share/io.github.clash-verge-rev.clash-verge-rev/clash-verge.yaml
```

## 相关文档

- Clash 官方文档: https://github.com/Dreamacro/clash
- Clash.Meta: https://github.com/MetaCubeX/Clash.Meta
- Clash Verge: https://github.com/clash-verge-rev/clash-verge-rev

---

**配置生效时间**: 2026-09-19 21:25
**配置方式**: 添加本地流量绕过规则到 rules 最前面

# 🚀 AI Prompt Studio 更新服务

## 📋 概述

这是 AI Prompt Studio 的免费自动更新服务，使用 GitHub + Vercel 实现零成本部署。

## 🌐 服务地址

- **API 端点**: `https://your-app.vercel.app/api/check`
- **健康检查**: `https://your-app.vercel.app/health`
- **GitHub 仓库**: `https://github.com/bdrwss/aipromptstudio-updates`

## 📡 API 接口

### 检查更新

```http
GET /api/check?current_version=1.0.0&platform=windows&arch=x64
```

**请求参数**:
- `current_version` (必需): 当前版本号
- `platform` (可选): 平台，默认 `windows`
- `arch` (可选): 架构，默认 `x64`
- `user_id` (可选): 用户ID，用于统计

**响应示例**:

有更新时:
```json
{
  "has_update": true,
  "version": "1.1.0",
  "download_url": "https://github.com/YOUR_USERNAME/aipromptstudio-updates/releases/download/v1.1.0/AIPromptStudio-1.1.0-Setup.exe",
  "file_size": 52428800,
  "checksum": "sha256:abc123...",
  "release_notes": "修复若干问题，新增功能",
  "force_update": true,
  "min_version": "1.0.0",
  "release_date": "2025-01-16T10:00:00Z"
}
```

无更新时:
```json
{
  "has_update": false,
  "current_version": "1.1.0",
  "latest_version": "1.1.0",
  "message": "当前已是最新版本",
  "check_time": "2025-01-16T10:00:00Z"
}
```

### 健康检查

```http
GET /health
```

**响应示例**:
```json
{
  "status": "healthy",
  "service": "AI Prompt Studio Update API",
  "version": "1.0.0",
  "timestamp": "2025-01-16T10:00:00Z",
  "uptime": 3600,
  "environment": "production",
  "region": "iad1"
}
```

## 📦 发布新版本

### 1. 准备安装包

```bash
# 确保安装包文件名格式正确
AIPromptStudio-1.1.0-Setup.exe
```

### 2. 创建 GitHub Release

```bash
# 使用 GitHub CLI
gh release create v1.1.0 \
  --title "AI Prompt Studio v1.1.0" \
  --notes "修复若干问题，新增强制更新功能" \
  AIPromptStudio-1.1.0-Setup.exe

# 或通过 Web 界面
# 访问: https://github.com/bdrwss/aipromptstudio-updates/releases/new
```

### 3. 更新版本信息

编辑 `api/check.js` 文件中的版本配置:

```javascript
const LATEST_VERSION = {
  version: "1.1.0",  // 新版本号
  download_url: "https://github.com/bdrwss/aipromptstudio-updates/releases/download/v1.1.0/AIPromptStudio-1.1.0-Setup.exe",
  file_size: 52428800,  // 实际文件大小
  checksum: "sha256:新的校验和",  // 计算新的校验和
  release_notes: "版本更新说明",
  force_update: true,
  min_version: "1.0.0"
};
```

### 4. 计算文件校验和

```bash
# Windows (PowerShell)
Get-FileHash -Algorithm SHA256 AIPromptStudio-1.1.0-Setup.exe

# Linux/macOS
sha256sum AIPromptStudio-1.1.0-Setup.exe
```

### 5. 提交更新

```bash
git add api/check.js
git commit -m "更新到版本 1.1.0"
git push origin main
```

## 🔧 本地开发

### 安装依赖

```bash
npm install -g vercel
```

### 本地运行

```bash
# 启动开发服务器
vercel dev

# 访问本地API
curl "http://localhost:3000/api/check?current_version=1.0.0"
```

### 部署到 Vercel

```bash
# 首次部署
vercel

# 生产环境部署
vercel --prod
```

## 📊 使用统计

### 免费限制

- **函数执行时间**: 100GB-小时/月
- **函数调用次数**: 无限制
- **带宽**: 100GB/月
- **文件大小**: 单个文件最大 2GB

### 性能指标

- **响应时间**: < 200ms
- **可用性**: 99.99%
- **全球CDN**: 自动启用

## 🛠️ 故障排除

### 常见问题

1. **API 返回 404**
   - 检查 `vercel.json` 配置
   - 确认文件路径正确

2. **CORS 错误**
   - 检查响应头设置
   - 确认客户端请求格式

3. **版本比较错误**
   - 检查版本号格式 (x.y.z)
   - 确认版本比较逻辑

### 调试方法

```bash
# 查看部署日志
vercel logs

# 查看函数日志
vercel logs --follow
```

## 📞 支持

如有问题，请：
1. 检查 [GitHub Issues](https://github.com/bdrwss/aipromptstudio-updates/issues)
2. 查看 [Vercel 文档](https://vercel.com/docs)
3. 提交新的 Issue

---

**部署完成后，记得更新客户端配置中的服务器地址！**

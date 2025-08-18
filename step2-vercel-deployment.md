# 步骤2：配置Vercel部署

## 🎯 目标
在Vercel上部署Serverless API服务处理更新检查请求

## 📋 操作步骤

### 1. 注册Vercel账户

1. **访问Vercel**: https://vercel.com
2. **点击 "Sign Up"**
3. **选择 "Continue with GitHub"** (推荐)
4. **授权Vercel访问GitHub**

### 2. 导入GitHub项目

1. **登录Vercel后，点击 "New Project"**
2. **选择 "Import Git Repository"**
3. **找到 `aipromptstudio-updates` 仓库**
4. **点击 "Import"**

### 3. 配置项目设置

在项目配置页面：

1. **Project Name**: `aipromptstudio-updates`
2. **Framework Preset**: `Other`
3. **Root Directory**: `./` (默认)
4. **Build and Output Settings**: 
   - Build Command: 留空
   - Output Directory: 留空
   - Install Command: 留空

### 4. 环境变量配置（可选）

如果需要配置环境变量：

1. **点击 "Environment Variables"**
2. **添加变量**:
   ```
   NODE_ENV = production
   API_VERSION = 1.0.0
   ```

### 5. 部署项目

1. **点击 "Deploy"**
2. **等待部署完成** (通常1-2分钟)
3. **获取部署URL**: `https://your-app.vercel.app`

## 🧪 测试部署

### 1. 测试健康检查

```bash
# 访问健康检查端点
curl https://your-app.vercel.app/health
```

预期响应：
```json
{
  "status": "healthy",
  "service": "AI Prompt Studio Update API",
  "version": "1.0.0",
  "timestamp": "2025-01-16T10:00:00Z"
}
```

### 2. 测试更新检查API

```bash
# 测试更新检查
curl "https://your-app.vercel.app/api/check?current_version=1.0.0"
```

预期响应：
```json
{
  "has_update": true,
  "version": "1.1.0",
  "download_url": "https://github.com/YOUR_USERNAME/aipromptstudio-updates/releases/download/v1.1.0/AIPromptStudio-1.1.0-Setup.exe",
  "force_update": true
}
```

## 🔧 自定义域名（可选）

### 1. 购买域名

推荐域名注册商：
- **Namecheap**: 便宜，界面友好
- **Cloudflare**: 价格透明，管理方便
- **阿里云**: 国内用户方便

### 2. 在Vercel添加域名

1. **进入项目设置**
2. **点击 "Domains"**
3. **添加域名**: `update.yourdomain.com`
4. **配置DNS记录**:
   ```
   Type: CNAME
   Name: update
   Value: cname.vercel-dns.com
   ```

### 3. 验证域名

1. **等待DNS传播** (5-30分钟)
2. **Vercel自动配置SSL证书**
3. **测试访问**: `https://update.yourdomain.com/health`

## 📊 监控和分析

### 1. Vercel Analytics

1. **进入项目设置**
2. **点击 "Analytics"**
3. **启用 "Web Analytics"**
4. **查看访问统计**

### 2. 函数日志

```bash
# 安装Vercel CLI
npm i -g vercel

# 登录
vercel login

# 查看实时日志
vercel logs --follow
```

### 3. 性能监控

在Vercel控制台查看：
- **函数执行时间**
- **错误率**
- **调用次数**
- **带宽使用**

## 🔄 自动部署

### 1. 配置自动部署

Vercel默认启用自动部署：
- **推送到main分支** → 自动部署到生产环境
- **推送到其他分支** → 自动部署到预览环境

### 2. 部署钩子

获取部署钩子URL：
1. **项目设置** → **Git**
2. **复制 Deploy Hook URL**
3. **用于外部触发部署**

### 3. 手动重新部署

```bash
# 使用CLI重新部署
vercel --prod

# 或在Web界面点击 "Redeploy"
```

## ⚙️ 高级配置

### 1. 函数配置优化

编辑 `vercel.json`:
```json
{
  "functions": {
    "api/check.js": {
      "runtime": "nodejs18.x",
      "maxDuration": 10,
      "memory": 1024
    }
  }
}
```

### 2. 缓存配置

```json
{
  "headers": [
    {
      "source": "/api/check",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "s-maxage=300, stale-while-revalidate"
        }
      ]
    }
  ]
}
```

### 3. 地域配置

```json
{
  "functions": {
    "api/check.js": {
      "regions": ["iad1", "hnd1", "fra1"]
    }
  }
}
```

## 🚨 故障排除

### 常见问题

1. **部署失败**
   - 检查 `vercel.json` 语法
   - 查看构建日志
   - 确认文件路径正确

2. **函数超时**
   - 增加 `maxDuration` 设置
   - 优化代码性能
   - 检查外部API调用

3. **CORS错误**
   - 确认响应头设置
   - 检查预检请求处理

### 调试方法

```bash
# 本地调试
vercel dev

# 查看部署日志
vercel logs

# 查看项目信息
vercel inspect
```

## ✅ 完成标志

- [x] Vercel账户已注册
- [x] 项目已成功部署
- [x] API端点正常响应
- [x] 健康检查通过
- [x] 自动部署已配置

## 🔄 下一步

继续步骤3：修改客户端配置

---

**记录您的Vercel应用URL，下一步需要用到！**

# 步骤1：创建GitHub仓库

## 🎯 目标
创建用于存储安装包和版本信息的GitHub仓库

## 📋 操作步骤

### 1. 创建新仓库

1. **访问GitHub**：https://github.com
2. **点击 "New repository"**
3. **填写仓库信息**：
   - Repository name: `aipromptstudio-updates`
   - Description: `AI Prompt Studio 自动更新服务`
   - 设置为 **Public**（免费用户必须）
   - 勾选 **Add a README file**
   - 选择 **MIT License**

4. **点击 "Create repository"**

### 2. 克隆仓库到本地

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/aipromptstudio-updates.git
cd aipromptstudio-updates

# 创建目录结构
mkdir -p api
mkdir -p .github/workflows
mkdir -p releases
```

### 3. 创建API文件

创建 `api/check.js` 文件：

```javascript
// Vercel Serverless Function - 更新检查API
export default function handler(req, res) {
  // 启用CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { current_version, platform = 'windows', arch = 'x64' } = req.query;

  if (!current_version) {
    return res.status(400).json({
      error: "缺少 current_version 参数"
    });
  }

  // 版本配置 - 这里需要根据实际情况修改
  const LATEST_VERSION = {
    version: "1.1.0",
    download_url: "https://github.com/YOUR_USERNAME/aipromptstudio-updates/releases/download/v1.1.0/AIPromptStudio-1.1.0-Setup.exe",
    file_size: 52428800,
    checksum: "sha256:your_checksum_here",
    release_notes: "修复若干问题，新增强制更新功能",
    force_update: true,
    min_version: "1.0.0"
  };

  // 版本比较函数
  function compareVersions(version1, version2) {
    const v1parts = version1.split('.').map(Number);
    const v2parts = version2.split('.').map(Number);
    
    for (let i = 0; i < Math.max(v1parts.length, v2parts.length); i++) {
      const v1part = v1parts[i] || 0;
      const v2part = v2parts[i] || 0;
      
      if (v1part < v2part) return -1;
      if (v1part > v2part) return 1;
    }
    return 0;
  }

  const hasUpdate = compareVersions(current_version, LATEST_VERSION.version) < 0;

  if (hasUpdate || LATEST_VERSION.force_update) {
    console.log(`🔄 发现更新: ${current_version} -> ${LATEST_VERSION.version}`);
    res.json({
      has_update: true,
      version: LATEST_VERSION.version,
      download_url: LATEST_VERSION.download_url,
      file_size: LATEST_VERSION.file_size,
      checksum: LATEST_VERSION.checksum,
      release_notes: LATEST_VERSION.release_notes,
      force_update: LATEST_VERSION.force_update,
      min_version: LATEST_VERSION.min_version
    });
  } else {
    console.log(`✅ 版本最新: ${current_version}`);
    res.json({
      has_update: false,
      current_version: current_version,
      message: "当前已是最新版本"
    });
  }
}
```

### 4. 创建Vercel配置

创建 `vercel.json` 文件：

```json
{
  "functions": {
    "api/check.js": {
      "runtime": "nodejs18.x"
    }
  },
  "rewrites": [
    {
      "source": "/api/check",
      "destination": "/api/check.js"
    }
  ],
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        },
        {
          "key": "Access-Control-Allow-Methods",
          "value": "GET, POST, PUT, DELETE, OPTIONS"
        },
        {
          "key": "Access-Control-Allow-Headers",
          "value": "Content-Type, Authorization"
        }
      ]
    }
  ]
}
```

### 5. 创建README文档

创建 `README.md` 文件：

```markdown
# AI Prompt Studio 更新服务

## 概述
这是 AI Prompt Studio 的免费自动更新服务，使用 GitHub + Vercel 实现。

## API 接口

### 检查更新
```
GET /api/check?current_version=1.0.0&platform=windows&arch=x64
```

## 发布新版本

1. 创建新的 Release
2. 上传安装包文件
3. 更新 `api/check.js` 中的版本信息
4. 提交并推送代码

## 服务地址
- API: https://your-app.vercel.app/api/check
- 仓库: https://github.com/YOUR_USERNAME/aipromptstudio-updates
```

### 6. 提交代码

```bash
# 添加所有文件
git add .

# 提交代码
git commit -m "初始化 AI Prompt Studio 更新服务"

# 推送到GitHub
git push origin main
```

## ✅ 完成标志

- [x] GitHub仓库已创建
- [x] API代码已上传
- [x] Vercel配置已完成
- [x] 文档已创建

## 🔄 下一步

继续步骤2：配置Vercel部署

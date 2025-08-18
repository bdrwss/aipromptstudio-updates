# 步骤5：自动化和优化

## 🎯 目标
设置自动化发布流程和性能优化，提升更新服务的效率和可靠性

## 🤖 自动化发布流程

### 1. GitHub Actions 自动发布

创建 `.github/workflows/release.yml`:

```yaml
name: 自动发布新版本

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    
    steps:
      - name: 检出代码
        uses: actions/checkout@v4
        
      - name: 获取版本号
        id: get_version
        run: |
          VERSION=${GITHUB_REF#refs/tags/}
          echo "VERSION=$VERSION" >> $GITHUB_OUTPUT
          echo "VERSION_NUMBER=${VERSION#v}" >> $GITHUB_OUTPUT
        
      - name: 验证版本格式
        run: |
          if [[ ! "${{ steps.get_version.outputs.VERSION_NUMBER }}" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            echo "错误: 版本号格式不正确，应为 x.y.z"
            exit 1
          fi
        
      - name: 创建 Release
        id: create_release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: AI Prompt Studio ${{ steps.get_version.outputs.VERSION }}
          body: |
            ## 🚀 AI Prompt Studio ${{ steps.get_version.outputs.VERSION }}
            
            ### ✨ 新功能
            - 请在此处添加新功能说明
            
            ### 🐛 修复
            - 请在此处添加修复说明
            
            ### 📥 下载
            请下载对应平台的安装包进行更新。
            
            ---
            
            **发布时间**: ${{ github.event.head_commit.timestamp }}
            **提交**: ${{ github.sha }}
          draft: false
          prerelease: false
          
      - name: 更新API版本信息
        run: |
          # 自动更新 api/check.js 中的版本信息
          VERSION="${{ steps.get_version.outputs.VERSION_NUMBER }}"
          sed -i "s/version: \"[^\"]*\"/version: \"$VERSION\"/" api/check.js
          sed -i "s/v[0-9]\+\.[0-9]\+\.[0-9]\+/v$VERSION/g" api/check.js
          
      - name: 提交版本更新
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add api/check.js
          git commit -m "自动更新API版本信息到 ${{ steps.get_version.outputs.VERSION }}" || exit 0
          git push origin HEAD:main
```

### 2. 版本发布脚本

创建 `scripts/release.sh`:

```bash
#!/bin/bash

# AI Prompt Studio 版本发布脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 检查参数
if [ $# -lt 2 ]; then
    echo "用法: $0 <版本号> <安装包路径> [发布说明]"
    echo "示例: $0 1.1.0 ./AIPromptStudio-1.1.0-Setup.exe '修复若干问题'"
    exit 1
fi

VERSION=$1
INSTALLER_PATH=$2
RELEASE_NOTES=${3:-"版本更新"}

# 验证版本号格式
if [[ ! $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    log_error "版本号格式错误，应为 x.y.z"
    exit 1
fi

# 验证安装包文件
if [ ! -f "$INSTALLER_PATH" ]; then
    log_error "安装包文件不存在: $INSTALLER_PATH"
    exit 1
fi

log_info "开始发布版本 $VERSION..."

# 1. 计算文件信息
log_info "计算文件信息..."
FILE_SIZE=$(stat -c%s "$INSTALLER_PATH")
CHECKSUM=$(sha256sum "$INSTALLER_PATH" | cut -d' ' -f1)

log_info "文件大小: $(echo $FILE_SIZE | numfmt --to=iec-i)B"
log_info "SHA256: $CHECKSUM"

# 2. 创建GitHub Release
log_info "创建GitHub Release..."
gh release create "v$VERSION" \
    --title "AI Prompt Studio v$VERSION" \
    --notes "$RELEASE_NOTES" \
    "$INSTALLER_PATH"

# 3. 更新API配置
log_info "更新API配置..."
DOWNLOAD_URL="https://github.com/$(gh repo view --json owner,name -q '.owner.login + \"/\" + .name')/releases/download/v$VERSION/$(basename $INSTALLER_PATH)"

# 更新 api/check.js
cat > api/check.js << EOF
// AI Prompt Studio 更新检查API - 自动生成于 $(date)
export default function handler(req, res) {
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

  const LATEST_VERSION = {
    version: "$VERSION",
    download_url: "$DOWNLOAD_URL",
    file_size: $FILE_SIZE,
    checksum: "sha256:$CHECKSUM",
    release_notes: "$RELEASE_NOTES",
    force_update: true,
    min_version: "1.0.0",
    release_date: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  };

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
    res.json({
      has_update: true,
      version: LATEST_VERSION.version,
      download_url: LATEST_VERSION.download_url,
      file_size: LATEST_VERSION.file_size,
      checksum: LATEST_VERSION.checksum,
      release_notes: LATEST_VERSION.release_notes,
      force_update: LATEST_VERSION.force_update,
      min_version: LATEST_VERSION.min_version,
      release_date: LATEST_VERSION.release_date
    });
  } else {
    res.json({
      has_update: false,
      current_version: current_version,
      message: "当前已是最新版本"
    });
  }
}
EOF

# 4. 提交更新
log_info "提交配置更新..."
git add api/check.js
git commit -m "发布版本 $VERSION"
git push origin main

# 5. 创建Git标签
log_info "创建Git标签..."
git tag "v$VERSION"
git push origin "v$VERSION"

log_success "版本 $VERSION 发布完成！"
log_info "下载地址: $DOWNLOAD_URL"
log_info "API将在1-2分钟后更新"
```

## ⚡ 性能优化

### 1. API缓存优化

更新 `vercel.json`:

```json
{
  "functions": {
    "api/check.js": {
      "runtime": "nodejs18.x",
      "maxDuration": 10,
      "memory": 1024
    }
  },
  "headers": [
    {
      "source": "/api/check",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "s-maxage=300, stale-while-revalidate=600"
        },
        {
          "key": "CDN-Cache-Control",
          "value": "max-age=300"
        }
      ]
    }
  ]
}
```

### 2. 响应压缩

在 `api/check.js` 中添加压缩：

```javascript
export default function handler(req, res) {
  // 启用压缩
  res.setHeader('Content-Encoding', 'gzip');
  
  // 其他代码...
}
```

### 3. 错误监控

添加错误监控到 `api/check.js`:

```javascript
export default function handler(req, res) {
  try {
    // 主要逻辑
  } catch (error) {
    // 记录错误
    console.error('API错误:', {
      error: error.message,
      stack: error.stack,
      query: req.query,
      timestamp: new Date().toISOString()
    });
    
    res.status(500).json({
      error: "服务器内部错误",
      timestamp: new Date().toISOString()
    });
  }
}
```

## 📊 监控和分析

### 1. 使用统计

创建 `api/stats.js`:

```javascript
// 使用统计API
export default function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  // 这里可以集成Google Analytics或其他统计服务
  const stats = {
    total_checks: process.env.TOTAL_CHECKS || 0,
    daily_checks: process.env.DAILY_CHECKS || 0,
    last_update: new Date().toISOString()
  };
  
  res.json(stats);
}
```

### 2. 健康监控

增强 `api/health.js`:

```javascript
export default function handler(req, res) {
  const health = {
    status: 'healthy',
    service: 'AI Prompt Studio Update API',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    environment: process.env.VERCEL_ENV || 'development',
    region: process.env.VERCEL_REGION || 'unknown',
    checks: {
      api: true,
      database: true, // 如果有数据库
      external_services: true
    }
  };
  
  res.json(health);
}
```

### 3. 告警设置

创建监控脚本 `scripts/monitor.sh`:

```bash
#!/bin/bash

# 监控脚本
API_URL="https://aipromptstudio-updates.vercel.app"
WEBHOOK_URL="YOUR_SLACK_WEBHOOK_URL"

# 检查API健康状态
check_health() {
    response=$(curl -s -w "%{http_code}" "$API_URL/health")
    http_code="${response: -3}"
    
    if [ "$http_code" != "200" ]; then
        send_alert "API健康检查失败: HTTP $http_code"
        return 1
    fi
    
    return 0
}

# 发送告警
send_alert() {
    message="$1"
    curl -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"🚨 AI Prompt Studio 更新服务告警: $message\"}" \
        "$WEBHOOK_URL"
}

# 主监控循环
main() {
    if ! check_health; then
        echo "健康检查失败"
        exit 1
    fi
    
    echo "服务正常运行"
}

main
```

## 🔧 高级配置

### 1. 多环境部署

创建环境配置：

```bash
# .env.production
UPDATE_SERVER_URL=https://aipromptstudio-updates.vercel.app/api/check
ENVIRONMENT=production

# .env.staging  
UPDATE_SERVER_URL=https://aipromptstudio-updates-staging.vercel.app/api/check
ENVIRONMENT=staging

# .env.development
UPDATE_SERVER_URL=http://localhost:3000/api/check
ENVIRONMENT=development
```

### 2. A/B测试支持

在 `api/check.js` 中添加：

```javascript
// A/B测试逻辑
function shouldShowUpdate(userId, rolloutPercentage = 100) {
  if (rolloutPercentage >= 100) return true;
  
  // 基于用户ID的哈希决定是否显示更新
  const hash = require('crypto')
    .createHash('md5')
    .update(userId || 'anonymous')
    .digest('hex');
  
  const hashNumber = parseInt(hash.substring(0, 8), 16);
  const percentage = (hashNumber % 100) + 1;
  
  return percentage <= rolloutPercentage;
}
```

### 3. 版本回滚机制

创建回滚脚本 `scripts/rollback.sh`:

```bash
#!/bin/bash

# 版本回滚脚本
PREVIOUS_VERSION=$1

if [ -z "$PREVIOUS_VERSION" ]; then
    echo "用法: $0 <回滚版本号>"
    exit 1
fi

echo "回滚到版本 $PREVIOUS_VERSION..."

# 恢复API配置
git checkout "v$PREVIOUS_VERSION" -- api/check.js
git add api/check.js
git commit -m "回滚到版本 $PREVIOUS_VERSION"
git push origin main

echo "回滚完成"
```

## ✅ 完成标志

- [x] 自动化发布流程已配置
- [x] 性能优化已实施
- [x] 监控告警已设置
- [x] 多环境支持已配置
- [x] 版本管理流程已完善

## 🎉 部署完成

恭喜！您已经成功部署了完全免费的AI Prompt Studio更新服务！

### 📋 最终检查清单

- [x] GitHub仓库已创建并配置
- [x] Vercel服务已部署并运行
- [x] 客户端配置已更新
- [x] 完整测试已通过
- [x] 自动化流程已设置

### 🔗 重要链接

- **API端点**: `https://aipromptstudio-updates.vercel.app/api/check`
- **健康检查**: `https://aipromptstudio-updates.vercel.app/health`
- **GitHub仓库**: `https://github.com/YOUR_USERNAME/aipromptstudio-updates`
- **Vercel控制台**: `https://vercel.com/dashboard`

### 📞 后续支持

如需帮助，请：
1. 查看项目文档
2. 检查GitHub Issues
3. 查看Vercel日志
4. 运行测试脚本诊断

---

**🎊 您的免费更新服务已准备就绪！**

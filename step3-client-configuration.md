# 步骤3：修改客户端配置

## 🎯 目标
更新AI Prompt Studio客户端配置，指向新的免费更新服务

## 📋 需要修改的文件

### 1. 主配置文件

**文件路径**: `aipromptstudio/config.json`

**当前配置**:
```json
{
  "update": {
    "auto_check_enabled": true,
    "check_interval_hours": 6,
    "server_url": "https://update.aipromptstudio.com/api/check",
    "force_update": true,
    "auto_download": true,
    "auto_install": false,
    "check_on_startup": true,
    "notify_available": true,
    "last_check_time": null
  }
}
```

**修改后配置**:
```json
{
  "update": {
    "auto_check_enabled": true,
    "check_interval_hours": 6,
    "server_url": "https://your-app.vercel.app/api/check",
    "force_update": true,
    "auto_download": true,
    "auto_install": false,
    "check_on_startup": true,
    "notify_available": true,
    "last_check_time": null
  }
}
```

### 2. 更新服务配置

**文件路径**: `aipromptstudio/app/core/config.py`

查找并修改默认更新服务器URL：

```python
@dataclass
class UpdateConfig:
    """自动更新配置"""
    auto_check_enabled: bool = True
    check_interval_hours: int = 24
    server_url: str = "https://your-app.vercel.app/api/check"  # 修改这里
    force_update: bool = True
    auto_download: bool = False
    auto_install: bool = False
    check_on_startup: bool = True
    notify_available: bool = True
    last_check_time: Optional[str] = None
```

### 3. 更新服务实现

**文件路径**: `aipromptstudio/app/services/update_service.py`

确认更新服务器URL配置：

```python
def _load_settings(self):
    """加载更新设置（强制启用自动更新）"""
    try:
        if self.config_manager:
            # 强制设置自动更新为启用状态，忽略用户配置
            self.auto_check_enabled = True  # 强制启用
            self.check_interval_hours = min(self.config_manager.get("check_interval_hours", 6, "update"), 6)
            self.update_server_url = self.config_manager.get("server_url", "https://your-app.vercel.app/api/check", "update")  # 修改默认URL
            # ... 其他配置
```

## 🔧 具体修改步骤

### 步骤1：修改主配置文件

```bash
# 编辑配置文件
nano aipromptstudio/config.json

# 或使用您喜欢的编辑器
code aipromptstudio/config.json
```

将 `server_url` 从：
```
"https://update.aipromptstudio.com/api/check"
```

修改为：
```
"https://your-app.vercel.app/api/check"
```

**注意**: 将 `your-app` 替换为您实际的Vercel应用名称。

### 步骤2：修改默认配置

编辑 `aipromptstudio/app/core/config.py`:

```python
# 找到 UpdateConfig 类
@dataclass
class UpdateConfig:
    """自动更新配置"""
    auto_check_enabled: bool = True
    check_interval_hours: int = 24
    server_url: str = "https://your-app.vercel.app/api/check"  # 修改这里
    force_update: bool = True
    auto_download: bool = False
    auto_install: bool = False
    check_on_startup: bool = True
    notify_available: bool = True
    last_check_time: Optional[str] = None
```

### 步骤3：修改更新服务

编辑 `aipromptstudio/app/services/update_service.py`:

```python
def __init__(self, db_manager, config_manager=None):
    super().__init__(db_manager)
    self.config_manager = config_manager
    self.current_version = "1.0.0"

    # 更新设置 - 强制启用自动更新
    self.auto_check_enabled = True
    self.check_interval_hours = 6
    self.update_server_url = "https://your-app.vercel.app/api/check"  # 修改这里
    # ... 其他设置
```

## 🧪 测试配置

### 1. 本地测试

```python
# 创建测试脚本 test_update.py
import requests
import json

def test_update_api():
    url = "https://your-app.vercel.app/api/check"
    params = {
        "current_version": "1.0.0",
        "platform": "windows",
        "arch": "x64"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print("✅ API测试成功:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        return True
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False

if __name__ == "__main__":
    test_update_api()
```

运行测试：
```bash
python test_update.py
```

### 2. 客户端测试

启动AI Prompt Studio并检查：

1. **启动应用**
2. **查看日志**，确认更新检查请求发送到正确的URL
3. **检查网络请求**，确认没有错误

## 🔄 环境配置

### 开发环境

```json
{
  "update": {
    "server_url": "http://localhost:3000/api/check"
  }
}
```

### 测试环境

```json
{
  "update": {
    "server_url": "https://your-app-preview.vercel.app/api/check"
  }
}
```

### 生产环境

```json
{
  "update": {
    "server_url": "https://your-app.vercel.app/api/check"
  }
}
```

## 📱 多环境配置

### 配置文件模板

创建 `config.template.json`:

```json
{
  "update": {
    "auto_check_enabled": true,
    "check_interval_hours": 6,
    "server_url": "${UPDATE_SERVER_URL}",
    "force_update": true,
    "auto_download": true,
    "auto_install": false,
    "check_on_startup": true,
    "notify_available": true,
    "last_check_time": null
  }
}
```

### 环境变量替换脚本

```python
# config_generator.py
import os
import json

def generate_config():
    # 读取模板
    with open('config.template.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 替换环境变量
    update_server_url = os.getenv('UPDATE_SERVER_URL', 'https://your-app.vercel.app/api/check')
    config['update']['server_url'] = update_server_url
    
    # 写入配置文件
    with open('aipromptstudio/config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 配置文件已生成，更新服务器: {update_server_url}")

if __name__ == "__main__":
    generate_config()
```

## 🔒 安全考虑

### 1. URL验证

在更新服务中添加URL验证：

```python
def validate_update_url(self, url):
    """验证更新服务器URL"""
    allowed_domains = [
        'your-app.vercel.app',
        'your-custom-domain.com'
    ]
    
    from urllib.parse import urlparse
    parsed = urlparse(url)
    
    if parsed.hostname not in allowed_domains:
        raise ValueError(f"不允许的更新服务器域名: {parsed.hostname}")
    
    if parsed.scheme != 'https':
        raise ValueError("更新服务器必须使用HTTPS")
    
    return True
```

### 2. 请求签名（可选）

```python
import hmac
import hashlib

def sign_request(self, params, secret_key):
    """为请求添加签名"""
    message = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
    signature = hmac.new(
        secret_key.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    
    params['signature'] = signature
    return params
```

## ✅ 完成标志

- [x] 主配置文件已修改
- [x] 默认配置已更新
- [x] 更新服务配置已修改
- [x] 本地测试通过
- [x] 客户端测试正常

## 🔄 下一步

继续步骤4：测试和验证

---

**重要提醒**: 
1. 将所有 `your-app` 替换为您实际的Vercel应用名称
2. 如果使用自定义域名，请使用自定义域名URL
3. 确保所有URL都使用HTTPS协议

# 步骤4：测试和验证

## 🎯 目标
测试完整的更新流程，确保客户端能正常检查和下载更新

## 📋 测试清单

### 1. API服务测试

#### 自动化测试脚本

```bash
# 运行测试脚本
python github-vercel-setup/test_update_api.py

# 或指定自定义URL
python github-vercel-setup/test_update_api.py https://your-app.vercel.app/api/check
```

#### 手动API测试

```bash
# 1. 健康检查
curl "https://aipromptstudio-updates.vercel.app/health"

# 2. 更新检查 - 有更新
curl "https://aipromptstudio-updates.vercel.app/api/check?current_version=1.0.0"

# 3. 更新检查 - 无更新
curl "https://aipromptstudio-updates.vercel.app/api/check?current_version=2.0.0"

# 4. 错误处理测试
curl "https://aipromptstudio-updates.vercel.app/api/check"
```

### 2. 客户端集成测试

#### 修改客户端版本进行测试

临时修改 `aipromptstudio/config.json` 中的版本：

```json
{
  "version": "0.9.0"
}
```

#### 启动客户端测试

```bash
# 进入客户端目录
cd aipromptstudio

# 启动应用
python main.py
```

#### 检查日志输出

查看控制台输出，确认：
- ✅ 更新检查请求发送到正确URL
- ✅ 收到更新响应
- ✅ 强制更新对话框显示
- ✅ 下载链接正确

### 3. 网络请求验证

#### 使用浏览器开发者工具

1. **打开浏览器**
2. **按F12打开开发者工具**
3. **切换到Network标签**
4. **访问**: `https://aipromptstudio-updates.vercel.app/api/check?current_version=1.0.0`
5. **检查请求详情**:
   - 状态码: 200
   - 响应时间: < 500ms
   - CORS头: 正确设置

#### 使用Postman测试

```json
GET https://aipromptstudio-updates.vercel.app/api/check
Params:
  current_version: 1.0.0
  platform: windows
  arch: x64
```

### 4. 版本发布测试

#### 创建测试Release

```bash
# 1. 创建测试文件
echo "Test installer" > test-installer.exe

# 2. 创建GitHub Release
gh release create v1.1.0-test \
  --title "AI Prompt Studio v1.1.0 (测试版)" \
  --notes "这是一个测试版本，用于验证更新功能" \
  --prerelease \
  test-installer.exe
```

#### 更新API配置

编辑 `github-vercel-setup/api/check.js`:

```javascript
const LATEST_VERSION = {
  version: "1.1.0",
  download_url: "https://github.com/YOUR_USERNAME/aipromptstudio-updates/releases/download/v1.1.0-test/test-installer.exe",
  file_size: 1024,
  checksum: "sha256:test_checksum",
  release_notes: "测试版本更新",
  force_update: true,
  min_version: "1.0.0"
};
```

#### 提交更新

```bash
git add api/check.js
git commit -m "更新测试版本配置"
git push origin main
```

## 🧪 详细测试用例

### 测试用例1: 正常更新流程

**前置条件**: 客户端版本 < 最新版本

**测试步骤**:
1. 启动AI Prompt Studio
2. 等待自动更新检查
3. 确认弹出更新对话框
4. 点击下载按钮
5. 验证下载进度
6. 确认安装提示

**预期结果**:
- ✅ 检测到更新
- ✅ 显示强制更新对话框
- ✅ 无法取消更新
- ✅ 下载链接有效

### 测试用例2: 无更新情况

**前置条件**: 客户端版本 >= 最新版本

**测试步骤**:
1. 修改客户端版本为 "2.0.0"
2. 启动AI Prompt Studio
3. 等待自动更新检查

**预期结果**:
- ✅ 不显示更新对话框
- ✅ 日志显示"当前已是最新版本"

### 测试用例3: 网络异常处理

**前置条件**: 模拟网络异常

**测试步骤**:
1. 修改配置为无效URL
2. 启动AI Prompt Studio
3. 观察错误处理

**预期结果**:
- ✅ 显示网络错误提示
- ✅ 应用正常启动
- ✅ 后续重试机制工作

### 测试用例4: 强制更新验证

**前置条件**: 设置 force_update = true

**测试步骤**:
1. 确保API返回 force_update: true
2. 启动客户端
3. 尝试关闭更新对话框

**预期结果**:
- ✅ 无法关闭更新对话框
- ✅ 无取消按钮
- ✅ 必须完成更新

## 📊 性能测试

### 响应时间测试

```bash
# 使用curl测试响应时间
for i in {1..10}; do
  curl -w "响应时间: %{time_total}s\n" -o /dev/null -s \
    "https://aipromptstudio-updates.vercel.app/api/check?current_version=1.0.0"
done
```

### 并发测试

```python
# concurrent_test.py
import requests
import threading
import time

def test_api():
    url = "https://aipromptstudio-updates.vercel.app/api/check"
    params = {"current_version": "1.0.0"}
    
    try:
        start = time.time()
        response = requests.get(url, params=params, timeout=10)
        end = time.time()
        
        print(f"状态: {response.status_code}, 时间: {end-start:.3f}s")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

# 并发测试
threads = []
for i in range(20):
    t = threading.Thread(target=test_api)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

## 🔍 故障排除

### 常见问题及解决方案

#### 1. API返回404错误

**原因**: Vercel配置问题
**解决**:
```bash
# 检查vercel.json配置
cat vercel.json

# 重新部署
vercel --prod
```

#### 2. CORS错误

**原因**: 跨域配置问题
**解决**:
```javascript
// 在api/check.js中确认CORS头
res.setHeader('Access-Control-Allow-Origin', '*');
```

#### 3. 客户端连接超时

**原因**: 网络或服务器问题
**解决**:
```python
# 增加超时时间
response = requests.get(url, timeout=30)
```

#### 4. 版本比较错误

**原因**: 版本格式不一致
**解决**:
```javascript
// 确保版本格式为 x.y.z
const version = "1.0.0";  // 正确
const version = "v1.0";   // 错误
```

### 调试工具

#### 1. Vercel日志

```bash
# 实时查看日志
vercel logs --follow

# 查看特定函数日志
vercel logs api/check.js
```

#### 2. 网络抓包

```bash
# 使用tcpdump抓包
sudo tcpdump -i any -w update_api.pcap host aipromptstudio-updates.vercel.app

# 使用Wireshark分析
wireshark update_api.pcap
```

#### 3. 客户端调试

```python
# 在更新服务中添加调试日志
import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.debug(f"发送更新请求: {url}")
```

## ✅ 验收标准

### 功能验收

- [x] API健康检查正常
- [x] 更新检查返回正确结果
- [x] 版本比较逻辑正确
- [x] 强制更新功能工作
- [x] 错误处理完善
- [x] CORS配置正确

### 性能验收

- [x] API响应时间 < 500ms
- [x] 并发处理能力 > 10 QPS
- [x] 可用性 > 99.9%
- [x] 错误率 < 0.1%

### 安全验收

- [x] HTTPS强制使用
- [x] 输入参数验证
- [x] 错误信息不泄露敏感信息
- [x] 无SQL注入风险

## 📝 测试报告模板

```markdown
# AI Prompt Studio 更新服务测试报告

## 测试概要
- 测试时间: 2025-01-16
- 测试环境: 生产环境
- 测试版本: v1.0.0

## 测试结果
- 总测试用例: 15
- 通过用例: 15
- 失败用例: 0
- 成功率: 100%

## 性能指标
- 平均响应时间: 180ms
- 最大响应时间: 350ms
- 并发处理: 20 QPS
- 错误率: 0%

## 问题记录
无

## 结论
✅ 更新服务已准备就绪，可以正式上线使用。
```

## 🔄 下一步

继续步骤5：自动化和优化

---

**测试完成后，确保所有功能正常工作再进入下一步！**

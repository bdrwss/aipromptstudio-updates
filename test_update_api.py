#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI Prompt Studio 更新API测试脚本
用于测试GitHub + Vercel免费更新服务
"""

import requests
import json
import time
from urllib.parse import urlparse

class UpdateAPITester:
    def __init__(self, api_url="https://bdrwss-aipromptstudio-updates.vercel.app/api/check"):
        self.api_url = api_url
        self.health_url = api_url.replace('/api/check', '/health')
        
    def test_health_check(self):
        """测试健康检查端点"""
        print("🔍 测试健康检查...")
        try:
            response = requests.get(self.health_url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            print("✅ 健康检查通过:")
            print(f"   状态: {data.get('status')}")
            print(f"   服务: {data.get('service')}")
            print(f"   版本: {data.get('version')}")
            print(f"   时间: {data.get('timestamp')}")
            return True
            
        except requests.RequestException as e:
            print(f"❌ 健康检查失败: {e}")
            return False
        except Exception as e:
            print(f"❌ 健康检查错误: {e}")
            return False
    
    def test_update_check(self, current_version="1.0.0"):
        """测试更新检查"""
        print(f"🔍 测试更新检查 (当前版本: {current_version})...")
        
        params = {
            "current_version": current_version,
            "platform": "windows",
            "arch": "x64",
            "user_id": "test_user"
        }
        
        try:
            start_time = time.time()
            response = requests.get(self.api_url, params=params, timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            response.raise_for_status()
            data = response.json()
            
            print("✅ 更新检查成功:")
            print(f"   响应时间: {response_time:.2f}ms")
            print(f"   有更新: {data.get('has_update')}")
            
            if data.get('has_update'):
                print(f"   最新版本: {data.get('version')}")
                print(f"   下载地址: {data.get('download_url')}")
                print(f"   文件大小: {data.get('file_size', 0) / 1024 / 1024:.2f}MB")
                print(f"   强制更新: {data.get('force_update')}")
                print(f"   发布说明: {data.get('release_notes', '')[:100]}...")
            else:
                print(f"   当前版本: {data.get('current_version')}")
                print(f"   消息: {data.get('message')}")
            
            return True
            
        except requests.RequestException as e:
            print(f"❌ 更新检查失败: {e}")
            return False
        except Exception as e:
            print(f"❌ 更新检查错误: {e}")
            return False
    
    def test_version_comparison(self):
        """测试版本比较逻辑"""
        print("🔍 测试版本比较逻辑...")
        
        test_cases = [
            ("0.9.0", True),   # 应该有更新
            ("1.0.0", True),   # 强制更新
            ("1.1.0", False),  # 已是最新
            ("2.0.0", False),  # 更高版本
        ]
        
        for version, expected_update in test_cases:
            print(f"   测试版本 {version}...")
            params = {
                "current_version": version,
                "platform": "windows",
                "arch": "x64"
            }
            
            try:
                response = requests.get(self.api_url, params=params, timeout=5)
                response.raise_for_status()
                data = response.json()
                
                has_update = data.get('has_update', False)
                if has_update == expected_update:
                    print(f"   ✅ {version}: 预期={expected_update}, 实际={has_update}")
                else:
                    print(f"   ⚠️ {version}: 预期={expected_update}, 实际={has_update}")
                    
            except Exception as e:
                print(f"   ❌ {version}: 测试失败 - {e}")
        
        return True
    
    def test_error_handling(self):
        """测试错误处理"""
        print("🔍 测试错误处理...")
        
        # 测试缺少参数
        try:
            response = requests.get(self.api_url, timeout=5)
            if response.status_code == 400:
                print("   ✅ 缺少参数处理正确")
            else:
                print(f"   ⚠️ 缺少参数处理异常: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 缺少参数测试失败: {e}")
        
        # 测试无效方法
        try:
            response = requests.post(self.api_url, timeout=5)
            if response.status_code == 405:
                print("   ✅ 无效方法处理正确")
            else:
                print(f"   ⚠️ 无效方法处理异常: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 无效方法测试失败: {e}")
        
        return True
    
    def test_cors(self):
        """测试CORS配置"""
        print("🔍 测试CORS配置...")
        
        try:
            # 发送OPTIONS预检请求
            response = requests.options(self.api_url, timeout=5)
            
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
            }
            
            print("   CORS头信息:")
            for header, value in cors_headers.items():
                if value:
                    print(f"   ✅ {header}: {value}")
                else:
                    print(f"   ⚠️ {header}: 未设置")
            
            return True
            
        except Exception as e:
            print(f"   ❌ CORS测试失败: {e}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🧪 开始运行 AI Prompt Studio 更新API测试...\n")
        
        tests = [
            ("健康检查", self.test_health_check),
            ("更新检查", self.test_update_check),
            ("版本比较", self.test_version_comparison),
            ("错误处理", self.test_error_handling),
            ("CORS配置", self.test_cors),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n📋 {test_name}测试:")
            try:
                if test_func():
                    passed += 1
                    print(f"✅ {test_name}测试通过")
                else:
                    print(f"❌ {test_name}测试失败")
            except Exception as e:
                print(f"❌ {test_name}测试异常: {e}")
            
            print("-" * 50)
        
        print(f"\n📊 测试结果汇总:")
        print(f"   总测试数: {total}")
        print(f"   通过测试: {passed}")
        print(f"   失败测试: {total - passed}")
        print(f"   成功率: {(passed / total) * 100:.1f}%")
        
        if passed == total:
            print("\n🎉 所有测试通过！更新API服务运行正常。")
            return True
        else:
            print("\n⚠️ 部分测试失败，请检查服务配置。")
            return False

def main():
    """主函数"""
    import sys
    
    # 获取API URL
    if len(sys.argv) > 1:
        api_url = sys.argv[1]
    else:
        api_url = "https://bdrwss-aipromptstudio-updates.vercel.app/api/check"
    
    print(f"🎯 测试目标: {api_url}")
    print(f"🌐 域名: {urlparse(api_url).netloc}")
    print("=" * 60)
    
    # 运行测试
    tester = UpdateAPITester(api_url)
    success = tester.run_all_tests()
    
    # 退出码
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

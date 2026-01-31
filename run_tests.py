# 创建运行脚本
echo import subprocess > run_tests.py
echo import sys >> run_tests.py
echo import os >> run_tests.py
echo. >> run_tests.py
echo def run_all_tests(): >> run_tests.py
echo     print("🚀 开始运行所有测试...") >> run_tests.py
echo     result = subprocess.run(["pytest", "tests/", "-v"], capture_output=True, text=True) >> run_tests.py
echo     print("测试结果:") >> run_tests.py
echo     print(result.stdout) >> run_tests.py
echo     if result.stderr: >> run_tests.py
echo         print("错误信息:", result.stderr) >> run_tests.py
echo     return result.returncode >> run_tests.py
echo. >> run_tests.py
echo if __name__ == "__main__": >> run_tests.py
echo     run_all_tests() >> run_tests.py
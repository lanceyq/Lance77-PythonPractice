import importlib
import sys
import os

# 打印当前工作目录
print(f"Current working directory: {os.getcwd()}")

# 打印Python搜索路径
print(f"Python path: {sys.path}")

# 尝试导入main模块
try:
    print("Trying to import main module...")
    main_module = importlib.import_module('main')
    print("Successfully imported main module")
    
    # 检查main模块中的属性
    print(f"Attributes in main module: {dir(main_module)}")
    
    # 检查是否有app属性
    if hasattr(main_module, 'app'):
        print("Found 'app' attribute in main module!")
        print(f"Type of app: {type(main_module.app)}")
    else:
        print("ERROR: 'app' attribute not found in main module!")

except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
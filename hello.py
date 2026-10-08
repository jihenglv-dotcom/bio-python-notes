"""环境验收脚本｜吕基恒 · M1

用途：确认 VS Code 跑起来的解释器确实是 conda 的 bioinfo 环境（而不是系统 Python 3.13）。
跑法：VS Code 打开 bio-python 文件夹 → 打开本文件 → 右上角 ▷ Run Python File（或 Ctrl+F5）
合格：下面「解释器」那一行必须包含 envs\bioinfo
"""

import sys

print("=" * 52)
print("Python 版本 :", sys.version.split()[0])
print("解释器      :", sys.executable)
print("=" * 52)

# 关键判定：路径里有没有 envs\bioinfo
if "envs" in sys.executable and "bioinfo" in sys.executable:
    print("[OK]   解释器 = bioinfo 环境，正确")
else:
    print("[FAIL] 解释器不是 bioinfo 环境！")
    print("       请在 VS Code 里 Ctrl+Shift+P → Python: Select Interpreter")
    print(r"       手动指定 D:\miniconda3\envs\bioinfo\python.exe")

print()

# 逐个 import，缺哪个就报哪个，方便定位
# 注意：import 的名字（module）和 pip 装的名字（pip_name）有时不一样，
#       比如 biopython 装完后 import 的是 Bio。这是新手最常踩的坑之一。
packages = [
    ("numpy", "numpy", "numpy"),
    ("pandas", "pandas", "pandas"),
    ("matplotlib", "matplotlib", "matplotlib"),
    ("biopython", "Bio", "biopython"),
]

failed = []
for label, module, pip_name in packages:
    try:
        mod = __import__(module)
        version = getattr(mod, "__version__", "未知版本")
        print(f"[OK]   {label:<18} {version}")
    except ImportError:
        print(f"[FAIL] {label:<18} 未安装")
        failed.append(pip_name)

print()
if failed:
    print("缺失的包，在 Anaconda Prompt 里执行：")
    print("  conda activate bioinfo")
    print("  pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple " + " ".join(failed))
else:
    print("全部通过。10/7 环境搭建验收成功。")

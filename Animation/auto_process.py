import subprocess
import sys

# Blender 路径
blender_path = '/usr/local/blender/blender'  # 替换为你实际的 Blender 路径
python_script_path = '/path/to/my_blender_script.py'  # 替换为你的 Python 脚本路径

# 构建命令
command = [blender_path, '-b', '-P', python_script_path]
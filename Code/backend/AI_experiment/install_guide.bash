# 创建虚拟环境（推荐）
conda create -n script_ai python=3.8
conda activate script_ai

# 安装Hugging Face Transformers + PyTorch
pip install transformers[torch]  # 自动匹配CUDA版本
pip install datasets             # 数据处理工具

# 运行 install_test.py 测试是否安装成功
# 运行 model_test.py 测试是否能够加载最基本的模型
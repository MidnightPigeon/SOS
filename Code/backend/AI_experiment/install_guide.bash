# 一、创建虚拟环境（推荐）
conda create -n script_ai python=3.11 # 创建虚拟环境，请勿在运行后续代码后重复创建，否则会直接清空所有已安装的包
conda activate script_ai

# 二、安装Hugging Face Transformers + PyTorch

nvidia-smi # 如果你是Nvidia显卡，查看 Cuda Version
# CUDA 12.x
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# 并不知道其他配置怎么安装，可能默认最新版？

pip install transformers[torch]  # 自动匹配CUDA版本
pip install datasets             # 数据处理工具
# 如果安装失败，可以尝试以下命令（镜像源）
pip install transformers[torch] -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn # 清华真拉，镜像都连不上 
pip install transformers[torch] -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com # 还是阿里比较给力
pip install datasets -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn 
pip install datasets -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com 

# 三、安装后测试
# cd 到 AI_experiment 文件夹，在此目录下执行
cd SOS/Code/backend/AI_experiment

python install_test.py # 测试是否安装成功及查看电脑参数
python model_test.py # 测试是否能够加载最基本的模型
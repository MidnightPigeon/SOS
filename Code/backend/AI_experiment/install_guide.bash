# 一、创建虚拟环境（推荐）
conda create -n script_ai python=3.11 # 创建虚拟环境，请勿在运行后续代码后重复创建，否则会直接清空所有已安装的包
conda activate script_ai

# 二、安装Hugging Face LTP + PyTorch

nvidia-smi # 如果你是Nvidia显卡，查看 Cuda Version
# CUDA 12.x
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# 并不知道其他配置怎么安装，可能默认最新版？

# pip install transformers[torch]  # 自动匹配CUDA版本,可能不再需要这条指令了
pip install ltp             # LTP分词工具

# 重要！！！
# 访问 https://huggingface.co/LTP/base/resolve/main/pytorch_model.bin?download=true 下载模型文件，放在Code/backend/base 文件夹下
# github 不支持push大于100MB的文件，所以无法上传模型文件，需要各位手动下载


# 如果安装失败，可以尝试以下命令（镜像源）
-i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn # 清华真拉，镜像都连不上 
-i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com # 还是阿里比较给力


# 三、安装后测试
python Code/backend/AI_experiment/install_test.py # 测试torch是否安装成功及查看电脑参数
python Code/backend/AI_experiment/LTP_test.py # 测试LTP是否能够加载最基本的模型，墙内网络不稳定，可能会失败(方滨兴我囸你先人)
python Code/backend/AI_experiment/LTP_attempt.py # input.txt为测试输入，测试是否能够完成分词任务
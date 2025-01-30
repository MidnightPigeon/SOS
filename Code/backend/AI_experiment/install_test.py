import torch
print(f"PyTorch版本: {torch.__version__}")
print(f"GPU可用: {torch.cuda.is_available()}")  # 输出应为True（如果使用GPU）


# 我的输出：
#   PyTorch版本: 2.5.1+cu121
#   GPU可用: True
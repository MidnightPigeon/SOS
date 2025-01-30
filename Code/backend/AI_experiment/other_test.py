import torch
print(torch.cuda.is_available())

import sys
print(sys.executable)  # 输出当前Python解释器路径
print(sys.path)   # 输出当前Python解释器搜索路径
print(sys.getdefaultencoding()) # 输出当前Python解释器默认编码
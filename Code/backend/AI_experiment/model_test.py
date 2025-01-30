from transformers import DistilBertTokenizer, DistilBertModel

# 中文推荐版本（支持多语言）
model_name = "distilbert-base-multilingual-cased"

# 首次运行会自动下载
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = DistilBertModel.from_pretrained(model_name)

def test_installation():
    test_text = "测试文本"
    try:
        inputs = tokenizer(test_text, return_tensors="pt")
        outputs = model(**inputs)
        return "✅ 安装成功！模型正常运行"
    except Exception as e:
        return f"❌ 安装失败：{str(e)}"

print(test_installation())

text = "文景方圆"
# 分词处理
inputs = tokenizer(
    text,
    return_tensors="pt",  # 返回PyTorch张量
    truncation=True,
    max_length=512
)

# 获取模型输出
outputs = model(**inputs)
print(outputs.last_hidden_state.shape)  # 输出形状：[1, 序列长度, 768]

# 获取CLS令牌表示
cls_embedding = outputs.last_hidden_state[:, 0, :]
print(f"CLS向量维度: {cls_embedding.shape}")  # [1, 768]

# 我的输出：
#   torch.Size([1, 6, 768])
#   CLS向量维度: torch.Size([1, 768])
# 至此，我们已经成功加载了DistilBERT模型。
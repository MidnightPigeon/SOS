# 引入必要的库和模块
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch  # 用于张量和GPU计算
from torch.utils.data import Dataset, DataLoader  # 数据处理类

# 定义一个简单的数据集类来加载和预处理文本数据
class TextDataset(Dataset):
    def __init__(self, tokenizer, texts, labels, max_length=128):
        self.tokenizer = tokenizer
        self.texts = texts
        self.labels = labels
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]

        # 使用tokenizer对文本进行编码
        encoding = self.tokenizer(
            text,
            truncation=True,  # 截断过长的文本
            padding='max_length',  # 填充到固定长度
            max_length=self.max_length,
            return_tensors='pt'  # 返回张量格式
        )

        # 将编码结果转换为字典，并添加标签
        item = {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

        return item

# 定义训练函数
def train_model(model, tokenizer, texts, labels, num_epochs=3):
    # 创建数据集和数据加载器
    dataset = TextDataset(tokenizer, texts, labels)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

    # 设备设置（优先使用GPU）
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # 定义优化器
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

    # 开始训练循环
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0

        for batch in dataloader:
            # 零梯度
            optimizer.zero_grad()

            # 将数据移动到GPU（如果可用）
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            # 前向传播
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )

            # 获取损失值
            loss = outputs.loss

            # 反向传播和优化
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        # 打印 epoch 的平均损失值
        avg_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch + 1}/{num_epochs}, Average Loss: {avg_loss:.4f}")

# 加载预训练模型和tokenizer
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")

# 示例数据（正向情感标记为1，负向为0）
texts = [
    "I love this movie!", "This book is bad", "Amazing experience!",
    "Horrible movie", "I really liked the book.", "The film was awful",
    "I feel so happy after reading this book!", "This movie is terrible.",
    "The best movie ever.", "Very disappointing book."
]
labels = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

# 开始训练
train_model(model, tokenizer, texts, labels, num_epochs=10)

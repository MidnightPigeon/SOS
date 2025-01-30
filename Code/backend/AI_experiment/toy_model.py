from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch

# 1. 准备数据
train_texts = [
    "I love this movie!", "This book is bad", "Amazing experience!", "Horrible movie",
    "I really liked the book.", "The film was awful", "I feel so happy after reading this book!",
    "This movie is terrible.", "The best movie ever.", "Very disappointing book."
]
train_labels = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

# 2. 初始化模型和分词器
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")

# 3. 数据预处理
train_encodings = tokenizer(
    train_texts,
    truncation=True,
    padding=True,
    max_length=16,
    return_tensors="pt"
)

# 转换为数据集格式
class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = CustomDataset(train_encodings, train_labels)

# 4. 训练配置
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using {device} device")
model.to(device)
model.train()

train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=8, shuffle=True)
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

# 5. 增加训练轮数 (Epochs)
num_epochs = 30
for epoch in range(num_epochs):
    total_loss = 0
    for batch in train_loader:
        optimizer.zero_grad()
        inputs = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**inputs)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    avg_loss = total_loss / len(train_loader)
    print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {avg_loss:.4f}")

print("训练完成！")

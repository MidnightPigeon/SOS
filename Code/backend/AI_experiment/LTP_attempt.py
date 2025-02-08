import torch
from ltp import LTP
import pandas as pd

def extract_action_triples(text, ltp):
    """
    从输入文本中抽取动作三元组（动作发出者、动作类型、动作对象）。
    利用 LTP 的分词、词性标注和依存句法分析结果。
    """
    # 简单按中文逗号分句（实际场景建议使用更健壮的分句方法）
    sentences = text.split("，")
    actions = []
    
    # 同时获取分词、词性标注和依存句法分析结果
    output = ltp.pipeline(sentences, tasks=["cws", "pos", "dep"])
    print(output.cws, output.pos, output.dep)
    # 遍历每个句子的处理结果
    for words, pos_tags, dep in zip(output.cws, output.pos, output.dep):
        print("words ", words)
        print("pos_tags ", pos_tags)
        print("dep ", dep)
        # 遍历当前句子的所有词，查找动词
        for idx, (word, pos) in enumerate(zip(words, pos_tags)):
            print(" word ", word)
            print(" pos ", pos)
            if pos.startswith("v"):  # 简单判断：以 "v" 开头的词认为是动词
                verb = word
                subject = ""
                obj = ""
                # 遍历依存句法分析结果
                heads = dep['head']
                print(" heads ", heads)
                labels = dep['label']
                for i in range(len(heads)):
                    head = heads[i]
                    relation = labels[i]
                    word = words[i]
                    if head == idx + 1:  # 注意：head 是 1-indexed
                        if relation == "SBV":
                            subject = word
                        elif relation == "VOB":
                            obj = word
                # 针对“跑”这一动词，如果缺少宾语则补充“远处”
                #   if verb == "跑" and not obj:
                #   obj = "远处"
                # 如果至少存在施事或受事，则认为该动作有效
                if subject or obj:
                    actions.append((subject, verb, obj))
    return actions

if __name__ == "__main__":
    # 初始化 LTP 模型，使用 Small 版本（也可以传入模型路径）
    ltp = LTP("Code/backend/base", local_files_only=True)
    
    # 如果有 GPU 可用，将模型移动到 GPU 上
    if torch.cuda.is_available():
        ltp.to("cuda")
    
    # 自定义词表
    ltp.add_word("汤姆去", freq=2)
    ltp.add_words(["外套", "外衣"], freq=2)
    
    # 输入示例文本
    with open('Code/backend/AI_experiment/input.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 抽取动作三元组
    action_triples = extract_action_triples(text, ltp)
    print("抽取的动作三元组：", action_triples)
    
    # 使用 pandas 展示为表格
    df = pd.DataFrame(action_triples, columns=["动作发出者", "动作类型", "动作对象"])
    print("\n动作表格：")
    print(df)

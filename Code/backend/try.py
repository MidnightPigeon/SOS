import jieba
import os

# sentence = input("请输入所需字符串 ")

sentence = "我们的大学生创业项目名叫文景方圆，\n目的为通过现代技术与机器学习相结合，\n使计算机可以基于简要的文本描述进行拓展，\n产出可视化程度极高的3D建模动画。"
words_exact = jieba.cut(sentence)
print("精确模式结果：\n" + "/".join(words_exact)+'\n')  # 精确模式的分词结果（即默认模式），不会重复切分句子

words_full = jieba.cut(sentence, cut_all=True)
print("全模式结果：\n" + "/".join(words_full)+'\n')  # 全模式的分词结果，把句子中所有可以成词的词语都扫描出来

jieba.add_word('文景方圆') # 添加自定义词语
dict_path = os.path.join(os.path.dirname(__file__), 'dict.txt') 
jieba.load_userdict(dict_path) # 载入自定义词典，每一行从左到右依次为： 词语，*词频，*词性
words_updated = jieba.cut(sentence) 
print("载入词语后精确模式结果：\n" + "/".join(words_updated)+'\n')



import jieba
import os
import re

def read_act_1():
    with open('./Code/backend/script/act_1.txt', 'r', encoding='utf-8') as file:
        time = []
        scene = []
        character = []
        count = 0
        for line in file:
            # 先进行背景化的预处理
            if line[0:2] == '时间' or line[0:2] == '地点' or line[0:2] == '人物':
                if line[0:2] == '时间':
                    time = line[2:].lstrip()
                    count += 1
                elif line[0:2] == '地点':
                    scene = line[2:].lstrip()
                    count += 1
                elif line[0:2] == '人物':
                    character = line[2:].lstrip()
                    count += 1

                if count == 3:
                    break
        
        # 时间地点人物信息存取完毕
        
    print(time)
    print(scene)
    print(character)
    
    with open('./Code/backend/script/act_1.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.lstrip()  # 去掉行首的空白字符
            words = jieba.cut(line)
            print("/".join(words))
    
    #要进行更细节化的NLP了。爬去看NLP
    
read_act_1()
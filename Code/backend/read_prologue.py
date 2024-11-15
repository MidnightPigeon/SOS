import jieba
import os
import re

def read_prologue():
    people_list = []
    with open('./Code/backend/script/prologue.txt', 'r', encoding='utf-8') as file:
        for line in file:
            # 使用正则表达式匹配破折号前的名字,特征：1-5个字，在破折号前
            match = re.match(r'^(.{1,5})\s*[—-]{2}', line)
            if match:
                # 输出匹配到的名字
                name = match.group(1).replace(' ', '').replace('。', '')
                jieba.add_word(name) # 添加自定义词语，这是根据剧本内容确定的一些词语，记录下来用于以后使用
                gender = gender_match(line)
                age = age_match(line)
                age_group = age_group_match(age,line)

                person_info = {
                    'name': name,
                    'gender': gender,
                    'age': age,
                    'age_group': age_group,
                }
                print(person_info)
            people_list.append(person_info)

    with open('./Code/backend/script/prologue.txt', 'r', encoding='utf-8') as file:
        for line in file:
            words = jieba.cut(line)
            print("/".join(words))
    return people_list

def gender_match(line):
    matchGender = re.search(r'(男|女)', line)
    InferFemale = re.findall(r'(她|妈|母|奶|姨|姑|姐|妹|女士|尼姑|少女|妇|婆|夫人|闺蜜|女儿|妞)', line)
    #两个Infer函数都记录了相应的，表征性别词语出现的次数
    InferMale = re.findall(r'(他|爸|父|爷|叔|舅|弟|哥|先生|和尚|公子|儿|少年|太监|公|丈夫)', line)
    if matchGender:
        return matchGender.group(1) #用来获取匹配的内容，也就是 男 或 女 字符。
    if (InferFemale > InferMale): #如果女性词语出现次数大于男性
        return '女'
    if (InferMale > InferFemale):
        return '男'
    return '?' # 未知性别或非二元性别，返回?
def age_match(line):
    matchAge = re.search(r'([零一二两三四五六七八九十百]+多岁|[零一二两三四五六七八九十百]+来岁|[零一二两三四五六七八九十百]+几岁|[零一二两三四五六七八九十百]+岁)', line)
    age = 0
    round = 0 #round可以用来处理权数，用来处理后面跟十、百、千等可能出现的，并能够与先前记录的ageTemp进行组合匹配
    ageTemp=0
    if not matchAge:
        return 114514 #？何意啊
    for char in matchAge.group(1):
        if char == '一':
            ageTemp += 1
            round += 1
        if char == '二' or char == '两':
            ageTemp += 2
            round += 1
        if char == '三':
            ageTemp += 3
            round += 1
        if char == '四':
            ageTemp += 4
            round += 1
        if char == '五':
            ageTemp += 5
            round += 1
        if char == '六':
            ageTemp += 6
            round += 1
        if char == '七':
            ageTemp += 7
            round += 1
        if char == '八':
            ageTemp += 8
            round += 1
        if char == '九':
            ageTemp += 9
            round += 1
        if char == '十':
            if round > 0:
                age += ageTemp/round*10 #这样写是为了例如“二三十岁”，“十五岁”这种情况
                round = ageTemp = 0
            else:
                age += 10
        if char == '百':
            if round > 0:
                age += ageTemp/round*100 #这样写是为了例如“二三十岁”，“十五岁”这种情况
                round = ageTemp = 0
            else:
                age += 100
        if char == '多' or char == '几':
            age += 5
        if char == '岁' and round > 0:
            age += ageTemp/round
    return age.__round__()


def age_group_match(age,line):
    if age == 114514:
        return '?' # 未知年龄，返回?
    if age < 5:
        return '婴儿'
    if age < 12:
        return '儿童'
    if age < 25:
        return '青少年'
    if age < 60:
        return '成年人'
    if age < 150:
        return '老年人'
    return '非人哉！' # 年龄超过150岁，返回非人哉！

read_prologue()



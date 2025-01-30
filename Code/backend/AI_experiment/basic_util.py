from transformers import pipeline
unmasker = pipeline('fill-mask', model='distilbert-base-uncased')
masked_str = str(input("Please input a masked sentence: "))
list = unmasker(masked_str)
# print(list)
i = 0
for sub_dict in list:
    i += 1
    print("Result %d: " %i)
    print("    sequence : ", sub_dict['sequence'])
    print("    score : ", sub_dict['score'])
    print()

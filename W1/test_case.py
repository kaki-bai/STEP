import os
from itertools import permutations


# 辞書を作る
def make_dictionary():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dictionary_path = os.path.join(current_dir, './sorted_words.txt')
    # 辞書を読み込む
    with open(dictionary_path, 'r') as f:
        dictionary = []
        for line in f:
            line = line.rstrip('\n')
            element = eval(line)
            dictionary.append(element)
    return dictionary

dictionary = make_dictionary()
ans = []
i = 0
k = -1
while i < len(dictionary)-2:
    j = i + 1
    if dictionary[i][0] == dictionary[j][0]:
        k += 1
        ans.append([])
        ans[k].append(dictionary[i][1])
        ans[k].append(dictionary[j][1])
        j += 1
        while dictionary[i][0] == dictionary[j][0] and j < len(dictionary)-1:
            ans[k].append(dictionary[j][1])
            j += 1
    i += 1
# for i in range(len(dictionary) - 1):
#     if dictionary[i][0] == dictionary[i+1][0]:
#         if k == -1 or dictionary[i][0] != ans[k][0]:
#             ans.append([])  # 新しい子リストを追加
#             k += 1
#         ans[k].append(dictionary[i][1])
#         ans[k].append(dictionary[i+1][1])

current_dir = os.path.dirname(os.path.abspath(__file__))
example_path = os.path.join(current_dir, './example2.txt')
with open(example_path, 'w') as f:
    for item in ans:
        f.write(str(item) + '\n')

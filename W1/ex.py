import os
from itertools import permutations
# global sorted_dictionary
sorted_dictionary = []
counted_dictionary = []

# wordを読むこむ
def read_word(word_file):
    word_list = []
    with open(word_file) as f:
        for line in f:
            line = line.rstrip('\n')
            word_list.append(line)
    return word_list

# 文字列を列挙する
def permutation_word(word):
    perms = permutations(word)
    permutation_list = [''.join(p) for p in perms]
    permutation_list = list(set(permutation_list))
    return permutation_list

# 文字列をソートする
def sort(word):
    sorted_word = ''.join(sorted(word))
    return sorted_word

# 単語の文字の組み合わせ
def combine_word(word):
    combined_list = ['']
    for char in sorted(word):
        tmp_list = []
        for combined_word in combined_list:
            tmp_list.append(combined_word + char)
        combined_list.extend(tmp_list)
    combined_list = list(set(combined_list))
    combined_list.remove('')
    # if word in combined_list:
    #     combined_list.remove(word)
    return combined_list

# 単語の文字をカウントする
def count_letter(word):
    counts = {}
    for char in sorted(word):
        if char.isalpha():
            if char in counts:
                counts[char] += 1
            else:
                counts[char] = 1
    return counts

# 辞書の単語の文字をカウントする
def count_dictionary(dictionary):
    counted_dictionary = []
    for word in dictionary:
        counted_word = count_letter(word)
        counted_dictionary.append((counted_word, word))
    return counted_dictionary

def sort_word_list(word_list):
    # 辞書をソートする
    sorted_word_list = []
    for word in word_list:
        sorted_word = sort(word)
        sorted_word_list.append((sorted_word, word))
    return sorted_word_list

# score
def word_score(word):
    score_table = {
        'a': 1, 'e': 1, 'h': 1, 'i': 1, 'n': 1, 'o': 1, 'r': 1, 's': 1, 't': 1,
        'c': 2, 'd': 2, 'l': 2, 'm': 2, 'u': 2,
        'b': 3, 'f': 3, 'g': 3, 'p': 3, 'v': 3, 'w': 3, 'y': 3,
        'j': 4, 'k': 4, 'q': 4, 'x': 4, 'z': 4
    }

    score = 0
    for char in word:
        score += score_table.get(char, 0)
    return score

# 最高得点のアナグラム
def find_highest_score_word(word_list):
    highest_score = 0
    highest_word = ''
    for word in word_list:
        score = word_score(word)
        if score > highest_score:
            highest_score = score
            highest_word = word
    return highest_word


# 辞書を作る
def make_dictionary():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dictionary_path = os.path.join(current_dir, './words.txt')
    # 辞書を読み込む
    with open(dictionary_path, 'r') as f:
        dictionary = []
        for line in f:
            line = line.rstrip('\n')
            dictionary.append(line)
    return dictionary

# 二分探索_simple
def binary_search_simple(word_list, sorted_dictionary):
    answer = []
    for word in word_list:
        min = 0
        max = len(sorted_dictionary) - 1
        found = False

        while min <= max:
            mid = (min + max) // 2
            if sorted_dictionary[mid][0] < word:
                min = mid + 1
            elif sorted_dictionary[mid][0] > word:
                max = mid - 1
            else:
                found = True
                min = mid + 1
                break
        
        if found:
            tmp = mid
            while tmp < len(sorted_dictionary) and sorted_dictionary[tmp][0] == word:
                answer.append(sorted_dictionary[tmp][1])
                tmp += 1
            tmp = mid - 1
            while tmp >= 0 and sorted_dictionary[tmp][0] == word:
                answer.append(sorted_dictionary[tmp][1])
                tmp -= 1

    if answer == []:
        return False
    return answer

# anagram_simple
def anagram_simple(word, dictionary, sorted_dictionary):
    combined_list = combine_word(word)

    if sorted_dictionary == []:
        sorted_dictionary = sort_word_list(dictionary)
        sorted_dictionary = sorted(sorted_dictionary, key=lambda x: x[0])

    anagram = binary_search_simple(combined_list, sorted_dictionary)
    return anagram

# 探索_complex
def search_complex(word, word_counts_list, counted_dictionary):
    answer = []
    i = 0
    for dic_counts, dic_word in counted_dictionary:
        answer.append((word,[]))
        if set(dic_counts.keys()).issubset(word_counts_list.keys()):
            for char, count in dic_counts.items():
                if count > word_counts_list[char]:
                    break
            else:
                answer[i][1].append(dic_word)
                continue
    i += 1

    if answer == []:
        return False
    return answer

# anagram_complex
def anagram_complex(word, dictionary, counted_dictionary):
    word_counts_list = count_letter(word)
    if counted_dictionary == []:
        counted_dictionary = count_dictionary(dictionary)
    anagram = search_complex(word, word_counts_list, counted_dictionary)
    return anagram

dictionary = make_dictionary()
current_dir = os.path.dirname(os.path.abspath(__file__))

# mini_file_path = os.path.join(current_dir, './mini.txt')
# mini_word_list = read_word(mini_file_path)

# mini_anagram = {}
# for item in mini_word_list:
#     # print(f'{item}: ')
#     if len(item) <= 13:
#         mini_anagram[item] = anagram_simple(item, dictionary, sorted_dictionary)
#     else:
#         mini_anagram[item] = anagram_complex(item, dictionary, counted_dictionary)
            
#     if mini_anagram[item] == []:
#         print(f"{item}'s anagram not found.")

# mini_highest_anagram_list = []
# for key, values in mini_anagram.items():
#     word = find_highest_score_word(values)
#     mini_highest_anagram_list.append(word)


# small_answer_path = os.path.join(current_dir, './small_answer.txt')
# with open(small_answer_path, 'w') as f:
#     for word in mini_highest_anagram_list:
#         f.write(str(word) + '\n')

small_file_path = os.path.join(current_dir, './small.txt')
small_word_list = read_word(small_file_path)
small_anagram = {}
for item in small_word_list:
    # print(f'{item}: ')
    if len(item) <= 13:
        small_anagram[item] = anagram_simple(item, dictionary, sorted_dictionary)
    else:
        small_anagram[item] = anagram_complex(item, dictionary, counted_dictionary)
            
    if small_anagram[item] == []:
        print(f"{item}'s anagram not found.")

small_highest_anagram_list = []
for key, values in small_anagram.items():
    word = find_highest_score_word(values)
    small_highest_anagram_list.append(word)

small_answer_path = os.path.join(current_dir, './small_answer.txt')
with open(small_answer_path, 'w') as f:
    for word in small_highest_anagram_list:
        f.write(str(word) + '\n')


# medium_file_path = os.path.join(current_dir, './medium.txt')
# medium_word_list = read_word(medium_file_path)
# for item in medium_word_list:
#     # print(f'{item}: ')
#     if len(item) <= 13:
#         anagram_simple(item, dictionary, sorted_dictionary)
#     else:
#         anagram_complex(item, dictionary, counted_dictionary)

# large_file_path = os.path.join(current_dir, './large.txt')
# large_word_list = read_word(large_file_path)
# for item in large_word_list:
#     # print(f'{item}: ')
#     if len(item) <= 13:
#         anagram_simple(item, dictionary, sorted_dictionary)
#     else:
#         anagram_complex(item, dictionary, counted_dictionary)

    # sorted_dictionary_path = os.path.join(current_dir, './sorted_words.txt')
    # with open(sorted_dictionary_path, 'w') as f:
    #     for item in sorted_dictionary:
    #         f.write(str(item) + '\n')
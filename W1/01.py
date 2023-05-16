import os
from itertools import permutations
sorted_dictionary = []
current_dir = os.path.dirname(os.path.abspath(__file__))

# input
def input_word():
    word_list = []
    length = int(input("How many words? "))
    for i in range(length):
        while True:
            try:
                word = str(input(f'word{i+1}: '))
                if not word.isalpha():
                    raise ValueError
                word_list.append(word)
            except ValueError:
                print('Error. Please input a valid word.')
            else:
                break
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

# 辞書をソートする
def sort_dictionary(dictionary):
    sorted_dictionary = []
    for word in dictionary:
        sorted_word = sort(word)
        sorted_dictionary.append((sorted_word, word))
    sorted_dictionary = sorted(sorted_dictionary, key=lambda x: x[0])
    return sorted_dictionary

# 二分探索_simple
def binary_search_simple(word, dictionary):
    min = 0
    max = len(dictionary) - 1
    while min <= max:
        mid = (min + max) // 2
        if dictionary[mid] < word:
            min = mid + 1
        elif dictionary[mid] > word:
            max = mid - 1
        else:
            return dictionary[mid]
    return False

# anagram_simple
def anagram_simple(word, dictionary):
    permutation_list = permutation_word(word)
    permutation_list.remove(word)
    anagram = []
    for word in permutation_list:
        answer = binary_search_simple(word, dictionary)
        if answer:
            anagram.append(answer)
    if anagram == []:
        print("Anagram not found.")
    else:
        print(anagram)
        return 0

# 二分探索_complex
def binary_search_complex(word, sorted_word, dictionary):
    answer = []
    min = 0
    max = len(dictionary) - 1
    found = False

    while min <= max:
        mid = (min + max) // 2
        if dictionary[mid][0] < sorted_word:
            min = mid + 1
        elif dictionary[mid][0] > sorted_word:
            max = mid - 1
        else:
            found = True
            min = mid + 1
            break

    if found:
        tmp = mid
        while tmp < len(dictionary) and dictionary[tmp][0] == sorted_word:
            if dictionary[tmp][1] != word:
                answer.append(dictionary[tmp][1])
            tmp += 1
        tmp = mid - 1
        while tmp >= 0 and dictionary[tmp][0] == sorted_word:
            if dictionary[tmp][1] != word:
                answer.append(dictionary[tmp][1])
            tmp -= 1
    
    if answer == [] or not found:
        return False
    return answer

# anagram_complex
def anagram_complex(word, dictionary, sorted_dictionary):
    sorted_word = sort(word)
    if sorted_dictionary == []:
        sorted_dictionary = sort_dictionary(dictionary)
    anagram = binary_search_complex(word, sorted_word, sorted_dictionary)
    if anagram:
        print(anagram)
    else:
        print("No anagram found.")
    return 0

dictionary = make_dictionary()

word_list = input_word()
for item in word_list:
    print(f'{item}: ')
    if len(item) <= 10:
        anagram_simple(item, dictionary)
    else:
        anagram_complex(item, dictionary, sorted_dictionary)
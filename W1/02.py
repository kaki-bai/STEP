import os
# counted_dictionary = []
current_dir = os.path.dirname(os.path.abspath(__file__))
counted_word_cache = {}
scored_word_cache = {}

# wordを読むこむ
def read_word(word_file):
    word_list = []
    with open(word_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip('\n')
            word_list.append(line)
    return word_list

# 辞書を作る
def make_dictionary():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dictionary_path = os.path.join(current_dir, './dictionary/words.txt')
    # 辞書を読み込む
    dictionary = []
    with open(dictionary_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip('\n')
            dictionary.append(line)
    return dictionary

# 文字列をソートする
def sort(word):
    sorted_word = ''.join(sorted(word))
    return sorted_word

# 辞書をソートする
def sort_word_list(word_list):
    sorted_word_list = []
    for word in word_list:
        sorted_word = sort(word)
        sorted_word_list.append((sorted_word, word))
    return sorted_word_list

# 単語の文字の組み合わせ
def combine_word(word):
    combined_set = set([''])
    for char in sorted(word):
        tmp_set = set()
        for combined_word in combined_set:
            tmp_set.add(combined_word + char)
        combined_set.update(tmp_set)
    combined_set.remove('')
    return list(combined_set)

# 単語の文字をカウントする
def count_letter(word):
    if word in counted_word_cache:
        return counted_word_cache[word]
    
    counts = {}
    for char in sorted(word):
        if char.isalpha():
            if char in counts:
                counts[char] += 1
            else:
                counts[char] = 1
    # カウントした単語を記録する
    counted_word_cache[word] = counts
    return counts

# 辞書の単語の文字をカウントする
def count_dictionary(dictionary):
    counted_dictionary = []
    for word in dictionary:
        counted_word = count_letter(word)
        counted_dictionary.append((counted_word, word))
    return counted_dictionary

# 単語のスコアを出す
def word_score(word):
    if word in scored_word_cache:
        return scored_word_cache[word]
    
    score_table = {
        'a': 1, 'e': 1, 'h': 1, 'i': 1, 'n': 1, 'o': 1, 'r': 1, 's': 1, 't': 1,
        'c': 2, 'd': 2, 'l': 2, 'm': 2, 'u': 2,
        'b': 3, 'f': 3, 'g': 3, 'p': 3, 'v': 3, 'w': 3, 'y': 3,
        'j': 4, 'k': 4, 'q': 4, 'x': 4, 'z': 4
    }
    score = 0
    for char in word:
        score += score_table.get(char, 0)
    # スコアした単語を記録する
    scored_word_cache[word] = score
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
def anagram_simple(word, sorted_dictionary):
    combined_list = combine_word(word)
    answer = binary_search_simple(combined_list, sorted_dictionary)
    return answer




# 探索_complex
def search_complex(word_counts_list, counted_dictionary):
    answer = []
    for dic_counts, dic_word in counted_dictionary:
        if set(dic_counts.keys()).issubset(word_counts_list.keys()):
            for char, count in dic_counts.items():
                if count > word_counts_list[char]:
                    break
            else:
                answer.append(dic_word)
                continue
    if answer == []:
        return False
    return answer

# anagram_complex
def anagram_complex(word, counted_dictionary):
    word_counts_list = count_letter(word)
    anagram = search_complex(word_counts_list, counted_dictionary)
    return anagram

def main(word_file):
    dictionary = make_dictionary()
    sorted_dictionary = []
    counted_dictionary = []
    dic_count = 0
    
    file_path = os.path.join(current_dir, word_file)
    word_list = read_word(file_path)

    anagram = {}
    for item in word_list:
        if len(item) <= 13 and not sorted_dictionary:
            sorted_dictionary = sort_word_list(dictionary)
            sorted_dictionary = sorted(sorted_dictionary, key=lambda x: x[0])
            dic_count += 1
        elif len(item) > 13 and not counted_dictionary:
            counted_dictionary = count_dictionary(dictionary)
            dic_count += 1
            
        if len(item) <= 13:
            anagram[item] = anagram_simple(item, sorted_dictionary)
        else:
            anagram[item] = anagram_complex(item, counted_dictionary)
            
        if anagram[item] == []:
            print(f"{item}'s anagram not found.")

    highest_anagram_list = []
    for key, values in anagram.items():
        word = find_highest_score_word(values)
        highest_anagram_list.append(word)

    print(dic_count)
    return highest_anagram_list

def make_answer_file(answer_file, highest_anagram_list):
    answer_path = os.path.join(current_dir, answer_file)
    with open(answer_path, 'w') as f:
        for word in highest_anagram_list:
            f.write(str(word) + '\n')

# mini_answer = main('./test_case/mini.txt')
# make_answer_file('./answer/mini_answer.txt', mini_answer)

# small_answer = main('./test_case/small.txt')
# make_answer_file('./answer/small_answer.txt', small_answer)

# medium_answer = main('./test_case/medium.txt')
# make_answer_file('./answer/medium_answer.txt', medium_answer)

large_answer = main('./test_case/large.txt')
make_answer_file('./answer/large_answer.txt', large_answer)
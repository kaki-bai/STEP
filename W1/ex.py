def search_complex(word_counts_list, counted_dictionary):
    answer = []

    for dic_counts, dic_word in counted_dictionary:
        for i in range(len(word_counts_list)):
            if dic_counts[i] > word_counts_list[i]:
                print(dic_counts[i], word_counts_list[i])
                break
        else:
            answer.append(dic_word)
            continue

    print(answer)
    if not answer:
        return False
    return answer

# 単語の文字をカウントする
def count_letter(word):
    counts = [0] * 26
    for char in sorted(word):
        if char.isalpha():
            index = ord(char.lower()) - ord('a')
            counts[index] += 1
    return counts

def count_dictionary(dictionary):
    counted_dictionary = []
    for word in dictionary:
        counted_word = count_letter(word)
        counted_dictionary.append((counted_word, word))
    return counted_dictionary

word_counts_list = count_letter('aabbccc')
counted_dictionary = count_dictionary(['aa', 'ab','ad'])
search_complex(word_counts_list, counted_dictionary)



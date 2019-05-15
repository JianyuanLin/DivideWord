#encoding:utf-8
import math
import re


def DivideWord(text_path, result_path, vocab_path, word_size=5, freq_threshold=0.0001, co_threshold=0.99999, free_threshold=0.99999):
    if word_size <= 1:
        print("word size can't be 1 or less!")
        exit()
    pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'
    with open(text_path, encoding="utf8") as f:
        lines = f.readlines()
    sentences = []
    for line in lines:
        ll = line.strip()
        sentences += re.split(pattern, ll)
    with open("./temp.txt", "w", encoding="utf8") as f:
        for s in sentences:
            f.write(s+"\n")
    with open("./temp.txt", encoding="utf8") as f:
        lines = f.readlines()
    word_freq = {}
    word_left = {}
    word_right = {}
    word_num = 0
    # count the numbers of every word
    all_num = len(lines)
    for length in range(1, word_size + 1):
        for _, line in enumerate(lines):
            print("Get the word whose length is "+str(length)+"..."+str(_/all_num*100)+"%")
            string = line.strip()
            string_length = len(string)
            for i in range(string_length - length + 1):
                word = string[i:i + length]
                word_num += 1
                if word not in word_freq.keys():
                    word_freq[word] = 1
                    word_left[word] = {}
                    word_right[word] = {}
                    if i != 0:
                        word_left[word][string[i - 1]] = 1
                    if i + length < string_length:
                        word_right[word][string[i + length]] = 1
                else:
                    word_freq[word] += 1
                    if i != 0:
                        lw = string[i - 1]
                        if lw not in word_left[word]:
                            word_left[word][lw] = 1
                        else:
                            word_left[word][lw] += 1
                    if i + length < string_length:
                        rw = string[i + length]
                        if rw not in word_right[word]:
                            word_right[word][rw] = 1
                        else:
                            word_right[word][rw] += 1
    # calculate the freq of every word and generate word_dict1
    word_dict1 = []
    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / word_num
        if word_freq[word] > freq_threshold:
            word_dict1.append(word)
    # calculate the co of every word in word_dict1 and generate word_dict2
    word_dict2 = []
    for word in word_dict1:
        length = len(word)
        if length > 1:
            co = min(
                [word_freq[word] / word_freq[word[:index]] / word_freq[word[index:]]
                 for index in range(1, length)]
            )
            if co > co_threshold:
                word_dict2.append(word)
        else:
            word_dict2.append(word)
    # calculate the free of every word in word_dict2 and generate word_dict3
    word_dict3 = []
    for word in word_dict2:
        left_num = 0
        left_h = 0
        for lw in word_left[word]:
            left_num += word_left[word][lw]
        for lw in word_left[word]:
            p = word_left[word][lw] / left_num
            left_h -= p * math.log(p)
        right_num = 0
        right_h = 0
        for rw in word_right[word]:
            right_num += word_right[word][rw]
        for rw in word_right[word]:
            p = word_right[word][rw] / right_num
            right_h -= p * math.log(p)
        free = min(left_h, right_h)
        if free > free_threshold:
            word_dict3.append(word)
    result_dict = {}
    for word in word_dict3:
        result_dict[word] = word_freq[word]
    with open(vocab_path, "w", encoding="utf8") as f:
        for word in sorted(result_dict, key=result_dict.__getitem__, reverse=True):
            if len(word) > 1:
                f.write(word+"\n")
    with open(result_path, "w", encoding="utf8") as f:
        index = 0
        for line in lines:
            index += 1
            words = []
            string = line.strip()
            length = len(string)
            start = 0
            end = word_size
            while True:
                if start >= length:
                    break
                if end > length:
                    end = length
                if string[start:end] in word_dict3:
                    words.append(string[start:end])
                    start = end
                    end = start + word_size
                else:
                    end -= 1
                    if end - start <= 1:
                        words.append(string[start])
                        start += 1
                        end = start + word_size
            for word in words:
                f.write(word+" ")
            f.write("\n")

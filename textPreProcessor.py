from email.errors import FirstHeaderLineIsContinuationDefect
import re
from xml.dom.pulldom import SAX2DOM

def read_string(file_name):
    f = open(file_name, "r")
    text = f.readlines()
    f.close()
    return "\n".join(text)

def remove_punctuation(my_str, puncts):
    str_no_puncts = ""
    for c in my_str:
        if c in puncts:
            str_no_puncts += ""
            continue
        str_no_puncts += c
    my_str = str_no_puncts
    return my_str

def remove_stopwords(my_str, stopwords):
    list_without_stopwords = [word for word in my_str.split(" ") if word not in stopwords]
    my_str = " ".join(list_without_stopwords)
    return my_str

def remove_prefix(my_str, prefix_to_remove):
    my_str = " ".join(
        [word for word in my_str.split(" ") if not any([word.startswith(phrase) for phrase in prefix_to_remove])])
    return my_str


def remove_oov(my_str, min_count, oov):
    words = my_str.split(" ")
    final_ans_list = []
    word_count = {}
    for w in words:
        word_count[w] = word_count.get(w, 0) + 1
    final_ans_list += [word if word_count[word] >= min_count else oov for word in words]
    my_str = " ".join(final_ans_list)
    return (my_str)

def remove_spaces(my_str):
    my_str = re.sub(" +", " ", my_str)
    my_str = my_str.strip(" ")
    return my_str

def clean_text(my_str, puncts_to_remove, stop_words, min_count, oov, prefix_to_remove):
    my_str = my_str.lower()
    my_str = remove_punctuation(my_str, puncts_to_remove)
    my_str = remove_stopwords(my_str, stop_words)
    my_str = remove_prefix(my_str, prefix_to_remove)
    my_str = remove_oov(my_str, min_count, oov)
    my_str = remove_spaces(my_str)
    return my_str

def get_word2count(my_str):
    word2count_dict = {}
    for word in my_str.split(" "):
        word2count_dict[word] = word2count_dict.get(word, 0) + 1
    return word2count_dict

def get_count2words(my_str):
    count2words_dict = {}
    word2count_dict = get_word2count(my_str)
    for k, v in word2count_dict.items():
        count2words_dict.setdefault(v, []).append(k)
    return count2words_dict

def top_n_words(n, count2words_dict):
    popular_words = []
    for value in sorted(count2words_dict.keys(), reverse=True):
        popular_words.append(count2words_dict[value])
    popular_words = sum(popular_words, [])
    popular_words = popular_words[0:n]
    return popular_words

def compare_texts(n, text_path1, text_path2):
    text1 = read_string(text_path1)
    text2 = read_string(text_path2)
    puncts_to_remove = ["\t", "\n", "~", "{", "|", "}", "`", "_", "^", "[", "\\", "]", "@", "?", "<", "=", ">", ";",
                        ":", "/", ".", "-", ",", "+", "*", "(", ")", "&", "%", "$", "#", '"', "!"]
    stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "you're", "you've",
                        "you'll", "you'd", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself",
                        "she", "she's", "her", "hers", "herself", "it", "it's", "its", "itself", "they", "them",
                        "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "that'll",
                        "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "a", "an", "the",
                        "and", "but", "if", "or", "because", "as", "until", "while", "of", "by", "for", "with", "about",
                        "against", "between", "into", "through", "during", "before", "after", "above", "below", "to",
                        "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then",
                        "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few",
                        "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so",
                        "than", "too", "very", "s", "t", "can", "will", "just", "don", "don't", "should", "should've",
                        "now", "d", "ll", "m", "o", "re", "ve", "y", "ain", "aren", "aren't", "couldn", "couldn't",
                        "didn", "didn't", "doesn", "doesn't", "hadn", "hadn't", "hasn", "hasn't", "haven", "haven't",
                        "isn", "isn't", "ma", "mightn", "mightn't", "mustn", "mustn't", "needn", "needn't", "shan",
                        "shan't", "shouldn", "shouldn't", "wasn", "wasn't", "weren", "weren't", "won", "won't",
                        "wouldn", "wouldn't", "at", "has", "had", "have", "did", "do"]
    min_count = 3
    oov = "changed"
    prefix_to_remove = ["well"]
    text1 = clean_text(text1, puncts_to_remove, stop_words, min_count, oov, prefix_to_remove)
    text2 = clean_text(text2, puncts_to_remove, stop_words, min_count, oov, prefix_to_remove)
    text1_dict = get_count2words(text1)
    text2_dict = get_count2words(text2)
    text1_top_n_words = top_n_words(n, text1_dict)
    text2_top_n_words = top_n_words(n, text2_dict)
    count = 0
    for word in text1_top_n_words:
        if word in text2_top_n_words:
            count += 1
    return count

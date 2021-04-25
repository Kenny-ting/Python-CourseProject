from turtle import pd

import jieba


def word_count(data):
    """
    词频统计
    """
    txt = ""
    for i in data:
        txt += str(i)
    # 加载停用词表
    stopwords = [line.strip() for line in open("cn_stopwords.txt", encoding="utf-8").readlines()]
    words = jieba.lcut(txt)
    counts = {}
    for word in words:
        # 不在停用词表中
        if word not in stopwords:
            # 不统计字数为一的词
            if len(word) == 1:
                continue
            else:
                counts[word] = counts.get(word, 0) + 1

    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)

    return items

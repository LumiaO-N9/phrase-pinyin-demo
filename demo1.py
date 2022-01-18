"""
pip install jieba pypinyin
"""
from pypinyin import Style, pinyin, load_phrases_dict
import itertools
import jieba
import logging

jieba.setLogLevel(logging.INFO)  # 关闭jieba分词器日志打印


# 加载中文停用词 用于jieba分词
# 作用：用于去除标点符号
def get_stop_words(path):
    with open(path, mode='r', encoding='utf8') as f:
        strip_word_list = [word.strip() for word in f.readlines()]
        return strip_word_list


# 自定义拼音词典
phrases_dict = {
    '行长': [['háng'], ['zhǎng']],
}

INPUT_PATH = 'data/input/input1.txt'
OUTPUT_PATH = 'data/output/output.txt'
STOP_WORDS_PATH = 'data/stop_words.txt'
with open(INPUT_PATH, mode='r', encoding='utf8') as ip:
    with open(OUTPUT_PATH, mode='w', encoding='utf8') as op:
        # 加载停用词
        stop_words_list = get_stop_words(STOP_WORDS_PATH)
        print("加载停用词")

        # 加载自定义拼音
        load_phrases_dict(phrases_dict)
        print("加载自定义拼音")

        print("#" * 20)
        line = ip.readline().strip()

        print("开始处理")
        while line:
            # print(line)
            text = line.split(" ")[1]
            cut_res_iter = jieba.cut(text)
            words = []
            for word in cut_res_iter:
                # 过滤标点符号
                if word not in stop_words_list:
                    words.append(word)
            # 分词结果
            # print(words)
            result = " ".join(list(itertools.chain.from_iterable(pinyin(words, style=Style.TONE3))))
            op.write(line + '\n')
            op.write('\t')
            op.write(result + '\n')
            line = ip.readline().strip()
        print("处理完成，结果保存在data/output/output.txt文件中")

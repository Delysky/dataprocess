# _*_coding:utf-8_*_
# author: tiantianSaveWorld
# time: 18-11-2 上午9:44
# E-mail: zengdetian@eefung.com
'''

Describle: 数据预处理的相关强有力工具
 
'''
import re
import jieba
import matplotlib
import matplotlib.pyplot as plt
import random
import os

def emoji_filter(source_str):
    '''去除文字中的相关表情'''
    try:
        # python UCS-4 build的处理方式
        highpoints = u'[\U00010000-\U0010ffff]'
        result_str = re.sub(u'[\U00010000-\U0010ffff]', '', source_str)
    except re.error:
        # python UCS-2 build的处理方式
        highpoints = u'[\uD800-\uDBFF][\uDC00-\uDFFF]'
        result_str = re.sub(highpoints, '', source_str)
    # 返回去除表情后的字符串
    return result_str


def special_filter(source_str, del_singal, rep_singal):
    '''去除某一特殊符号，如@'''
    return source_str.replace(del_singal, rep_singal)


def url_filter(message):
    '''去除文本中的url'''
    results = re.sub("(?isu)((http|https)\://[a-zA-Z0-9\.\?/&\=\:]+)", '', message)
    p = re.compile('<[^>]+>')
    res = p.sub("", results)
    return res


def static_text_lenght(path, flag='char', xlen=3000, ylen=15000):
    '''统计一个文本中中字符长度或词的长度,画频率直方图'''
    num_words = []

    with open(path, "r", encoding='utf-8') as f:
        for res in f.readlines():
            # mess = line.split('\t')
            # res = mess[1]
            if flag == 'char':
                counter = len(res)
            elif flag == 'word':
                contents = jieba.cut(res)
                counter = len(list(contents))
            num_words.append(counter)
    print(num_words)
    print('所有的字（词）的数量', sum(num_words))
    print('平均文件字（词）的长度', sum(num_words) / len(num_words))

    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['font.family'] = 'sans-serif'
    # %matplotlib inline
    plt.hist(num_words, 20, facecolor='g')
    plt.xlabel('lenght of text')
    plt.ylabel('frequent')
    plt.axis([0, xlen, 0, ylen])
    plt.show()


def static_rate_of_diff_part(path, label):
    '''统计一个文本中两个类别的个数及比列'''
    count = 0
    count1 = 0
    # 查看训练数据中的类别比列
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            hang = line.split('\t')
            if hang[0] == label:
                count += 1
            else:
                count1 += 1
    print(label, ' count is', count)
    print('the other is', count1)
    print("the rate is=", float(count) / count1)


def shuffle_text_in_file(path):
    '''打乱文本中每一行的顺序，并将所有的行以列表的形式返回'''
    with open(path, 'r', encoding='utf-8') as f:
        # 打乱文本的顺序
        lists = f.readlines()
        random.shuffle(lists)
    return lists


def meet_format_of_fasttext(source_str):
    '''将文本切词后转换维fasttext的格式，后面需要自己加实际的标签'''
    words = jieba.cut(source_str.strip())
    res = ' '.join(words)
    result = res + '    \t__label__'
    return result


def static_lenght_of_text(path):
    '''统计文本的行数'''
    with open(path, mode='r', encoding='utf-8') as f:
        print('文本的行数：' + str(len(f.readlines())))


def split_the_text_to_three(source_text, train, percent1, val, percent2, test):
    '''将一个文本中的行数按比例分割成为train val test三个部分'''
    f1 = open(train, mode='w', encoding='utf-8')
    f2 = open(val, mode='w', encoding='utf-8')
    f3 = open(test, mode='w', encoding='utf-8')

    with open(source_text, mode='r', encoding='utf-8') as f:
        contents = f.readlines()
        random.shuffle(contents)     # 打乱文本的顺序
        for i, line in enumerate(contents):
            if i < len(contents)*percent1:
                f1.write(line)
            elif i < len(contents)*(percent1+percent2):
                f2.write(line)
            else:
                f3.write(line)

    # close the file
    f1.close()
    f2.close()
    f3.close()
    # show the lenght of text
    print('训练集')
    static_lenght_of_text(train)
    print('验证集')
    static_lenght_of_text(val)
    print('测试集')
    static_lenght_of_text(test)


def list_file_of_dir(path):
    '''列举某一文件夹下的所有文件名'''
    files = os.listdir(path)
    print('此文件夹下文件的数量为：', len(files))
    for file in files:
        print(file)
    print('列举完毕！')






'''unit test'''

if __name__ == '__main__':
    # split_the_text_to_three('/media/tian/备份/updown/corpus_CNN.txt', 'cnn_train', 0.7, 'cnn_val', 0.1, 'cnn_test')

    # static_text_lenght('/media/tian/备份/updown/corpus.train.txt', xlen=200 , flag='char', ylen=40000)
    pass
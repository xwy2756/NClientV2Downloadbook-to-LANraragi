import copy
import re


def FormattingTag(totag: str, tagfile: str):
    """
    更新本地文件中的tag翻译表
    :param totag: 总tag
    :param tagfile: 存放tag翻译的文件
    :return:
    """
    tag = re.sub(r"[\[\]']+", "", str(totag), 0)  # 删除多余字符
    tag = tag.split(', ')   # 把所有tag从字符串变成列表

    #   判断本地tag翻译表中是否有内容
    with open(tagfile, mode='r', encoding="utf-8") as file:
        f = file.readlines()

    #  截取不需要的字符
    f = f[1:-1]
    for i in range(len(f)):
        f[i] = f[i][3:-2]

    # 拷贝变量
    content = copy.copy(f)
    tagcopy = copy.copy(tag)

    #  找出是否有更新的tag
    for i in range(len(tag)):
        for j in f:
            if tag[i] == re.search(r'(?<=\').*?(?=\')', j).group(0):
                tagcopy.remove(tag[i])
    for i in tagcopy:
        content.append(' \'' + i + '\'' + ': ' + 'None')
    con = 'TagDictionaries = { \n'

    # 把整理好地翻译列表写入文件
    for i in content:
        con = con + '    ' + i + ',\n'
    con = con + '}'
    with open(tagfile, mode='w', encoding="utf-8") as file:
        file.write(con)


def Translate(origintag: str, tagfile):
    #   读取本地tag翻译表
    with open(tagfile, mode='r', encoding="utf-8") as file:
        f = file.readlines()

    #  截取不需要的字符
    f = f[1:-1]
    for i in range(len(f)):
        f[i] = f[i][3:-2]

    # 从本地tag翻译表中找到tag对应的翻译
    for i in f:
        if origintag == re.search(r'(?<=\').*?(?=\')', i).group(0):
            try:
                return re.search(r'(?<=: \').*?(?=\')', i).group(0)
            except AttributeError:
                return None
    return None


if __name__ == '__main__':
    pass


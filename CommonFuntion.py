import fnmatch
import hashlib
import os
import re


def GetDirList(path: str, mode: str):
    """
    1.获取指定文件夹下的子目录并返回由所有子目录构成的列表

    :param path: {str} 指定目录路径
    :param mode: {str} 操作模式 【dir:仅文件夹, file:仅文件, any:任意,】
    :return: {list} path下子目录构成的列表
    """
    try:
        if mode == 'dir':
            dirlist = os.listdir(path)
            retlist = []
            # 遍历整个dirlist元素，如果不是文件夹则跳过
            for n in dirlist:
                if os.path.isdir(path + '\\' + n):
                    retlist.append(n)
            return retlist
        if mode == 'file':
            dirlist = os.listdir(path)
            retlist = []
            # 遍历整个dirlist元素，如果不是文件则跳过
            for n in dirlist:
                if os.path.isfile(path + '\\' + n):
                    retlist.append(n)
            return retlist
        if mode == 'any':
            dirlist = os.listdir(path)
            return dirlist
    except FileNotFoundError:
        print('请输入正确路径')


def GetDirTime(path: str):
    """
    1.获取文件夹的上次修改时间

    :param path: {str} 指定的文件夹或者文件
    :return: {str} path的修改时间
    """
    #   如果path是文件则直接获取，否则找到001文件并获取它的时间
    if os.path.isfile(path):
        date = os.stat(path)
        t = re.search(r"(?<=st_mtime=).*?(?=,)", str(date))
    else:
        dirlist = GetDirList(path, 'file')
        file = ""
        for i in dirlist:  # 找到001文件
            if fnmatch.fnmatch(i, '*1.*'):
                file = i
                break
        date = os.stat(path + "\\" + file)
        # date = os.stat(path)
        # 返回001文件的时间信息
        t = re.search(r"(?<=st_mtime=).*?(?=,)", str(date))
    return t.group()


def Getid(pathlist: list):
    """
    获取本子id
    :param pathlist: 文件路径
    :return: {str} id
    """
    try:
        t1 = re.search(r"\.\d*", str(pathlist)).group(0)
        t2 = re.search(r"\d.*", t1).group(0)
        return t2
    except AttributeError:
        return ""


def GetMd5(file: str):
    """
    获取文件md5值
    :param file: 文件
    :return: {str} file的md5值
    """
    md = hashlib.md5()
    with open(file, 'rb') as f:
        md.update(f.read())
    return md.hexdigest()


if __name__ == '__main__':
    pass

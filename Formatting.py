import fnmatch
import multiprocessing
import os
import re

import CommonFuntion
import main
import TranslateTag

from multiprocessing import Manager
from multiprocessing import Process


def FindBackupFile(dirpath: str):
    """
    从指定目录中找到最新的备份文件，并返回备份文件对象
    :param dirpath: {str} 备份文件所在目录
    :return: {fileObj} 备份文件对象
    """
    tmp = CommonFuntion.GetDirList(dirpath, 'file')
    BackupFile = []
    #   遍历目标目录找到所有的备份文件
    try:
        for i in tmp:
            if fnmatch.fnmatch(i, 'backup*.json'):
                BackupFile.append(i)
        for i in range(0, len(BackupFile) - 1):
            if CommonFuntion.GetDirTime(dirpath + '\\' + BackupFile[i]) > CommonFuntion.GetDirTime(dirpath + '\\' + BackupFile[i + 1]):
                BackupFile[i], BackupFile[i + 1] = BackupFile[i + 1], BackupFile[i]
        BackupFileObj = open(dirpath + '\\' + BackupFile[-1], mode='r+', encoding='UTF-8')
    except:
        print('没有在文件夹中找到备份文件,这可能是文件名错误或文件夹不存在')
        return None
    return BackupFile[-1]


def CutBackupFile(BackFileContent: str):
    """
    处理备份文件内容，使其变成可被遍历的列表
    :param BackFileContent: {str}备份文件内容
    :return: {List[2]} 二维列表{内容，开头字符，结尾字符，内容中开头字符，内容中结束字符}
    """
    front = re.search(".*?(?=\\[\\{)", BackFileContent).group(0)  # 备份文件开头不需要的字符
    end = re.search("(?<=}]).*", BackFileContent).group(0)  # 备份文件结尾不需要的字符
    content = re.search("(?<=" + re.escape(front) + ")" + ".*?(?=" + re.escape(end) + ")", BackFileContent).group(0)  # 备份文件中需要被处理的内容
    content = content.strip("[")  # 删除内容开头多余的中括号
    content = content[:-1]  # 删除内容结尾多余的中括号
    contentlist = []
    contentlist = content.split('},')
    # 把内容分割成一个个可编辑的元素
    for i in range(len(contentlist)):
        if i != len(contentlist) - 1:
            contentlist[i] = contentlist[i] + '}'
    # while re.search("(?={).*?(?<=})", content):
    #     contentlist.append(re.search("(?={).*?(?<=})", content).group(0))
    #     content = re.sub(r'(?={).*?(?<=})', "", content, 1)
    # 汇总结果到一个二维列表 returnlist[内容，开头字符，结尾字符，内容中开头字符，内容中结束字符]
    returnlist = [[], [], [], [], []]
    returnlist[0], returnlist[1], returnlist[2], returnlist[3], returnlist[4] = contentlist, front, end, "[", "]"
    return returnlist


def FindBookName(bookname: str, contenname: str):
    """
    在contenname中找到bookname
    :param bookname: 本
    :param contenname:
    :return:
    """
    #   从contenname中匹配bookname
    contenname = re.search("(?<=\"filename\":\").*?(?=\",\"tags\")", contenname).group(0)
    if contenname == re.search("(?<={).*?(?=:)", str(bookname)).group(0) or contenname == re.search("(?<=:).*?(?=})", str(bookname)).group(0):
        return re.search("(?<={).*?(?=:)", str(bookname)).group(0)
    else:
        return False


def GetNomediaContent(nomediapath: str):
    """
    1.获取.nomedia文件的内容

    :param nomediapath: {str} .nomedia的路径
    :return: {str} .nomedia的内容
    """
    try:
        file = open(nomediapath, mode='r', encoding='UTF-8')
        filecontent = file.readline()
        file.close()
        return filecontent
    except FileNotFoundError:
        return "没有找到有效nomedia文件"


def GetTag(nomedia: str, bookid: str, time: str, alltaglist: list, tagfilename: str):
    """
    1.解析nomedia内容并返回整理过后的tag列表

    :param nomedia: {str}   nomedia内容
    :param bookid: {str}    本子id
    :param time: {str}  时间戳
    :param alltaglist:  {list} 所有Tag列表
    :param tagfilename {str}  Tag翻译表的名字
    :return: {str}整理后的tag
    """

    # 获取每一个tag集到一个列表
    taglist = []
    # 如果nomedia里面有有效内容则提取tag，没有则只添加时间戳和id
    if re.search(r'(?=\"tags\":).*(?=})', nomedia):
        tag = re.search(r'(?=\"tags\":).*(?=})', nomedia).group(0)[7:]  # 提取tag
        tag = re.sub(r"[\[\]']+", "", str(tag), 0)  # 删除多余字符

        #   提取tag中的tag组
        while re.search(r'(?={).*?(?=})', tag):
            taglist.append(re.search(r'(?={).*?(?=})', tag).group(0))
            tag = re.sub(r'(?={).*?(?=})', "", tag, 1)

        #   格式化提取出的tag组
        for i in range(len(taglist)):
            #   汇总所有本子中的tag
            if re.search(r"(?<=\"type\":\").*?(?=\")", taglist[i]).group(0) == 'tag':
                try:
                    alltaglist.index(re.search(r"(?<=\"name\":\").*?(?=\")", taglist[i]).group(0))
                except ValueError:
                    alltaglist.append(re.search(r"(?<=\"name\":\").*?(?=\")", taglist[i]).group(0))

                tmp = TranslateTag.Translate(re.search(r"(?<=\"name\":\").*?(?=\")", taglist[i]).group(0), tagfilename)
                if tmp is not None:
                    taglist[i] = re.search(r"(?<=\"type\":\").*?(?=\")", taglist[i]).group(0) + ":" + tmp
                else:
                    taglist[i] = re.search(r"(?<=\"type\":\").*?(?=\")", taglist[i]).group(0) + ":" + re.search(r"(?<=\"name\":\").*?(?=\")", taglist[i]).group(
                        0)
            else:
                #  格式化提取出的tag组
                taglist[i] = re.search(r"(?<=\"type\":\").*?(?=\")", taglist[i]).group(0) + ":" + re.search(r"(?<=\"name\":\").*?(?=\")", taglist[i]).group(0)
        taglist.append("date_added" + ":" + time)
        taglist.append("id" + ":" + bookid)
        taglist = str(taglist)
        taglist = re.sub(r"[\[\]']+", "", taglist, 0)
        return taglist
    else:
        taglist.append("date_added" + ":" + time)
        taglist.append("id" + ":" + bookid)
        taglist = str(taglist)
        taglist = re.sub(r"[\[\]']+", "", taglist, 0)
        return taglist


def Recode(content: str, serial: str, tag: str, title: str):
    """
    解析Lrr备份文件并写入nhtag信息

    :param content: 备份文件属性组
    :param serial: nh打包文件的文件名(不包括后缀
    :param tag: nh本子tag
    :param title: nh本子标题
    :return: {list} 重新写好的元素
    """
    regex = '"(?<=\\"filename\\":\\"' + serial + '\\",\\"tags\\":\\")' + '.*?(?=\\",\\"thumbhash\\":)"'
    content = re.sub(regex, '"' + tag + '"', content, 1)
    content = re.sub(r"(?<=\"title\":\").*?(?=\"})", title, content, 1)
    return content


def RecodeWorkThread(booklist: list, contentlist: list, donelist: list, taglist: list, booksourcedir: str, takelist: list, errlist: list, tagfilename):
    for i in contentlist:
        for j in booklist:
            name = FindBookName(j, i)  # 获取本子名
            if name:
                takelist.append("正在处理" + " " + "“" + "\033[1;36m " + name + "\033[0m" + "”")
                bookdir = booksourcedir + '\\' + name
                nomediacontent = GetNomediaContent(bookdir + '\\' + '.nomedia')
                bookid = CommonFuntion.Getid(CommonFuntion.GetDirList(bookdir, 'any'))
                dirtime = CommonFuntion.GetDirTime(bookdir)
                tag = GetTag(nomediacontent, bookid, dirtime, taglist, tagfilename)

                if os.path.isfile(bookdir + '\\' + '.nomedia'):
                    if nomediacontent is not None:
                        donelist.append(Recode(i, re.search("(?<=:).*?(?=})", str(j)).group(0), tag, name))
                    else:
                        donelist.append(Recode(i, re.search("(?<=:).*?(?=})", str(j)).group(0), tag, name))
                        errlist.append("\033[1;31m 没有在  \"" + "\033[1;36m " + name + "\"  \033[1;31m 的.nomedia文件中找到有效内容只能添加时间戳和idTag")

                else:
                    donelist.append(Recode(i, re.search("(?<=:).*?(?=})", str(j)).group(0), tag, name))
                    errlist.append("\033[1;31m 没有找到  \"" + "\033[1;36m " + name + "\"  \033[1;31m 的.nomedia文件，只能添加时间戳和idTag")


def WriteBackupFile(content: str, filepath: str):
    """
    保存修改后的内容到备份文件
    :param content: 修改后的备份内容
    :param filepath: 备份文件路径
    :return:
    """
    file = open(filepath, mode='w+', encoding='utf-8')
    file.write(content)
    file.close()


def StartRecode(booklist: list, sourcepath: str, backupfilepath: str, thread: int, tagfile: str):
    """
    编码备份文件任务启动函数
    :param booklist:    本子列表
    :param sourcepath: 文件夹源路径
    :param backupfilepath: 备份文件存放路径
    :param thread: 线程数
    :param tagfile tag翻译文件名
    :return:
    """
    #   获取线程数
    # if thread != multiprocessing.cpu_count():
    #     thread = thread * 2
    #     if thread > multiprocessing.cpu_count():
    #         thread = multiprocessing.cpu_count()
    # 判断是否有备份文件
    i = ''
    while True:
        BackFilename = FindBackupFile(backupfilepath)  # 获取备份文件名
        if BackFilename is None:
            print('请在指定的备份文件夹中放入备份文件，确认无误后请输入 ok，如要退出请输入 exit')
            i = input("指令: ")
        if i == 'exit':
            return
        if BackFilename is not None:
            break

    # 判断备份文件时候有内容
    i = ''
    while True:
        BackFilename = FindBackupFile(backupfilepath)  # 获取备份文件名
        BackFile = open(backupfilepath + '\\' + BackFilename, mode='r+', encoding='UTF-8')
        BackFileContent = BackFile.readline()  # 获取备份文件对象
        if BackFileContent == '':
            print('备份文件里面没有内容,请检查备份文件，确认无误后请输入 ok，如要退出请输入 exit')
            BackFile.close()
            i = input("指令: ")
        if i == 'exit':
            BackFile.close()
            return
        if BackFileContent != '':
            BackFile.close()
            break

    recodeMM = Manager()  # 获取多线程变量实例
    BackFileContent = CutBackupFile(BackFileContent)  # 格式化备份文件

    # 检测备份文件更新状态
    i = ''
    while True:
        if len(BackFileContent[0]) != len(booklist):
            print('备份文件文件内本子数量: ' + str(len(BackFileContent[0])) + '   ' + '本地本子数量: ' + str(len(booklist)))
            print('备份文件元素数和本子数量不一致，请检查是否拉取了最新的备份文件，如果已经拉取请输入 ok ，如果想跳过请输入 skip, 退出请输入 exit')
            i = input("指令: ")
            BackFilename = FindBackupFile(backupfilepath)  # 获取备份文件名
            BackFile = open(backupfilepath + '\\' + BackFilename, mode='r+', encoding='UTF-8')
            BackFileContent = BackFile.readline()  # 获取备份文件对象
            BackFile.close()
            BackFileContent = CutBackupFile(BackFileContent)  # 格式化备份文件
        if i == 'exit':
            return
        if len(BackFileContent[0]) == len(booklist) or i == 'skip':
            break

    Content = main.DistributionBucket(BackFileContent[0], thread)  # 分割备份文件内容

    # 根据线程数启动对应数量的进程
    recodetaskbarlist = recodeMM.list()  # 共享进度条
    recodeerrorlist = recodeMM.list()  # 共享错误列表
    recodedonelist = recodeMM.list()  # 重编码完成后的列表
    Taglist = recodeMM.list()

    recodeprocessList = []  # 进程列表
    print('处理备份文件中....')
    for i in range(thread):
        if i == 0:  # 如果是第一次循环则启动进度条子进程
            recodetaskthread = Process(target=main.Task, args=(len(booklist), recodetaskbarlist,))
            recodetaskthread.start()
            recodeprocessList.append(recodetaskthread)
        recodethreaad = Process(target=RecodeWorkThread,
                                args=(booklist, Content[i], recodedonelist, Taglist, sourcepath, recodetaskbarlist, recodeerrorlist, tagfile))
        recodethreaad.start()
        recodeprocessList.append(recodethreaad)
    # RecodeWorkThread(booklist, Content[0], recodedonelist, sourcepath, recodetaskbarlist, recodeerrorlist)
    for i in recodeprocessList:
        i.join()

    #   写入tag
    TranslateTag.FormattingTag(str(Taglist), tagfile)

    # 重混合内容
    BackFileTxt = str()
    for i in range(len(recodedonelist)):
        BackFileTxt = BackFileTxt + recodedonelist[i]
        if i != len(recodedonelist) - 1:
            BackFileTxt = BackFileTxt + ','
    BackFileTxt = BackFileContent[1] + BackFileContent[3] + BackFileTxt + BackFileContent[4] + BackFileContent[2]
    WriteBackupFile(BackFileTxt, backupfilepath + '\\' + FindBackupFile(backupfilepath))
    return recodeerrorlist


if __name__ == '__main__':
    pass

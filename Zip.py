import fnmatch
import os
import re
import shutil
import zipfile

import CommonFuntion
import main

from multiprocessing import Manager
from multiprocessing import Process


def ZipPack(path: str, basepath: str, name: str, t: str):
    """
    1.压缩指定目录(不包括路径）内容

    2.修改压缩文件的创建时间和修改时间和原目录修改时间一致

    :param path: {str} 压缩文件存放目录
    :param basepath: {str} 原文件目录
    :param name: {str} 压缩文件名
    :param t: {str} 原目录修改时间
    :return: None
    """
    # time.sleep(random.uniform(0.01, 0.3))
    with zipfile.ZipFile(path + '\\' + name + '.zip', 'w') as Zip:
        if os.path.isdir(basepath):
            for i in CommonFuntion.GetDirList(basepath, 'any'):  # 遍历添加目录下的文件给压缩包
                Zip.write(basepath + '\\' + i, arcname=i)
        else:
            Zip.write(basepath, arcname=name)
    os.utime(path + '\\' + name + '.zip', (int(t), int(t)))  # 处理压缩完成后文件的修改时间


def ZipWorkThread(sourcepath: str, targetpath: str, ziplist: list, thread: int, tasklist: list, errlist: list):
    """
    把本子目录打包为压缩包并更改压缩包名称
    :param sourcepath: 文件夹源路径
    :param targetpath: 压缩包存放路径
    :param ziplist: 需要压缩的文件夹列表
    :param thread:  线程数
    :param tasklist:    任务进度
    :param errlist:   错误列表
    :return:
    """
    task = 1
    for i in ziplist:
        # tasklist.append("总共" + "\033[1;34m " + str(listlength) + "\033[0m" + "个任务,当前进度第" + "\033[1;35m " + str(task) + "\033[0m" + "个任务," + "正在处理文件夹" + " " + "“" + "\033[1;36m " + re.search("(?<={).*?(?=:)", str(i)).group(0) + "\033[0m" + "”")
        tasklist.append("正在处理文件夹" + " " + "“" + "\033[1;36m " + re.search("(?<={).*?(?=:)", str(i)).group(0) + "\033[0m" + "”")
        task = task + 1
        tmpdir = sourcepath + '\\' + re.search("(?<={).*?(?=:)", str(i)).group(0)  # 确定本子源文件夹
        #  如果压缩包已经存在，则对比md5值判断是否需要重新压缩，不存在则直接压缩
        if os.path.isfile(targetpath + '\\' + re.search("(?<=:).*?(?=})", str(i)).group(0) + ".zip"):
            with zipfile.ZipFile(targetpath + '\\' + re.search("(?<=:).*?(?=})", str(i)).group(0) + ".zip", 'r') as zipf:
                if not os.path.exists(targetpath + '\\' + "tmp" + str(thread)):  # 检查是否存在临时文件夹，如不存在则创建
                    os.mkdir(targetpath + '\\' + "tmp" + str(thread))
                try:  # 尝试解压.nomedia文件，如果没有nomedia文件则解压001文件
                    zipf.extract(".nomedia", targetpath + '\\' + "tmp" + str(thread))
                    nomedia = True  # 。nomedia文件解压成功标识
                except KeyError:
                    nomedia = False  # 。nomedia文件解压失败标识
                    #   在压缩包里找到001文件，并解压
                    for h in zipf.namelist():
                        if fnmatch.fnmatch(h, '*1.*'):
                            file = h
                            break
                    zipf.extract(file, targetpath + '\\' + "tmp" + str(thread))
            # 如果nomedia文件被成功解压则对比源目录和被解压的nomedia文件的md5值。如果一致则不需要压缩，不一致则删除已有压缩包并重新压缩
            # 如果nomedia文件没有被成功解压则解压001文件进行对比
            if nomedia:
                if CommonFuntion.GetMd5(tmpdir + "\\" + ".nomedia") == CommonFuntion.GetMd5(
                        targetpath + '\\' + "tmp" + str(thread) + "\\" + ".nomedia"):  # 对比md5
                    # print("\033[1;31m 跳过\033[0m  \"" + "\033[1;36m " + re.search("(?<={).*?(?=:)", str(i)).group(0) + "\033[0m" + "\"  \033[1;31m 理由：文件夹已被压缩\033[0m\n")
                    errlist.append("\033[1;36m " + re.search("(?<={).*?(?=:)", str(i)).group(0) + "\033[0m" + "    id：" + "\033[1;33m " + CommonFuntion.Getid(
                        CommonFuntion.GetDirList(tmpdir, 'file')) + "   \033[1;31m 错误类型：已存在压缩包无需压缩\033[0m")
                    shutil.rmtree(targetpath + '\\' + "tmp" + str(thread))
                    continue
                else:  # 不成功则删掉重新压缩
                    os.remove(targetpath + '\\' + re.search("(?<=:).*?(?=})", str(i)).group(0) + ".zip")
                    ZipPack(targetpath, tmpdir, re.search("(?<=:).*?(?=})", str(i)).group(0), CommonFuntion.GetDirTime(tmpdir))
            else:  # nomedia文件没有被成功解压则解压001文件进行对比
                ofile = ""
                for g in CommonFuntion.GetDirList(tmpdir, 'file'):  # 找到001文件
                    if fnmatch.fnmatch(g, '*1.*'):
                        ofile = g
                        break
                if CommonFuntion.GetMd5(tmpdir + "\\" + ofile) == CommonFuntion.GetMd5(targetpath + '\\' + "tmp" + str(thread) + "\\" + ofile):  # 对比md5
                    # print("\033[1;31m 跳过\033[0m  \"" + "\033[1;36m " + re.search("(?<={).*?(?=:)", str(i)).group(0) + "\033[0m" + "\"  \033[1;31m 理由：文件夹已被压缩\033[0m\n")
                    errlist.append("\033[1;36m " + re.search("(?<={).*?(?=:)", str(i)).group(0) + "\033[0m" + "    id：" + "\033[1;33m " + CommonFuntion.Getid(
                        CommonFuntion.GetDirList(tmpdir, 'file')) + "   \033[1;31m 错误类型：已存在压缩包无需压缩\033[0m")
                    shutil.rmtree(targetpath + '\\' + "tmp" + str(thread))
                    continue
                else:  # 不成功则删掉重新压缩
                    os.remove(targetpath + '\\' + re.search("(?<=:).*?(?=})", str(i)).group(0) + ".zip")
                    ZipPack(targetpath, tmpdir, re.search("(?<=:).*?(?=})", str(i)).group(0), CommonFuntion.GetDirTime(tmpdir))
        #  如果不存在压缩包则直接压缩
        else:
            ZipPack(targetpath, tmpdir, re.search("(?<=:).*?(?=})", str(i)).group(0), CommonFuntion.GetDirTime(tmpdir))


def StartZipPack(booklist: list, sourcepath: str, targetpath: str, thread: int):
    """
    压缩任务启动函数
    :param booklist:    已经排序号的文件夹列表
    :param sourcepath: 文件夹源路径
    :param targetpath: 压缩包存放路径
    :param thread: 线程数
    :return:
    """
    totalTask = len(booklist)
    pilelist = main.DistributionBucket(booklist, thread)  # 把排序好的文件夹分割
    # 进度条处理
    zipMM = Manager()
    ziptasklist = zipMM.list()  # 共享进度条
    ziperrorlist = zipMM.list()  # 共享错误列表
    zipprocessList = []  # 进程列表
    # 根据线程数启动对应数量的进程
    print('制作压缩包中....')
    for i in range(thread):
        if i == 0:  # 如果是第一次循环则启动进度条子进程
            ziptaskthread = Process(target=main.Task, args=(totalTask, ziptasklist,))
            ziptaskthread.start()
            zipprocessList.append(ziptaskthread)
        ZipProcessThread = Process(target=ZipWorkThread, args=(sourcepath, targetpath, pilelist[i], i, ziptasklist, ziperrorlist))
        ZipProcessThread.start()
        # ZipProcessThread.join()
        zipprocessList.append(ZipProcessThread)
    # 检查进程是否工作完成
    for j in zipprocessList:
        j.join()
    return ziperrorlist


if __name__ == '__main__':
    pass

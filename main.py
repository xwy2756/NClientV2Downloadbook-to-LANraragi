import copy
import multiprocessing
import re

import CommonFuntion
import Zip
import Formatting

from alive_progress import alive_bar


def ListInstDirTime(dirlist: list, sourcepath: str):
    """
    在列表中插入文件夹时间
    :param dirlist: 本子文件夹子目录列表
    :param sourcepath: 本子文件夹源目录
    :return:
    """
    relist = []
    print('处理文件列表中.....')
    #   遍历整个列表，给每个元素都加上时间戳
    with alive_bar(len(dirlist), force_tty=True, length=20, dual_line=False, max_cols=1000) as bar:
        for i in dirlist:
            relist.append("{" + i + ":" + CommonFuntion.GetDirTime(sourcepath + '\\' + i) + "}")
            bar()
        return relist


def Sort(dirlist: list):
    """
    对本子按照本子文件夹的修改时间进行排序并添加序号

    :param dirlist: 本子文件夹列表
    :return: {list} 排序好的本子列表
    """
    print('处理排序中.....')
    rank = dirlist[0]  # 获取起始元素
    Sortlist = []
    loop_2 = range(len(dirlist))  # 确定总循环次数
    # nn = len(dirlist) - 1  # 进度条
    num = 1  # 序号
    tmp = dirlist
    with alive_bar(len(dirlist), force_tty=True, length=20, dual_line=False, max_cols=1000) as bar:
        for _ in loop_2:  # 主循环
            # print("处理排序,当前进度:" + "\033[1;31m " + str(i / nn * 100) + "\033[0m" + "%")
            if len(tmp) != 1:  # 当列表只剩一个元素时不进入排序
                for j in tmp:
                    if int(re.search("(?<=:).*?(?=})", str(rank)).group(0)) > int(re.search("(?<=:).*?(?=})", str(j)).group(0)):  # 如果rank大于j则rank为j
                        rank = j
                Sortlist.append(re.sub(r"(?<=:).*?(?=})", str(num), rank, 0))
                tmp.remove(rank)
                rank = tmp[0]
                num += 1
            else:
                Sortlist.append(re.sub(r"(?<=:).*?(?=})", str(num), tmp[0], 0))
            bar()
    return Sortlist


def DistributionBucket(arr: list, count: int):
    """
    把一个完整的一维列表变成多个二维列表
    :param arr: 需要分割的列表
    :param count:  分割数量
    :return:{list[2]}  二维列表
    """
    if count == 0:
        return arr
    BucketSize = len(arr) // count
    Buckets = []
    for i in range(count):  # 创建桶 0号桶是主桶
        Buckets.append([])
        for j in range(BucketSize):  # 往桶里放入值
            Buckets[i].append(arr[0])
            arr.remove(arr[0])
    if len(arr) != 0:  # 把列表剩余值放入主桶中
        for i in arr:
            Buckets[0].append(i)
            arr.remove(i)
    return Buckets


def Task(total: int, tasktarget: list):
    """
    显示任务进度条
    :param total:
    :param tasktarget:
    :return:
    """
    # 创建进度条对象
    with alive_bar(total, force_tty=True, length=20, dual_line=False, max_cols=1000) as bar:
        items = 0
        # 进行一个死循环，不停的检测子进程共享的变量是否有增加，有增加则进度加一，没有则不增加，当已执行任务和总总任务数一样时，退出死循环
        while True:
            task = len(tasktarget)
            if items != task:
                bar()
                bar.text(tasktarget[items])
                items += 1
            if items == total:
                break


if __name__ == '__main__':
    # 参数设置
    BookSourcePath = 'E:\\同步\\NClientV2\\Download'  # 本子源目录
    ZipSavePath = 'E:\\同步\\NClientV2\\Backup'  # 压缩包存放目录
    BackupFilePath = 'G:\\下载'
    TagFileName = 'Tag.py'
    ProcessNumber = 2  # 多核心设置

    # 处理目录为列表
    if ProcessNumber == 0:  # 判断是否需要自动设置线程
        ProcessNumber = multiprocessing.cpu_count()
    SourcePathList = ListInstDirTime(CommonFuntion.GetDirList(BookSourcePath, 'dir'), BookSourcePath)  # 获取需要压缩的文件夹
    SourcePathList = Sort(SourcePathList)  # 取得文件夹下的子目录排序需要压缩的文件夹
    SourcePathList2 = copy.copy(SourcePathList)

    #   开始处理
    errList1 = Zip.StartZipPack(SourcePathList, BookSourcePath, ZipSavePath, ProcessNumber)
    errList2 = Formatting.StartRecode(SourcePathList2, BookSourcePath, BackupFilePath, ProcessNumber, TagFileName)
    # for errstr in errList1:
    #     print(errstr)
    # for errstr2 in errList2:
    #     print(errstr2)

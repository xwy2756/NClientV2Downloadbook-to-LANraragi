# NClientV2Downloadbook-to-LANraragi
将NClientV2下载的图书上传至LANraragi,并保存相应的Tag

声明:

我第一次使用github,这东西有点高级,库有不对请见谅.

!!!我不知道这对有着其他来源漫画的Lanrargi有何副作用,我强烈建议您开始之前导出一份Lanrargi备份文件作为备份!!!
    
脚本说明:

这是一个从NClientV2下载文件夹中,压缩本子,并且按照修改时间顺序排序本子.然后上传至LANraragi并且修改LANraragi备份文件中对应的本子属性

  !!!这不是一键式傻瓜脚本.你需要手动把本子移动到LANraragi目录下,并且手动获取LANraragi的备份文件!!!

文件功能:

  CommonFuntion.py ---- 常用函数库
  
  Formatting.py ---- LANraragi备份文件处理脚本
  
  Zip.py ---- 压缩脚本
  
  TranslateTag.py ---- Tag翻译脚本
  
  Tag.py ---- 无作用,仅作Tag翻译表储存用
  
  main.py ---- 脚本入口

如何使用:

  首先你需要一个安装了alive-progress的python解释器(或者编辑main脚本,注释掉第9行,并且把其中的Task函数下的内容替换为pass),然后使用pycharm或者类似的可以建立python工程的软件建立一个python工程,并把这个库里面的东西放进去.
  接下来打开并编辑mian脚本,在main脚本下有几个变量:
  
          BookSourcePath ---- 你NClientV2的下载文件夹
          
          ZipSavePath ---- 你想存放压缩包的目录
          
          BackupFilePath ---- LANraragi备份文件的目录
          
          TagFileName ---- 存放Tag翻译表的文件,这不需要更改
          
          ProcessNumber ---- 需要使用的cpu核心数(2最佳,我不知道为什么高于2会导致进程卡死)

          
  把BookSourcePath更改为你的NClientV2的下载文件夹,并且把ZipSavePath更改为你需要的目录,以及BackupFilePath填上你的备份文件可能保存的位置,然后运行main,等待压缩完毕.
  
  此时你下载的NClientV2本子会按照修改时间顺序压缩并更名为数字序号.压缩完毕后请把这些压缩包上传至LANraragi以便开始第二步.
  
  等待LANraragi上传结束,你可能需要一点时间来等待LANraragi处理内部数据库.LANraragi处理内部数据库完成后,请导出LANraragi备份文件,这是个.json格式文件
  
  让我们回到main,此时脚本应该会提示你备份文件出错,请按照提示输入对应的单词继续脚本并等待脚本处理备份文件.如果一直重复错误过程,请检查BackupFilePath变量下的路径下是否存在最新的备份文件
  
  当脚本处理结束后,请把备份文件导入至LANraragi,你就能在LANraragi中浏览你在NClientV2下载的本子了

关于Tag翻译:

  脚本每次运行时,都会从已有本子中寻找新的tag加入到Tag.py中.
  
  Tag.py的结构类似于python的dict:
  
    TagDictionaries = { 
           'bdsm': '性虐待',
           'multi-work series': None,
           'collar': '项圈',
           'dark skin': '深色皮肤',
           'anal': '肛门'
           }

  左边是原始tag名称,右边是翻译过后的名称.None代表暂无翻译
         
  你只需要手动在这里更改键值对就能更改脚本执行时对应修改的tag翻译
  如果你不需要翻译,删除Tag.py里面的所有内容并保存即可(不要删除Tag.py文件)


Since English is not my native language, so

!!!!!!!!! Machine Translation WARNING!!!!!!!!!

!!!!!I'm not sure how this will affect Lanrargi,if which has comics from other sources, and I highly recommend exporting a backup Lanrargi file as a backup before you start!!!!!

Upload the NClientV2 downloaded book to LANraragi and save the corresponding Tag

Statement:

I'm using github for the first time, this thing is a little advanced, the library is wrong, please forgive me.

Script description:

This is a download from the NClientV2 folder, compress the books, and sort the books in order of modification time. Then upload to LANraragi and modify the corresponding book sub-properties in the LANraragi backup file

!!!!!!!!! This is not a one-click dumb script. You need to manually move the book to the LANraragi directory and manually get the LANraragi backup file!!!

File function:

    CommonFuntion.py ---- Common function library 
    
    Format. py ---- LANraragi backup file processing script 
    
    Zip.py ---- Compress the script
    
    TranslateTag.py ---- Tag translates the script
    
    Tag.py ---- has no effect and is only used to store Tag translation tables
    
    main.py ---- script entry

How to use:

First you need a python interpreter with alive-progress installed (or edit the main script, comment out line 9, and replace the contents of the Task function with pass), and then create a python project using pycharm or similar software that can create python projects software, and put in the contents of this vault.

Next open and edit the mian script, which has several variables under the main script:

    BookSourcePath ---- The download folder of your NClientV2
    
    ZipSavePath ---- The directory where you want to store the zip package
    
    BackupFilePath ---- LANraragi directory of the backup file
    
    TagFileName ---- stores the file for the Tag translation table, which does not need to be changed
    
    ProcessNumber ---- Number of cpu cores to be used (2 is best, I don't know why any higher than 2 would cause the process to stall)

Change BookSourcePath to the download folder of your NClientV2, change ZipSavePath to the directory you want, and BackupFilePath to the location where your backup files are likely to be saved, then run main and wait for the compression to finish.

At this point, the NClientV2 file you downloaded will be compressed in chronological order and renamed to a numeric sequence number. After the compression is complete, please upload these compressed packages to LANraragi to begin the second step.

Wait for the LANraragi upload to finish, you may need a little time for LANraragi to process the internal database. After LANraragi finishes processing the internal database, export the LANraragi backup file, which is a.json file

Let's go back to main. At this point, the script should prompt you to backup the file error, please follow the prompt to enter the corresponding word to continue the script and wait for the script to process the backup file. If the error process keeps repeating, check whether the latest backup file exists in the directory under the BackupFilePath variable

When the script is finished, please import the backup file to LANraragi and you will be able to browse the book you downloaded from NClientV2 in LANraragi

About Tag Translation:

Each time the script is run, it finds a new Tag from the existing book and adds it to tag.py.

Tag.py is structured like python's dict:

    TagDictionaries = { 
           'bdsm': '性虐待',
           'multi-work series': None,
           'collar': '项圈',
           'dark skin': '深色皮肤',
           'anal': '肛门'
    }

On the left is the original tag name, and on the right is the translated name. None indicates no translation



You only need to manually change the key-value pairs here to change the tag translation corresponding to the modifications when the script is executed

If you don't need to translate, just delete everything in Tag.py and save it (don't delete Tag.py file)

 

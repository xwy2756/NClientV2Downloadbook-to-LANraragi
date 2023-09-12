# NClientV2Downloadbook-to-LANraragi
将NClientV2下载的图书上传至LANraragi,并保存相应的Tag

声明:

    我第一次使用github,这东西有点高级,库有不对请见谅.
    
脚本说明:

  这是一个从NClientV2下载文件夹中,压缩本子,并且按照修改时间顺序排序本子.然后上传至LANraragi并且修改LANraragi备份文件中对应的本子属性

      !!!这不是一键式傻瓜脚本.你需要手动把本子移动到LANraragi目录下,并且手动获取LANraragi的备份文件!!!

文件功能:

  CommonFuntion.py ---- 常用函数库
  
  Formatting.py ---- LANraragi备份文件处理脚本
  
  Zip.py ---- 压缩脚本
  
  TranslateTag.py ---- Tag翻译脚本
  
  Tag.py ---- 无作用,仅作Tag存储
  
  main.py ---- 脚本入口

如何使用:

  首先你需要一个安装了alive-progress的python解释器,在main脚本下有几个变量:
  
          BookSourcePath ---- 你NClientV2的下载文件夹
          
          ZipSavePath ---- 你想存放压缩包的目录
          
          BackupFilePath ---- LANraragi备份文件的目录
          
          TagFileName ---- 存放Tag翻译表的文件,这不需要更改
          
          ProcessNumber ---- 需要使用的cpu核心数(2最佳,我不知道为什么高于2会导致进程卡死)

          
  把BookSourcePath更改为你的NClientV2的下载文件夹,并且把ZipSavePath更改为你需要的目录,以及BackupFilePath填上你的备份文件可能保存的位置,然后运行main,等待压缩完毕.
  
  此时你下载的NClientV2本子会按照修改时间顺序压缩并更名为数字序号.压缩完毕后请把这些压缩包上传至LANraragi以便开始第二步.
  
  等待LANraragi上传结束,你可能需要一点时间来等待LANraragi处理内部数据库.LANraragi处理内部数据库完成后,请导出LANraragi备份文件,这是个.json格式文件
  
  让我们回到main,此时脚本应该会提示你备份文件出错,请按照提示输入对应的单词继续脚本并等待脚本处理备份文件.
  
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

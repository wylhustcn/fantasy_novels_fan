# fantasy_novels_fan
最近书荒比较严重，正好学习python，建个repo来想想办法
***
***
## Script 1 : Biquge_text_spider.py
> 请在Python3下运行

这是一个Python脚本，配置后可以从[笔趣阁](https://www.biqugex.com)搜索并下载小说。

注：   
*1、此脚本参考Jack-Cui的[Python3网络爬虫快速入门实战解析](https://blog.csdn.net/c406495762/article/details/78123502)制作*    
*2、此脚本是学习时候用来练手的，顺便解决书荒的问题*   
*3、有问题和建议可以直接开issues讨论，正在学习Python爬虫中，欢迎交流讨论*
***
### 环境安装
配置好Python3后，直接*`pip install requests`*安装requests库即可。   
如果国外源不可用，直接通过国内的镜像安装*`pip --trusted-host=mirrors.aliyun.com -i http://mirrors.aliyun.com/pypi/simple/ install requests`*。
***
### 配置和运行
直接使用命令行运行

> *`python Biquge_text_spider.py`*   

然后按要求输入需要搜索的小说名称，并选择需要搜索的序号即可。   
小说会下载至*`download`*文件夹中。
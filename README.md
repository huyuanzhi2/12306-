# 12306_PC

简介：
12306查票软件
Python3.6 + Qt5
用到的第三方库只有requests和PyQt5

使用方法：
运行manage.py即可

gui.py -- Qt界面布局
manage.py -- 逻辑处理
parse_station.py -- 查询所有车站，将结果导出到station.py
station.py -- 字典文件，内含所有车站
query.py -- 查询函数，可单独运行，
    格式 python query.py 时间 起点 终点
    例如 python query.py 2017-09-02 北京 上海

dist目录含有利用pyinstaller编译好的查票软件，pyinstaller暂不支持python3.6，详情请看http://blog.csdn.net/yz271212/article/details/71171824

初学Qt5，写得比较渣。。。。
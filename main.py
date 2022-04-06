# coding:utf-8
# 定时执行批处理程序
# 作者: dsy
# 时间：2022/4/6 13:21

import subprocess       #执行cmd程序导入包
import os               #读取文件目录引用包
import json             #解析json引用包
import configparser     #读取配置文件引用包
import _thread          #多线程
import datetime,time    #导入时间包

# 定义每天执行的时间 全局变量
global setHour
global setMinite

#默认为23点6分
setHour = 23
setMinite = 6

#读取ini方法
def read_ini(inikey,inivaluse):
    try:
        config = configparser.ConfigParser()

        # 配置文件路径
        print(os.getcwd() + "/config.ini")

        # 读取配置文件
        config.read(os.getcwd() + "/config.ini")

        # 读取配置文件对应的内容
        convaluse = config.get(inikey, inivaluse)

        # 返回值
        return convaluse
    except:
        return "";

# 执行程序
def run_program():
    #读取配置文件 获取执行文件的列表
    str_procelist = read_ini("appbase","procelist")

    #打印读取到的内容
    print(str_procelist)
    print(type(str_procelist))

    #解析成json数据
    json_procelist = json.loads(str_procelist)

    #程序的根目录
    root = os.getcwd()
    #遍历json
    for index in range(len(json_procelist)):
        # 启动线程，在线程内执行
        try:
            _thread.start_new_thread(exe_proc,(root,json_procelist[index],))
        except:
            print("Error,线程启动失败")

# 执行bat程序
def exe_proc(root,bat_name):
    # cmd = 'cmd.exe d:/start.bat'
    # 执行对应的文件
    p = subprocess.Popen("cmd.exe /c" + root + "/" + bat_name, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # 读取返回值内容：bytes
    curline = p.stdout.readline()

    # 打印返回值内容:bytes
    print(type(curline))

    # 当前返回值内容：string
    str_curline = ''
    while (curline != b''):
        # 打印返回值内容:bytes
        print(curline)

        # 解析返回值内容：string
        str_curline = curline.decode('GB2312', 'ignore')

        # 打印返回值内容:string
        print(str_curline)
        writeLog('【' + bat_name + '】' + str_curline)

        # 继续读取返回值内容
        curline = p.stdout.readline()

    # 等待程序执行完成
    p.wait()

    # 打印返回状态
    print(p.returncode)

# 线程执行
def thread_proc():
    # 使用死循环一直循环执行，每1分钟循环一次
    while (True):
        # 获取当前时间
        now_time = datetime.datetime.now()
        # 格式化时间字符串
        str_time = now_time.strftime("%Y-%m-%d %X")
        tup_time = time.strptime(str_time, "%Y-%m-%d %X")
        time_sec = time.mktime(tup_time)
        # 转换成时间戳 进行计算
        time_sec += 1
        tup_time2 = time.localtime(time_sec)
        str_time2 = time.strftime("%Y-%m-%d %X", tup_time2)
        print(str_time)
        print(str_time2)

        hour = tup_time.tm_hour
        minite = tup_time.tm_min

        if minite == 30:
            os.system('cls')

        if hour == setHour and minite == setMinite:
            run_program()

        time.sleep(60)

#读取设置的时间
def readSetTime():
    global setHour
    # 读取小时
    str_hour = read_ini("appbase","hour")

    # 设置小时
    if len(str_hour) != 0:
        setHour = int(str_hour)
    global setMinite
    # 读取分钟
    str_minite = read_ini("appbase","minite")

    # 设置分钟
    if len(str_minite) != 0:
        setMinite = int(str_minite)

def writeLog(logInfo):
    # 当前时间
    now_time = datetime.datetime.now()
    # 格式化时间字符串
    str_time_now = now_time.strftime("%Y-%m-%d %X")
    str_time = now_time.strftime("%Y-%m-%d")
    root = os.getcwd()
    f = open(root + '/log'+str_time + '.txt','a+')
    f.write("\n" + str_time_now + " " + logInfo)
    f.close()
    pass

if __name__ == '__main__':
    #读取配置的时间，执行批处理的时间
    readSetTime()

    # 主线程执行程序
    thread_proc()

    # 暂停
    aa = input()
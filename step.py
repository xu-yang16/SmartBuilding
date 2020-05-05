# -*- coding: utf-8 -*-
# ping 39.100.78.210
import os
import sys
sys.path.append('../IoT')
import Interface
import time
from time import sleep
import datetime


def del_old_dir(path):  # 获取目录路径
    print("删除文件：")
    for root, dirs, files in os.walk(path):
        for file in files:
            print(os.path.join(path,file))
            os.remove(os.path.join(path,file))
    print("\n")

def write_setting(roomList, value):
    # 写入开度设置
    with open("./step_record/setting.txt", "a") as f: 
        f.write("****************************************变化风阀开度**************************************\n")
        for room in roomList:
            f.write("time:{}\troom:{}\tval_open:{}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), room[0:2], value))

def step(step_begin_time = 3, step_end_time = 6, scale=[40, 20]):
    # 记录时间
    TIME_FLAG = 0
    DAY = 1
    # flag=0标志着开度为scale[0]; flag=1标志着开度为scale[1]
    flag = 0
    # 开始记录的时间
    start_time = datetime.datetime.now()

    # 设定初始值
    roomList=[]
    roomList.append((8, 1))
    roomList.append((8, 5))
    roomList.append((8, 10))
    # 各房间风阀开度初始化为scale[0]
    for room in roomList: 
        Interface.controlRoom(*room[0:2], scale[0])
    # 写入开度设置
    write_setting(roomList, scale[0])
    
    while True:
        try:
            # 设定开始阶跃的时刻step_begin_time&结束阶跃的时刻step_end_time
            t_set, t_now, kaidu_now, time_now = Interface.dataForPID(*room[0:2])
            passtime = datetime.datetime.now() - start_time
            if time_now[0] == '16':#passtime.seconds >= step_end_time * 60 * 60:
                # 对(5,1~16)房间设置回到70，退出程序。
                for room in roomList: 
                        Interface.controlRoom(*room[0:2],scale[0])
                # 写入开度设置
                write_setting(roomList, scale[0])
                break
            elif time_now[0] == '13' and flag == 0:# passtime.seconds >=  step_begin_time * 60 * 60 and flag == 0:
                flag = 1
                # 对roomList房间给阶跃信号，记录阶跃响应曲线。
                for room in roomList: 
                        Interface.controlRoom(*room[0:2],scale[1])
                # 写入开度设置
                write_setting(roomList, scale[1])
            # 记录房间温度变化曲线
            for room in roomList:
                # 设定的温度, 当前温度, 当前开度, 当前时间
                t_set, t_now, kaidu_now, time_now = Interface.dataForPID(*room[0:2])
                # 写入日期信息
                if time_now[0] == '0' and TIME_FLAG == 0:
                    DAY = DAY + 1
                    TIME_FLAG = 1
                elif time_now[0] != '0':
                    TIME_FLAG = 0
                #写入文件
                with open("./step_record/state_in_{}_{}.txt".format(*room[0:2]), "a") as f:
                    f.write("{}:{}:{}:{}\t{}\t{}\t{}\t{}\t{}\n".format(DAY,*time_now[0:3], *room[0:2], t_set, t_now, kaidu_now))
            #打印输出
            print("{}:{}:{}:{}\t{}\t{}\t{}\t{}\t{}\n".format(DAY,*time_now[0:3], *room[0:2], t_set, t_now, kaidu_now))
        except Exception as e:
            print("*********************读取温度数据出现错误...*******************")
        sleep(60)

if __name__ == '__main__':
    # 删除上一次的文件
    del_old_dir("./step_record/")
    # 开始实验
    step()
    
    
    